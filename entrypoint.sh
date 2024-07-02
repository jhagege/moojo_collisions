#!/bin/sh

# Set the port from the PORT environment variable, default to 8000
PORT=${PORT:-8000}

# Run the Uvicorn server
uvicorn app:app --host 0.0.0.0 --port $PORT
