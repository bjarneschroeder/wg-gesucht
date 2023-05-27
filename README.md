# WG-Gesucht Spider
This repository contains a scrapy project for scraping the german real estate website wg-gesucht.de.

May it help you maybe to find a flat really fast or to build a cool dataset.

**Please use the spider responsibly,
keep requests to a minimum.
No one likes bot traffic.**

## Scope and limitations of the project

Currently found flats will just be returned by the pipeline.
MongoDB connection or JSON Export are planned though.

Also only the first site is processed.
The scraper is thought to be scheduled more frequently,
so one gets notified earlier when flats are available.

Currently the scraper only collects individual flat offers,
no shared apartments.

## Possible Settings and Starting the Spider

The spider can be started as a Docker container.
Search settings are given via the enviornment,
when starting the spider.

### Building the Docker Image

Build the image with:

```shell
docker build -t wg_gesucht .
```

### Possible Search Arguments

`CITY_NAME`: Mandatory `str`.
Name of the city you are searching a flat in.

`MIN_ROOMS`:
Optional `float|int`.
The minimum amount of rooms a flat should have.
Has to be a whole number or `.5` decimal between
`2-9`, inclusive.

`MAX_RENT`:
Optional `int`.
The maximum amount of rent,
including additional costs ("warm").
Has to be between `1-9999`, inclusive.

`ONLY_PERMANENT_CONTRACTS`:
Optional `bool`.
If only flats should be collected that are
rentable on a permanent basis.
Defaults to `False`.

**Note**: Settings are logically connected
via an `and` condition.

*Example:*
You hand `"Berlin", min. 1.5 rooms, 1200 max. rent` the
spider will retrieve only flats in Berlin with atleat
1.5 rooms and rent below 1200 Euro.

### Starting the spider

Yoo can run your built container with:

```shell
docker run -e CITY_NAME=Berlin wg_gesucht
```

**Note**: You have to provide a valid city name.
All other parameters are optional.

For passing all paremeters you could also
use an environment file with the following structure:

```env
CITY_NAME=Berlin
MIN_ROOMS=1.5
MAX_RENT=1200
ONLY_PERMANENT_CONTRACTS=true
```

You can then run the container with:

```shell
docker run --env-file /path/to/your/env/file
```
