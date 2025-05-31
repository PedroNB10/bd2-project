#!/bin/bash

# Load environment variables from .env file
if [ -f "../../.env" ]; then
    export $(cat ../../.env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found in the root directory"
    exit 1
fi

# Create backup directory if it doesn't exist
BACKUP_DIR="../backup"
mkdir -p $BACKUP_DIR

# Generate timestamp for the backup file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_${POSTGRES_DB}_${TIMESTAMP}.sql"

# Debug: Print connection information
echo "Debug - Database connection parameters:"
echo "Host: $POSTGRES_HOST"
echo "Port: $POSTGRES_PORT"
echo "User: $POSTGRES_USER"
echo "Database: $POSTGRES_DB"
echo "Schema: $POSTGRES_SCHEMA"

# Generate the backup using pg_dump
echo "Generating backup..."
PGPASSWORD=$POSTGRES_PASSWORD pg_dump \
    -h $POSTGRES_HOST \
    -p $POSTGRES_PORT \
    -U $POSTGRES_USER \
    -d $POSTGRES_DB \
    -F p \
    -f $BACKUP_FILE

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "✅ Database backup created successfully at $BACKUP_FILE"
else
    echo "❌ Error creating database backup"
    exit 1
fi 