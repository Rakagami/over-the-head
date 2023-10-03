# Over-the-Head

A simple and easy to use CLI tool to check what's currently over-your-head. (_currently only focuses on satellites_)

## Quick Start

> Note: Currently, this project only supports recognizing Starlink satellites and their shells

```
cd /path/to/this/repository
pip install -r requirements.txt
python -m main 59.6395 17.9215 2023-10-03T12:07:00 2023-10-03T12:08:00 -o output.csv
```

After executing the above commands and waiting for a while, you will have a csv file containing all (_starlink_) satellites that had an overpass during the selected time interval.

To constitute an overpass, the following conditions must hold:
* During the given start and end, the satellite is visible over min elevation from the given ground position
* During the given start and end, the satellite never goes below the min elevation


If you are specifically interested in which starlink groups is over your head, you can use the `--starlink_groups` flag. It will yield an output like as follows:

```
python -m main 59.6395 17.9215 2023-10-03T12:07:00 2023-10-03T12:08:00 --starlink_groups --min_elevation 20
```

Output:

```
['G1', 'G2', 'G3', 'G4']
```

## FAQ

* **What are Starlink Groups?**

A the definition of a starlink group is taken from [here](https://space.skyrocket.de/doc_sdat/starlink-v1-5.htm) and [here](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm). Essentially they refer to which orbital shell a satellite belongs. This is interesting when discussing connectivity to starlink when you are at a specific latitude.
