#!/bin/bash

# Load environment variables from .env file
if [ -f "../../.env" ]; then
    export $(cat ../../.env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found in the root directory"
    exit 1
fi

OUTPUT_PATH="../app/models/models.py"

# Debug: Print connection information
echo "Debug - Database connection parameters:"
echo "Host: $POSTGRES_HOST"
echo "Port: $POSTGRES_PORT"
echo "User: $POSTGRES_USER"
echo "Database: $POSTGRES_DB"
echo "Schema: $POSTGRES_SCHEMA"

# Test database connection
echo "Testing database connection..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt" || {
    echo "❌ Failed to connect to database"
    exit 1
}

# Executa o sqlacodegen com um patch para a função version, evitando o erro com 'citext'
echo "Generating models..."
python -c "import importlib.metadata as md; orig = md.version; md.version = lambda dist: 'unknown' if dist=='citext' else orig(dist); from sqlacodegen.cli import main; import sys; sys.exit(main())" \
  postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB --schema=$POSTGRES_SCHEMA --outfile=$OUTPUT_PATH

# Check if models were generated
if [ -s "$OUTPUT_PATH" ]; then
    echo "✅ Models generated successfully at $OUTPUT_PATH"
else
    echo "❌ No models were generated. The output file is empty."
    exit 1
fi
