# Coregistration with SNAP

This repository contains material to coregister Sentinel-1 IW SLC products using the ESA [SNAP software](https://earth.esa.int/eogateway/tools/snap)

## Installation

For the regular installation (via GUI), one can download the OS-specific installer from [here](https://step.esa.int/main/download/snap-download/).

The installing procedure can also take care of installing the Python interface to SNAP. It should be enough to follow the given instructions, for more informations see [here](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/3114106881/Installation+and+configuration+of+the+SNAP-Python+esa_snappy+interface+SNAP+version+12)

## Examples

* [examples/gpt/TOPSAR-Coreg-Interferogram](./examples/gpt/TOPSAR-Coreg-Interferogram/): use the SNAP Graph Processing Tool (GPT) to coregister and calculate the interferogram for two (or more) Sentinel-1 scenes.
* [examples/gpt/test-parallelism](./examples/gpt/test-parallelism/): small test on parallelism of SNAP-GPT, based on the example above.
* [examples/gpt/Height-to-phase](./examples/gpt/Height-to-phase/): use SNAP-GPT to calculate the height-to-phase factor for two Sentinel-1 scenes.
* [examples/python/TOPSAR-Coreg-Interferogram](./examples/python/TOPSAR-Coreg-Interferogram/): run the coregistration / interferogram calculation for a set of Sentinel-1 scenes using the Python interface to GPT.

## Resources

* [Tutorial for TOPS Interferometry](https://step.esa.int/docs/tutorials/S1TBX%20TOPSAR%20Interferometry%20with%20Sentinel-1%20Tutorial_v2.pdf)

