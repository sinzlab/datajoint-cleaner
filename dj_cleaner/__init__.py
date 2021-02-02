"""Initialize package."""
from typing import Dict

from .adapters.controller import Controller
from .adapters.minio_gateway import MinIOGateway
from .adapters.pymysql_gateway import PyMySQLGateway
from .frameworks.minio_facade import MinIOFacade
from .frameworks.pymysql_facade import PyMySQLFacade
from .use_cases.clean import Clean

config: Dict[str, str] = {}
minio_facade = MinIOFacade(config)
minio_gateway = MinIOGateway(facade=minio_facade, config=config)
pymysql_facade = PyMySQLFacade(config)
pymysql_gateway = PyMySQLGateway(facade=pymysql_facade, config=config)
clean_use_case = Clean(db_gateway=pymysql_gateway, external_gateway=minio_gateway)
controller = Controller(config=config, use_cases={"clean": clean_use_case})
