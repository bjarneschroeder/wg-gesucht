import logging
from dataclasses import dataclass

logger = logging.getLogger()


@dataclass
class DatabaseSettings:
    db_name: str
    connection_uri: str

    def __init__(
        self,
        connection_uri: str,
        db_name: str,
    ):
        self._validate_init_params(
            db_name=db_name,
            connection_uri=connection_uri,
        )
        self.db_name = db_name
        self.connection_uri = connection_uri

    def _validate_init_params(
        self,
        db_name: str,
        connection_uri: str,
    ):
        if not db_name:
            raise ValueError("db_name must be set")

        if not isinstance(db_name, str):
            raise TypeError("db_name must be of type str")

        if not connection_uri:
            raise ValueError("connection_uri must be set")

        if not isinstance(connection_uri, str):
            raise TypeError("connection_uri must be of type str")


def load_db_settings(
    connection_uri: str,
    db_name: str,
) -> DatabaseSettings:
    try:
        return DatabaseSettings(
            db_name=db_name,
            connection_uri=connection_uri,
        )
    except (ValueError, TypeError) as e:
        logger.error("Failed to load database settings. Please check input.")
        logger.error(f"Error: {e}")
        raise e
