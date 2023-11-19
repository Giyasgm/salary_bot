# Salary Bot

## Description

Salary Bot is a Telegram bot designed to calculate and aggregate salaries based on input data.

## Setup and development

1. Install python 3.11.5
2. Create virtual environment with `poetry`
3. Install dependencies with `poetry install`
4. Run dev mongodb with docker compose `docker-compose -f compose-dev.yaml up -d`
5. Setup environment variables based on `.envrc.example` (i recommend to use `direnv` for this)
6. Run bot with `python -m salary_bot`

If you have database dump, you can restore it with `mongorestore` command.

```shell
mongorestore --authenticationDatabase=admin  --uri="mongodb://user:password@localhost:27017" --db=salaries_bot --collection=salaries /path/to/dump.bson
```

## Tests

TBD

## Deployment

TBD
