import pytest
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError, WriteError
from wg_gesucht.items import FlatItem
from wg_gesucht.pipelines import WgGesuchtPipeline


@pytest.fixture
def db_pipeline() -> WgGesuchtPipeline:
    # Set up the pipeline with a real MongoDB connection
    connection_uri = "mongodb://root:admin@host.docker.internal:27017"
    db_name = "test_db"
    collection_name = "test_collection"

    pipeline = WgGesuchtPipeline(connection_uri, db_name, collection_name)
    yield pipeline

    # Clean up after the tests
    pipeline._client.drop_database(db_name)
    pipeline._client.close()


def test_init_with_valid_connection():
    """Mongo Instance has to be running for this"""
    pipeline = WgGesuchtPipeline(
        connection_uri="mongodb://root:admin@host.docker.internal:27017",
        db_name="flats",
    )
    assert isinstance(pipeline, WgGesuchtPipeline)


def test_init_with_invalid_connection(mocker):
    """Mongo Instance has to be running for this"""
    with mocker.patch(
        "wg_gesucht.pipelines.Database.command",
        side_effect=ServerSelectionTimeoutError(),
    ):
        with pytest.raises(ValueError):
            WgGesuchtPipeline(
                connection_uri="mongodb://root:admin@somehost:27017",
                db_name="flats",
            )


def test_init_misisng_settings():
    with pytest.raises(ConfigurationError):
        WgGesuchtPipeline(connection_uri="", db_name="")


def test_check_database_connection_success(db_pipeline: WgGesuchtPipeline):
    db_pipeline._check_database_connection(db_pipeline._client)


def test_process_item(db_pipeline: WgGesuchtPipeline):
    """Asserts that an item is inserted into the database."""
    item = FlatItem()
    item["id"] = 123
    item["title"] = "What a nice flat"

    processed_item = db_pipeline.process_item(item, None)

    # Assert the processed item is returned unchanged
    assert processed_item == item

    # Assert the item is inserted into the collection
    document = db_pipeline._collection.find_one({"id": item["id"]})
    assert document["title"] == "What a nice flat"


def test_item_only_persisted_once(db_pipeline: WgGesuchtPipeline):
    """Asserts that an item is only inserted once into the database."""
    item: FlatItem = FlatItem()
    item["id"] = 123
    item["title"] = "What a nice flat"

    processed_item = db_pipeline.process_item(item, None)
    processed_item = db_pipeline.process_item(item, None)
    processed_item = db_pipeline.process_item(item, None)
    processed_item = db_pipeline.process_item(item, None)

    assert processed_item == item

    assert db_pipeline._collection.count_documents({}) == 1
    document = db_pipeline._collection.find_one({"id": item["id"]})
    assert document["title"] == "What a nice flat"


def test_persistence_error(db_pipeline: WgGesuchtPipeline, mocker):
    """Asserts that error is logged when persistence fails."""
    item: FlatItem = FlatItem()
    item["id"] = 123
    item["title"] = "What a nice flat"

    with mocker.patch(
        "wg_gesucht.pipelines.Collection.insert_one",
        return_value=WriteError(error="something failed"),
    ):
        db_pipeline.process_item(item, None)

    assert db_pipeline._collection.count_documents({}) == 0
