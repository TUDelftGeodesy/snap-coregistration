# Coregistratrion and interferogram using Python

This folder contains an example on how one can compute the interferogram from a stack of three Sentinel-1 scenes from Python. The main reason to use Python  to setup and run a SNAP/GPT worlflow is that it allows for more flexibility in setting up the analysis, e.g. selecting the relevant subswaths depending on the area of interest and carrying out conditional steps such as debursting/merging.

Here we make use of two Python libraries:

* [`esa_snappy`](https://senbox.atlassian.net/wiki/spaces/SNAP/pages/19300362/How+to+use+the+SNAP+API+from+Python), the "traditional" Python interface of SNAP. It interacts with SNAP at lower level, so it allows one to use its core (Java) functionality from Python.

* [`snapista`](https://github.com/snap-contrib/snapista/tree/main), a more recent and more "Pythonic" interface to SNAP. It is essentially a thin wrapper around GPT, so better suited to setup graphs and run them using GPT under the hood.

From SNAP 12, they have been packaged as a single library and distributed together with SNAP.

The approach implemented in [`TOPSAR-Coreg-Interferogram.py`](./TOPSAR-Coreg-Interferogram.py) uses `esa_snappy` to parse metadata from the Sentinel-1 scenes, and `snapista` to setup and run the workflow. Note that one can also use the script to **only output the XML graph**, which can then be run directly using GPT as: `gpt /path/to/graph.xml`.

## Files

* [`TOPSAR-Coreg-Interferogram.py`](./TOPSAR-Coreg-Interferogram.py): Python script that runs the coregistration and interferogram for two S1 scenes.
* [`TOPSAR-Coreg-Interferogram.bash`](./TOPSAR-Coreg-Interferogram.bash): bash script to run the Python code above - **WIP to run it on Spider**
