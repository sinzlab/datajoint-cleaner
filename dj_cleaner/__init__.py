"""Initialize package."""
from pathlib import Path

from .adapters import FACADE_CONFIGS
from .adapters.minio_gateway import MinIOGateway
from .adapters.pymysql_gateway import PyMySQLGateway
from .adapters.toml_controller import TOMLController
from .frameworks.minio_facade import MinIOFacade, MinIOFacadeConfig
from .frameworks.pymysql_facade import PyMySQLFacade, PyMySQLFacadeConfig
from .frameworks.toml_facade import TOMLFacade
from .use_cases.clean import Clean

minio_facade = MinIOFacade()
minio_gateway = MinIOGateway(facade=minio_facade)
pymysql_facade = PyMySQLFacade()
pymysql_gateway = PyMySQLGateway(facade=pymysql_facade)
clean_use_case = Clean(db_gateway=pymysql_gateway, external_gateway=minio_gateway)
toml_facade = TOMLFacade(Path("datajoint-cleaner.toml"))
controller = TOMLController(facade=toml_facade, use_cases={"clean": clean_use_case})
FACADE_CONFIGS["database"] = PyMySQLFacadeConfig
FACADE_CONFIGS["minio"] = MinIOFacadeConfig
