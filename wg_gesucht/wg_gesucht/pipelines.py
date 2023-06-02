# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from typing import Optional

from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError, WriteError
from wg_gesucht.db_settings import DatabaseSettings
from wg_gesucht.items import FlatItem


class WgGesuchtPipeline:
    _client: MongoClient
    _database: Database
    _collection: Collection

    @classmethod
    def from_crawler(cls, crawler):
        db_settings: Optional[DatabaseSettings] = crawler.settings.get("DB_SETTINGS")
        if not db_settings:
            raise ValueError("DB_SETTINGS must be set in settings.py")

        return cls(
            connection_uri=db_settings.connection_uri, db_name=db_settings.db_name
        )

    def __init__(
        self, connection_uri: str, db_name: str, collection_name: str = "flats"
    ):
        self._client = MongoClient(connection_uri, timeoutMS=10000)
        self._check_database_connection(client=self._client)

        self._database = self._client[db_name]
        self._collection = self._database[collection_name]
        self._collection.create_index("id", name="flat_id", unique=True)

    def _check_database_connection(self, client: MongoClient):
        try:
            logging.info("Pinging database to check connection.")
            client.admin.command("ping")
        except ServerSelectionTimeoutError:
            raise ValueError(
                "Failed to connect to database. "
                "Please check given connection parameters."
            )

    def process_item(self, item: FlatItem, spider):
        try:
            self._collection.insert_one(ItemAdapter(item).asdict())
        except WriteError as e:
            if e.code == 11000:
                logging.info("Found duplicate flat id: %s", item["id"])
            else:
                logging.error("Encountered unexpected error while persisting flat:", e)

        return item
