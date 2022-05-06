#!/bin/bash

# Run alembic migrations
alembic upgrade heads

# Start Python application
uvicorn app.main:app --host 0.0.0.0 --port 8000