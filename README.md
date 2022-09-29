# AC41004-Backend
Industrial Team Project - Backend


## TOML configuration
Create a `config.toml` in the `app` folder with the following keys and values

```toml
# Config File
mongo_uri = ""  # MongoDB Connection URI
db_name = ""  # DB name for dev purposes
redis_uri = ""  # URI for redis, can be ignored for docker compose deployment
session_secret = ""  # a LONG session secret key
debug = true  # If to launch app in debug mode
```

