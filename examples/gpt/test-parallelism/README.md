# Parallelism for coregistration and interferogram generation

Tests are based on one example (see [here](../TOPSAR-Coreg-Interferogram) for more information), but we have increased the AoI to cover 4 bursts.

SNAP (GPT) implements tile parallelism for some of the tasks: datasets are split in tiles (by default, 512x512) and calculations are run in parallel over tiles using multithreading.

Timing setting different values for `-q=` ("maximum parallelism used for the computation"), which should set the maximum number of threads used by GPT.

| q | Timings (s) | Speedup (compared to q=1) |
|---|-------------|---------------------------|
| 1 | 1296        | -                         |
| 2 | 948         | 1.4                       |
| 4 | 764         | 1.7                       |
| 6 | 490         | 2.6                       |
| 8 |          |                          |
