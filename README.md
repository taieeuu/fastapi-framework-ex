## Continually updated

## Usage Instructions

1. Rename .env.example to .env by removing the .example suffix.
2. Fill in the relevant parameters in the `.env` file.

## Parameter Description

- APP_ENV: Represents the environment. Options include:
  - dev: Development environment
  - prod: Production environment
  - uat: Testing environment

## USAGE
First: create app_network

```zsh
docker network create --driver bridge --subnet=<subnet>/24  --gateway=<gateway_ip> app-network
```

Second: build and up docker-compose
```shell
docker-compose -f docker-compose.base.yml -f docker-compose.v1.yml build
```

```shell
docker-compose -f docker-compose.base.yml -f docker-compose.v1.yml up
```
