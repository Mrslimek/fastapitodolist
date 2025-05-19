#!/bin/sh

uv run alembic revision --autogenerate -m "init migration"
uv run alembic upgrade head

exec "$@"
