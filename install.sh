#!/bin/bash
# JAM Mission Installer
#
# This script bootstraps the Django environment for the JAM Mission
# website on a Linux host.  It creates a Python virtual environment,
# installs dependencies, applies migrations and collects static files.
# Run this script from the root of the project: ./install.sh

set -e

if [ ! -f requirements.txt ]; then
  echo "Please run this script from the root of the JAM Mission project where requirements.txt exists."
  exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying database migrations..."
python backend/manage.py migrate

echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

echo "Setup complete."
echo "To start the development server, run:\nsource venv/bin/activate && python backend/manage.py runserver"