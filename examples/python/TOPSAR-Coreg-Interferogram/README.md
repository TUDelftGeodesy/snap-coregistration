# Coregistratrion and interferogram using Python

This folder contains an example on how one can compute the interferogram from two Sentinel-1 scenes from Python.

In particular, we make use of two Python libraries:

* [`esa_snappy`](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/19300362/How+to+use+the+SNAP+API+from+Python), the "traditional" Python interface of SNAP. It interacts with SNAP at lower level, so it allows one to use its core (Java) functionality from Python.

* [`snapista`](https://github.com/snap-contrib/snapista/tree/main), a more recent and more "Pythonic" interface to SNAP. It is essentially a thin wrapper around GPT, so better suited to setup graphs and run them using GPT under the hood.

From SNAP 12, they have been packaged as a single library and distributed together with SNAP.

## Files

* [`TOPSAR-Coreg-Interferogram.py`](./TOPSAR-Coreg-Interferogram.py): Python script that runs the coregistration and interferogram for two S1 scenes.
* [`TOPSAR-Coreg-Interferogram.bash`](./TOPSAR-Coreg-Interferogram.bash): bash script to run the Python code above - **WIP to run it on Spider**
