#!/bin/bash

# Connection variables - change as needed
DB_NAME="ai_assistant_db"
DB_USER="ai_assistant_user"
DB_PASS="ai_assistant_pass"
DB_HOST="localhost"
DB_PORT="5432"

# Check if psql is installed
if ! command -v psql &> /dev/null
then
    echo "psql is not installed or not in PATH. Please install PostgreSQL or add psql to your PATH."
    exit 1
fi

# Create user and database
echo "Creating PostgreSQL user and database..."

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1 || \
psql -U postgres -c "CREATE DATABASE ${DB_NAME};"

psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
psql -U postgres -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';"

psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

echo "Database and user created successfully."

# Create or update .env file for Strapi
ENV_FILE="backend/my-strapi-app/.env"

echo "Setting up Strapi .env file at $ENV_FILE ..."

cat > $ENV_FILE << EOL
DATABASE_HOST=${DB_HOST}
DATABASE_PORT=${DB_PORT}
DATABASE_NAME=${DB_NAME}
DATABASE_USERNAME=${DB_USER}
DATABASE_PASSWORD=${DB_PASS}
EOL

echo ".env file configured."

echo "Done! You can now run Strapi with 'npm run develop' inside backend/my-strapi-app"
