# datajoint-cleaner
![Test](https://github.com/cblessing24/datajoint-cleaner/workflows/Test/badge.svg)
![Black](https://github.com/cblessing24/datajoint-cleaner/workflows/Black/badge.svg)

## Configuration
The cleaner will look for a TOML file called `datajoint-cleaner.toml` in the current working directory to configure itself. The configuration file must have two top-level tables called `database_servers` and `storage_servers` and an array of tables called `cleaning_runs`. 

### Specifying Database Servers
Database servers are specified in the top-level `database_servers` table. Each key in the table corresponds to a distinct database server. The value of each key must be a table that contains the following keys: `host`, `user` and `password`.

The values of the `host`, `user` and `password` keys correspond to the host name of the database server, the name of a user present on said server and the password of said user, respectively.

Example:
```
[database_servers.my_db_server]
host = "192.156.3.65"
user = "me"
password = "mypassword"
```

### Specifying Storage Servers
Storage servers are specified in a sub-table of the `storage_servers` table based on their kind. Currently only MinIO servers are supported which are specified in the `minio` sub table. The keys necessary to specify a MinIO server are `endpoint`, `access_key`, `secret_key` and `secure`.

The values of these keys correspond to the endpoint of the MinIO server, your access and private key and whether a secure connection should be established or not, respectively.

Example:
```
[storage_servers.minio.my_minio_server]
endpoint = "192.543.5.61"
access_key = "my_access_key"
secret_key = "my_secret_key"
secure = true
```

### Specifying Cleaning Runs
Individual cleaning runs are specified in the top-level array of tables called `cleaning_runs`. Each table in the array corresponds to a distinct cleaning run and must have the following keys:

* `database_server`: Name of a database server specified in the `database_servers` table
* `schema`: Name of a schema on said database server
* `store`: Name of a DataJoint store for which an external table exists in said schema
* `storage_server`: A storage server specified in the `storage_servers` table in the `<kind>.<name>` format
* `bucket`: Name of a bucket on said MinIO server
* `location`: Location of externally stored objects in said bucket

Example:
```
[[cleaning_runs]]
database_server = "my_db_server"
schema = "my_schema"
store = "my_store"
storage_server = "minio.my_minio_server"
bucket = "my_bucket"
location = "my_location"
```