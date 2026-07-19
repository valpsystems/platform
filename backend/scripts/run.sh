#!/bin/bash
# VALP SYSTEMS Backend - Run Script
# Usage: ./scripts/run.sh [dev|prod]

set -e

ENV=${1:-dev}

echo "Starting VALP SYSTEMS Backend ($ENV mode)"

if [ "$ENV" = "dev" ]; then
    export APP_ENV=development
    export APP_DEBUG=true
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
elif [ "$ENV" = "prod" ]; then
    export APP_ENV=production
    export APP_DEBUG=false
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo "Usage: ./scripts/run.sh [dev|prod]"
    exit 1
fi
