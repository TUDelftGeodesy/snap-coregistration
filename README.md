# Coregistration with SNAP

This repository contains material to coregister Sentinel-1 IW SLC products using the ESA [SNAP software](https://earth.esa.int/eogateway/tools/snap)

## Installation

### Workstation

On local workstations, one can follow the regular SNAP installation procedure (via GUI): download and run the OS-specific installer from [here](https://step.esa.int/main/download/snap-download/).

The procedure also takes care of installing the Python interface to SNAP. It should be enough to follow the given instructions, for more informations see [here](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/3114106881/Installation+and+configuration+of+the+SNAP-Python+esa_snappy+interface+SNAP+version+12)

### Spider

SNAP is installed and made available as a module on Spider. Make sure you can load modules from `/project/caroline/Software` by running:

```shell
module use /project/caroline/Software/modulefiles
```

SNAP can be used after running:

```shell
module load snap/12.0.0
gpt -h  # test that the GPT command line tool is available
```

In order to install the Python interface to SNAP, we create a Python environment using `virtualenv`:

```shell
module load python/3.10  # base environment on python 3.10
virtualenv venv
source venv/bin/activate
```

Install and configure [ESA-SNAPPY](https://github.com/senbox-org/esa-snappy) as:

```shell
pip install esa-snappy
cd venv/lib/python3.10/site-packages/esa_snappy
python snappyutil.py --snap_home /project/caroline/Software/snap/12.0.0  --java_module /project/caroline/Software/snap/12.0.0/esasnappy/modules/eu-esa-snap-esa-snappy.jar --jvm_max_mem 32G --log_file ./snappyutil.log
```

In order to use ESA-SNAPPY, make sure all the required modules as well as the virtual environment are loaded:

```shell
module load snap/12.0.0
module load python/3.10
source venv/bin/activate
```

## Examples

* [examples/gpt/TOPSAR-Coreg-Interferogram](./examples/gpt/TOPSAR-Coreg-Interferogram/): use the SNAP Graph Processing Tool (GPT) to coregister and calculate the interferogram for two (or more) Sentinel-1 scenes.
* [examples/gpt/test-parallelism](./examples/gpt/test-parallelism/): small test on parallelism of SNAP-GPT, based on the example above.
* [examples/gpt/Height-to-phase](./examples/gpt/Height-to-phase/): use SNAP-GPT to calculate the height-to-phase factor for two Sentinel-1 scenes.
* [examples/python/TOPSAR-Coreg-Interferogram](./examples/python/TOPSAR-Coreg-Interferogram/): run the coregistration / interferogram calculation for a set of Sentinel-1 scenes using the Python interface to GPT.

## Resources

* [Tutorial for TOPS Interferometry](https://step.esa.int/docs/tutorials/S1TBX%20TOPSAR%20Interferometry%20with%20Sentinel-1%20Tutorial_v2.pdf)

