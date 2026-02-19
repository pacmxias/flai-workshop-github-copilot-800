#!/bin/bash
# Django setup script

set -e

cd /workspaces/flai-workshop-github-copilot-800

echo "Step 1: Running makemigrations..."
octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py makemigrations

echo "Step 2: Running migrate..."
octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py migrate

echo "Step 3: Populating database..."
octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py populate_db

echo "Setup complete!"
