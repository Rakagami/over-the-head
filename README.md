# Over-the-Head

A simple and easy to use CLI tool to check what's currently over-your-head. (_currently only focuses on satellites_)

## Quick Start

> Note: Currently, this project only supports recognizing Starlink satellites and their shells

```
$ cd /path/to/this/repository
$ pip install -r requirements.txt
$ python -m main 59.6395 17.9215 2023-10-03T12:07:00 2023-10-03T12:08:00 -o output.csv
```

After executing the above commands and waiting for a while, you will have a csv file containing all (_starlink_) satellites that were visible above the 0° elevation during the entire timespan. You can set the min elevation with the `--min_elevation` flag. The output looks as follows:

```
$ head -n 5 output.csv
,Satellite,COSPAR,Date,LS,Failed,Launch Vehicle,Remarks,GROUP,STARLINK_NUMBER
183,Starlink v1.0 L4-4 (Starlink 1200),2020-012D,2020-02-17,CC SLC-40,,Falcon-9 v1.2 (Block 5),"with Starlink v1.0 L4-1, ..., L4-60",L4,1200
203,Starlink v1.0 L4-24 (Starlink 1199),2020-012Z,2020-02-17,CC SLC-40,,Falcon-9 v1.2 (Block 5),"with Starlink v1.0 L4-1, ..., L4-60",L4,1199
260,Starlink v1.0 L5-21 (Starlink 1207),2020-019W,2020-03-18,CCK LC-39A,,Falcon-9 v1.2 (Block 5),"with Starlink v1.0 L5-1, ..., L5-60",L5,1207
291,Starlink v1.0 L5-52 (Starlink 1293),2020-019BD,2020-03-18,CCK LC-39A,,Falcon-9 v1.2 (Block 5),"with Starlink v1.0 L5-1, ..., L5-60",L5,1293
```

---

If you are specifically interested in which starlink groups is over your head, you can use the `--starlink_groups` flag. It will yield an output like as follows:

```
$ python -m main 59.6395 17.9215 2023-10-03T12:07:00 2023-10-03T12:08:00 --starlink_groups --min_elevation 20
['G1', 'G2', 'G3', 'G4']
```

## FAQ

* **What are Starlink Groups?**

The definition of a starlink group is taken from [here](https://space.skyrocket.de/doc_sdat/starlink-v1-5.htm) and [here](https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm). Essentially they refer to which orbital shell a satellite belongs. This is interesting when discussing connectivity to starlink when you are at a specific latitude.

* **Does this access historical TLE data, so we can make accurate predictions on timestamp far to the past?**

No. At least not yet. The api leaves room for this feature with the `reference_epoch` parameter.

* **The command takes so long! Why is that?**

Even by caching the http requests for the tles, the majority of the computation times is probably spent on orbit propagation for every satellite in the constellation. Maybe we can cache the sgp4 calculations, but that is not yet been implemented.

* **Why is thera a FAQ for such a small project?**

Because I can.
