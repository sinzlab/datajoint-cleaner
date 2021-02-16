"""A tool for cleaning up external DataJoint stores."""
from .adapters.minio_gateway import MinIOGateway
from .adapters.pymysql_gateway import PyMySQLGateway
from .adapters.toml_controller import TOMLController
from .frameworks.minio_facade import MinIOFacade
from .frameworks.pymysql_facade import PyMySQLFacade
from .frameworks.toml_cli import TOMLCLI
from .use_cases.clean import Clean

minio_facade = MinIOFacade()
minio_gateway = MinIOGateway(facade=minio_facade)
pymysql_facade = PyMySQLFacade()
pymysql_gateway = PyMySQLGateway(facade=pymysql_facade)
clean_use_case = Clean(db_gateway=pymysql_gateway, external_gateway=minio_gateway)
toml_controller = TOMLController(use_cases={"clean": clean_use_case})
toml_cli = TOMLCLI(toml_controller)
