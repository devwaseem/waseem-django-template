#!/bin/sh

set -o errexit
set -o nounset
set -o pipefail

# Give execution permissions
chmod +x ./scripts/local/backup
chmod +x ./scripts/local/restore
chmod +x ./scripts/local/up
chmod +x ./scripts/local/upx

cp env_template.txt .env

# Install python dependencies
poetry install --no-root

# Install node dependencies
npm install

mkdir -p dist

git init -b main
git add .

# poetry run pre-commit install

git add .
git commit -m "Intial Commit"

# Customize the env file before proceeding
nvim .env

echo "Setup Complete..."

cd {{cookiecutter.project_name}}
