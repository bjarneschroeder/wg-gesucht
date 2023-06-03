# WG-Gesucht Spider

This repository contains a scrapy project for scraping the german real estate website wg-gesucht.de.

May it help you maybe to find a flat really fast or to build a cool dataset.

**Please use the spider responsibly,
keep requests to a minimum.
No one likes bot traffic.**

---

## Scope and limitations of the project

Currently found flats will just be stored by the pipeline
in a MongoDB.
Also the scraper only collects individual flat offers,
no shared apartments.

Only the first site is processed.
The scraper is thought to be scheduled more frequently,
so one gets notified earlier when flats are available.

---

## Possible Settings and Starting the Spider

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

#### Database Connection Info

`DB_NAME`: Mandatory `str`.
Name off the database that will be created in the
given Mongo Cluster.

`DB_URI`: MongoDB Connection URI.
See [here](https://www.mongodb.com/docs/manual/reference/connection-string/)
for how to build a compliant URI.

---

### Starting the spider

The spider can be started as a Docker container.
Search settings and database
connection info are given via the enviornment,
when starting the spider.

### Building the Docker Image

You can build the image with:

```shell
docker build -t wg_gesucht .
```

If you have no MongoDB instance running anywhere and maybe
just want to test out the spider.
You can spin up a MongoDB Docker instance using
the [`compose.yaml`](/compose.yaml) from this repo.

```shell
docker compose up -d
```

You can run your built image with:

```shell
docker run \
-e CITY_NAME=Berlin \
-e DB_NAME=wg-gesucht \
-e DB_URI=mongodb://root:admin@host.docker.internal:27017 \
wg_gesucht
```

**Note**: You have to provide a valid city name
and a database connection.
All other search parameters are optional.

For passing all paremeters you could also
use an environment file with the following structure:

```env
CITY_NAME=Berlin
MIN_ROOMS=1.5
MAX_RENT=1200
ONLY_PERMANENT_CONTRACTS=true
DB_NAME=flats
DB_URI=mongodb://root:admin@host.docker.internal:27017
```

You can then run the container with:

```shell
docker run --env-file /path/to/your/env/file wg_gesucht
```
