FROM python:3.11

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./wg_gesucht /app/
WORKDIR /app

CMD scrapy crawl wg_gesucht
