"""Initialize package."""
from typing import Dict

from .clean import Clean
from .minio_facade import MinIOFacade
from .minio_gateway import MinIOGateway
from .pymysql_facade import PyMySQLFacade
from .pymysql_gateway import PyMySQLGateway

config: Dict[str, str] = {}
minio_facade = MinIOFacade(config)
minio_gateway = MinIOGateway(facade=minio_facade, config=config)
pymysql_facade = PyMySQLFacade(config)
pymysql_gateway = PyMySQLGateway(facade=pymysql_facade, config=config)
clean_use_case = Clean(config=config, db_gateway=pymysql_gateway, external_gateway=minio_gateway)
