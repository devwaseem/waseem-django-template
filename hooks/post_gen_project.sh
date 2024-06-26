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

mkdir dist

git init -b main
git add .

# poetry run pre-commit install

# echo "Linting & Formatting..."
# just lint

# echo "Checking type errors..."
# just type

git add .
git commit -m "Intial Commit"

# Customize the env file before proceeding
nvim .env

echo "Setup Complete..."

# if [[ $? -eq 0 ]];
# then
#   just up
#   just makemigrations
#   just migrate
#   if [[ $? -eq 0 ]];
#   then
#     echo "Setup Complete..."
#   fi
# fi
