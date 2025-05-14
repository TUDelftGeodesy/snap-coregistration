import argparse

import esa_snappy
import geopandas as gpd
import numpy as np
import shapely
import shapely.wkt

from snapista import Graph, Operator


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mother-path", required=True, type=str)
    parser.add_argument("-d", "--daughter-path", required=True, type=str)
    parser.add_argument("-a", "--aoi-wkt", required=True, type=str)
    parser.add_argument("-o", "--output-path", default="./interferogram.dim", type=str)
    parser.add_argument("-f", "--output-format", default="BEAM-DIMAP", type=str)
    parser.add_argument("-q", default=1, help="Maximum parallelism, passed on to GPT")
    parser.add_argument("--view", action='store_true', default=False, help="Print graph as XML")
    args = parser.parse_args()
    return vars(args)


def get_burst_bounds(longitude_grid, latitude_grid, num_bursts):
    """ Get the bounds of the bursts from the lat/lon grids.

    For each subswath, the given lat/lon grids represent points taken on the
    burst edges (each row is a burst edge, with several points along columns)
    """
    grid = np.stack([longitude_grid, latitude_grid], axis=-1)
    bounds = []
    for nburst in range(num_bursts):
        # We build the burst bounds by selecting the relevant edges (the i-th
        # and i+1-th edges for the i-th burst) and taking the first and last
        # points - analogous to what SNAP does: see findValidBurstsBasedOnWkt()
        # https://github.com/senbox-org/s1tbx/blob/1daae60d572e3ad0ee98c0ce3538c61ad71d7fa1/s1tbx-op-sentinel1/src/main/java/org/esa/s1tbx/sentinel1/gpf/TOPSARSplitOp.java#L237
        coords = grid[[nburst, nburst, nburst+1, nburst+1], [0, -1, -1, 0]]
        geometry = shapely.Polygon(coords)
        bounds.append(geometry)
    return gpd.GeoSeries(bounds, crs="EPSG:4326")


def get_intersecting_bursts(scene_path, aoi_wkt):
    """ For each of the scene subswaths, find out how many bursts intersect the AoI. """
    # Open scene and load WKT geometry as a shapely object
    scene = esa_snappy.ProductIO.readProduct(scene_path)
    aoi = shapely.wkt.loads(aoi_wkt)

    # Use Sentinel1Utils module from SNAP to parse scene metadata
    Sentinel1Utils = esa_snappy.jpy.get_type("eu.esa.sar.commons.Sentinel1Utils")
    su = Sentinel1Utils(scene)
    bursts = {}
    for swath in su.getSubSwath():
        burst_bounds = get_burst_bounds(np.asarray(swath.longitude),
                                        np.asarray(swath.latitude),
                                        swath.numOfBursts)
        nbursts = burst_bounds.intersects(aoi).sum()
        if nbursts > 0:
            bursts[swath.subSwathName] = nbursts
    return bursts


def get_graph(mother_path, daughter_path, aoi_wkt, bursts,
              output_path="./interferogram.dim", output_format="BEAM-DIMAP"):
    """ Build processing graph. """
    g = Graph()

    g.add_node(operator=Operator("Read", file=mother_path),
               node_id="read-mother")
    g.add_node(operator=Operator("Read", file=daughter_path),
               node_id="read-daughter")
    sources = []
    for swath, nbursts in bursts.items():
        for scene in ("mother", "daughter"):
            g.add_node(operator=Operator("TOPSAR-Split",
                                         subswath=swath,
                                         wktAoi=aoi_wkt),
                       node_id=f"topsar-split-{scene}-{swath}",
                       source=f"read-{scene}")
            g.add_node(operator=Operator("Apply-Orbit-File"),
                       node_id=f"apply-orbit-file-{scene}-{swath}",
                       source=f"topsar-split-{scene}-{swath}")
        g.add_node(operator=Operator("Back-Geocoding"),
                   node_id=f"back-geocoding-{swath}",
                   source=[f"apply-orbit-file-mother-{swath}",
                           f"apply-orbit-file-daughter-{swath}"])
        g.add_node(operator=Operator("Enhanced-Spectral-Diversity"),
                   node_id=f"enhanced-spectral-diversity-{swath}",
                   source=f"back-geocoding-{swath}")
        g.add_node(operator=Operator("Interferogram",
                                     subtractFlatEarthPhase=True,
                                     subtractTopographicPhase=True),
                   node_id=f"interferogram-{swath}",
                   source=f"enhanced-spectral-diversity-{swath}")
        if nbursts > 1:
            # If the AoI intersects multiple bursts, apply TOPSAR-Deburst
            g.add_node(operator=Operator("TOPSAR-Deburst"),
                       node_id=f"topsar-deburst-{swath}",
                       source=f"interferogram-{swath}")
            sources.append(f"topsar-deburst-{swath}")
        else:
            sources.append(f"interferogram-{swath}")
    if len(sources) > 1:
        # If the AoI intersects multiple subswaths, apply TOPSAR-Merge
        g.add_node(operator=Operator("TOPSAR-Merge"),
                   node_id="topsar-merge",
                   source=sources)
        source = "topsar-merge"
    else:
        source = sources.pop()
    g.add_node(operator=Operator("Subset", geoRegion=aoi_wkt),
               node_id="subset",
               source=source)
    g.add_node(operator=Operator("Write",
                                 file=output_path,
                                 formatName=output_format),
               node_id="write",
               source="subset")
    return g


def main(mother_path, daughter_path, aoi_wkt,
         output_path="./interferogram.dim", output_format="BEAM-DIMAP",
         view=True, q=1):
    # Extract information on intersecting swaths/bursts from mother scene
    # TODO: check that daughter scene has same intersections?
    bursts = get_intersecting_bursts(mother_path, aoi_wkt)

    # Build graph
    graph = get_graph(mother_path, daughter_path, aoi_wkt, bursts, output_path, output_format)

    # Print XML or process graph
    if view:
        graph.view()
    else:
        graph.run(gpt_options=["-q", q])


if __name__ == "__main__":
    args = parse_args()
    main(**args)
