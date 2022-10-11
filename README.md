# AC41004-Backend
Industrial Team Project - Backend

## Prerequisites
You'll need a few external services are needed for this application

- Python 3.9
- MongoDB hosted via MongoDB Cloud
- Redis

## MongoDB Database
This project makes use of MongoDB Atlas' cloud search index functionality to be able to search through the `resoruces`
database. You can set up a DB via [MongoDB Cloud Here](https://www.mongodb.com/).

### Search Index
You will need to set up a search index with the following json on the `resources` with the index name `resourceSearch`
table for Resource searching to be able to function correctly.

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "metadata": {
        "fields": {
          "Name": [
            {
              "dynamic": true,
              "type": "document"
            },
            {
              "type": "string"
            }
          ],
          "Tags": {
            "fields": {
              "Value": [
                {
                  "dynamic": true,
                  "type": "document"
                },
                {
                  "type": "string"
                }
              ]
            },
            "type": "document"
          }
        },
        "type": "document"
      },
      "name": [
        {
          "dynamic": true,
          "type": "document"
        },
        {
          "type": "string"
        }
      ],
      "reference": [
        {
          "dynamic": true,
          "type": "document"
        },
        {
          "type": "string"
        }
      ]
    }
  }
}
```

## TOML configuration
Create a `config.toml` with the following keys and values to start the application.

*You may need to place the `config.toml` file in the `app` directory to run during development.*

```toml
# Config File
mongo_uri = ""  # MongoDB Connection URI
db_name = ""  # DB name for dev purposes
redis_uri = ""  # URI for redis, can be ignored for docker compose deployment
session_secret = ""  # a LONG session secret key
debug = true  # If to launch app in debug mode
```

## Deployment 
We recommend you use the provided `DOCKERFILE` to set up this application as a Docker container to deploy using a tool 
such as [Terraform](https://www.terraform.io/).

### Dev deployment via Docker Compose
**This method not recommended for large scale deployment**

Another option for basic deployment is using the provided `docker-compose.yml` file and deploying via Docker Compose.
The docker compose file contains configuration to start up a Redis DB, Traefik as a reverse proxy and the backend
application itself.

To do this, edit the docker compose file with the appropriate `Host` address. You'll also need to configure `traefik` 
commands to your needs, such as providing a `.env` file with your Cloudflare API keys to configure an SSL cert.

