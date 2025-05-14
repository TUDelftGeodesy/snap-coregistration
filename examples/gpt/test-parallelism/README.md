# Investigating parallelism

The test is based on an example that involves the coregistration of two S1 scenes and the interferogram generation (see [here](../TOPSAR-Coreg-Interferogram) for more information).

SNAP (GPT) implements tile parallelism for some of the tasks: datasets are split in tiles (by default, 512x512) and calculations are run in parallel over tiles using multithreading.

The parameters that sets the maximum number of threads used by GPT is `q` (set in command line via the `-q` option). For the tests in this folder, we obtain the following timings:

| q | Timings (s) | Speedup (compared to q=1) |
|---|-------------|---------------------------|
| 1 | 1296        | -                         |
| 2 | 948         | 1.4                       |
| 4 | 764         | 1.7                       |
| 6 | 490         | 2.6                       |
| 8 | 419         | 3.1                       |
