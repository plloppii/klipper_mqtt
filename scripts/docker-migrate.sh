#!/bin/bash

echo "Applying alembic migrations"
# Run alembic migrations
alembic upgrade heads
