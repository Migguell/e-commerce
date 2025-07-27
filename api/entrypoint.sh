#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Initialize migrations directory if it doesn't exist
if [ ! -d "migrations" ]; then
  echo "Initializing migrations directory..."
  flask db init
fi

# Run migrations
echo "Running database migrations..."
flask db migrate -m "Initial migration." || echo "No changes to migrate."
flask db upgrade

# Execute the command passed to this script (e.g., python app.py)
exec "$@"