#!/bin/bash

# Make migrations
echo "Making migrations"
alembic upgrade head
echo "Migrations done"

# populate db
echo "Populating db"
python -m scripts.populate_db_real
