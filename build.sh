#!/bin/bash

# Exit on error
set -e

# Install dependencies
pip install -r config/requirements.txt

# Run migrations
python config/manage.py migrate

# Collect static files
python config/manage.py collectstatic --noinput

echo "✅ Build completed successfully!"
