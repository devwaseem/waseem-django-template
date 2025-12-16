#!/bin/sh

set -o errexit
set -o nounset
set -o pipefail

cp env_template.txt .env

# Install python dependencies
uv lock

# Install node dependencies
npm install

mkdir -p dist

git init -b main
git add .

# uv run pre-commit install

git add .
git commit -m "Initial Commit"

echo "Setup Complete..."
