"""
Compute the height-to-phase factor (h2ph) from the following interferograms:

- ifgs_srp (=subtracted reference phase, computed using SNAP/GPT using the
  Interferogram operator by setting flat Earth phase = true and topographic
  phase = false);
- ifgs_srd (=subtracted reference phase, computed using SNAP/GPT  using the
  Interferogram operator by setting flat Earth phase = true, and topographic
  phase = true);
- H (the DEM in radarcoordinates).

Compare the h2ph computed withing this script to the one computed with SNAP/GPT
via the BandManths operator.

Run as:

python check_h2ph.py --h2ph-path ./h2ph.dim --ifgs-srp-path ./ifgs_srp.dim --ifgs-srd-path ./ifgs_srd.dim

"""
import argparse

import esa_snappy
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--h2ph-path", default="./h2ph.dim", type=str)
    parser.add_argument("--ifgs-srp-path", default="./ifgs_srp.dim", type=str)
    parser.add_argument("--ifgs-srd-path", default="./ifgs_srd.dim", type=str)
    args = parser.parse_args()
    return vars(args)


def read_wavelength(path):
    scene = esa_snappy.ProductIO.readProduct(path)
    Sentinel1Utils = esa_snappy.jpy.get_type("eu.esa.sar.commons.Sentinel1Utils")
    su = Sentinel1Utils(scene)
    return su.wavelength


def read_raster_band(path, band_name):
    product = esa_snappy.ProductIO.readProduct(path)
    band = product.getBand(band_name)
    w = band.getRasterWidth()
    h = band.getRasterHeight()
    data = np.zeros(h*w, dtype=np.float32)
    band.readPixels(0, 0, w, h, data)
    return data.reshape(h, w)


def calculate_h2ph(ifgs_srp, ifgs_srd, H, wavelength):
    m2ph = 4 * np.pi / wavelength
    phase_height = np.angle(ifgs_srd * np.conj(ifgs_srp))
    h2ph = phase_height / H / m2ph
    return np.where(H > 0, h2ph, 0.)


def print_stats(x):
    print(f"Shape: {x.shape} - Max: {x.max()} - Min: {x.min()}"
          f" - Avg: {x.mean()} - Std: {x.std()}")


def main(h2ph_path, ifgs_srp_path, ifgs_srd_path):
    # Load height-to-phase factor computed within SNAP/GPT
    h2ph = read_raster_band(h2ph_path, "h2ph")
    print(f"** h2ph read from {h2ph_path} **")
    print_stats(h2ph)

    # Parse wavelength from any of the datasets
    wavelength = read_wavelength(h2ph_path)

    # Load raster datasets
    ifgs_srp_real = read_raster_band(ifgs_srp_path, "i_ifg_IW2_VV_16Apr2025_28Apr2025")
    ifgs_srp_imag = read_raster_band(ifgs_srp_path, "q_ifg_IW2_VV_16Apr2025_28Apr2025")
    ifgs_srd_real = read_raster_band(ifgs_srd_path, "i_ifg_IW2_VV_16Apr2025_28Apr2025")
    ifgs_srd_imag = read_raster_band(ifgs_srd_path, "q_ifg_IW2_VV_16Apr2025_28Apr2025")
    H = read_raster_band(ifgs_srd_path, "elevation")

    # Recast real and imaginary parts into complex numbers
    ifgs_srp = ifgs_srp_real + ifgs_srp_imag * 1j
    ifgs_srd = ifgs_srd_real + ifgs_srd_imag * 1j

    # Recompute height-to-phase factor from its input variables
    h2ph_computed = calculate_h2ph(ifgs_srp, ifgs_srd, H, wavelength)
    print("** h2ph recomputed **")
    print_stats(h2ph_computed)

    # Compare the two element-wise
    allclose = np.allclose(h2ph, h2ph_computed)
    print(f"** All values are equal: {allclose} **")


if __name__ == "__main__":
    args = parse_args()
    main(**args)
