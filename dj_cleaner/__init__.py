"""Initialize package."""
from pathlib import Path
from typing import Dict

from .adapters.minio_gateway import MinIOGateway
from .adapters.pymysql_gateway import PyMySQLGateway
from .adapters.toml_controller import TOMLController
from .frameworks.minio_facade import MinIOFacade
from .frameworks.pymysql_facade import PyMySQLFacade
from .frameworks.toml_facade import TOMLFacade
from .use_cases.clean import Clean

config: Dict[str, str] = {}
minio_facade = MinIOFacade(config)
minio_gateway = MinIOGateway(facade=minio_facade, config=config)
pymysql_facade = PyMySQLFacade(config)
pymysql_gateway = PyMySQLGateway(facade=pymysql_facade, config=config)
clean_use_case = Clean(db_gateway=pymysql_gateway, external_gateway=minio_gateway)
toml_facade = TOMLFacade(Path("datajoint-cleaner.toml"))
controller = TOMLController(facade=toml_facade, config=config, use_cases={"clean": clean_use_case})
