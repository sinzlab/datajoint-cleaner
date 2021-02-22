# DataJoint-Cleaner

![Test](https://github.com/cblessing24/datajoint-cleaner/workflows/Test/badge.svg)
![Black](https://github.com/cblessing24/datajoint-cleaner/workflows/Black/badge.svg)
![Mypy](https://github.com/cblessing24/datajoint-cleaner/workflows/Mypy/badge.svg)
![Build](https://github.com/cblessing24/datajoint-cleaner/workflows/Build/badge.svg)

DataJoint-Cleaner is a tool used to clean external [DataJoint](https://datajoint.io/) [stores](https://docs.datajoint.io/python/admin/5-blob-config.html?highlight=external).

## How It Works

The user provides information pointing to a particular external table and external store combination. Using this information DataJoint-Cleaner will delete all objects in the external store that have no corresponding entry in the external table, thus freeing storage space.

## Important Considerations

The creation of a backup is highly recommended before using DataJoint-Cleaner to avoid a potential loss of data due to an user error or a bug.

DataJoint-Cleaner should not be used to clean external stores that are used by multiple database servers or multiple storage protocols (e.g. file & s3). If done so it could potentially delete objects that are still referenced in the database.

## Installation

### Recommended installation method

To avoid messing up the system Python environment, the most recommended way to install DataJoint-Cleaner is via [pipx](https://pypi.org/project/pipx/):

```bash
pipx install datajoint-cleaner
```

### Other installation methods

Install DataJoint-Cleaner into user site with `pip`:

```bash
pip install --user datajoint-cleaner
```

## Configuration

DataJoint-Cleaner will look for a TOML file called `datajoint-cleaner.toml` in the current working directory (by default) to configure itself. The configuration file must have two top-level tables called `database_servers` and `storage_servers` and an array of tables called `cleaning_runs`.

### Specifying Database Servers

Database servers are specified in the top-level `database_servers` table. Each key in the table corresponds to a distinct database server. The value of each key must be a table that contains the following keys: `host`, `user` and `password`.

The values of the `host`, `user` and `password` keys correspond to the host name of the database server, the name of a user present on said server and the password of said user, respectively.

Example:

```toml
[database_servers.my_db_server]
host = "192.156.3.65"
user = "me"
password = "mypassword"
```

### Specifying Storage Servers

Storage servers are specified in a sub-table of the `storage_servers` table based on their kind. Currently only MinIO servers are supported which are specified in the `minio` sub table. The keys necessary to specify a MinIO server are `endpoint`, `access_key`, `secret_key` and `secure`.

The values of these keys correspond to the endpoint of the MinIO server, your access and private key and whether a secure connection should be established or not, respectively.

Example:

```toml
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

```toml
[[cleaning_runs]]
database_server = "my_db_server"
schema = "my_schema"
store = "my_store"
storage_server = "minio.my_minio_server"
bucket = "my_bucket"
location = "my_location"
```

## Usage

The cleaning process can be started like so:

```bash
dj-cleaner
```

The command above will execute all cleaning runs defined in the configuration file. The `--config-file` option can be used to pass a custom path to a configuration file to DataJoint-Cleaner:

```bash
dj-cleaner --config-file /path/to/config/file
```
