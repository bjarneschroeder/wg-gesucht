import pytest
from wg_gesucht.db_settings import DatabaseSettings


class TestDatabaseSettings:
    def test_db_name_wrong_type(self):
        with pytest.raises(TypeError):
            DatabaseSettings(
                db_name=1,
                connection_uri="mongodb://localhost:27017",
            )

    def test_db_name_empty(self):
        with pytest.raises(ValueError):
            DatabaseSettings(
                db_name="",
                connection_uri="mongodb://localhost:27017",
            )

    def test_db_name_none(self):
        with pytest.raises(ValueError):
            DatabaseSettings(
                db_name=None,
                connection_uri="mongodb://localhost:27017",
            )

    def test_connection_uri_wrong_type(self):
        with pytest.raises(TypeError):
            DatabaseSettings(
                db_name="wg_gesucht",
                connection_uri=1,
            )

    def test_connection_uri_empty(self):
        with pytest.raises(ValueError):
            DatabaseSettings(
                db_name="wg_gesucht",
                connection_uri="",
            )

    def test_connection_uri_none(self):
        with pytest.raises(ValueError):
            DatabaseSettings(
                db_name="wg_gesucht",
                connection_uri=None,
            )

    def test_db_settings(self):
        settings: DatabaseSettings = DatabaseSettings(
            db_name="wg_gesucht",
            connection_uri="mongodb://localhost:27017",
        )

        assert settings.db_name == "wg_gesucht"
        assert settings.connection_uri == "mongodb://localhost:27017"
