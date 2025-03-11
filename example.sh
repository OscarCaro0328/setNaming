#!/bin/bash

# Database Configuration
DB_HOST="localhost"      # Change if using a remote database
DB_USER="your_username"  # Replace with your MySQL username
DB_PASSWORD="your_password"  # Replace with your MySQL password
DB_NAME="your_database"  # Replace with your database name
TABLE_NAME="your_table"  # Replace with your table name
COLUMN_NAME="screen_set_name"  # Replace with your column name

# Define the screen set mappings (oldValue -> newValue)
declare -A screenSetsToUpdate=(
    ["L1"]="Lane 1"
    ["L2"]="Lane 2"
    ["L3"]="Lane 3"
    ["L4"]="Lane 4"
)

# Test database connection
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "SELECT 1" &>/dev/null

# If the connection fails, exit with an error message
if [ $? -ne 0 ]; then
    echo "Error: Unable to connect to the MySQL database. Please check your credentials and database settings."
    exit 1
fi

echo "Connected to MySQL database successfully."

# Loop through each mapping and update the database
for oldValue in "${!screenSetsToUpdate[@]}"; do
    newValue="${screenSetsToUpdate[$oldValue]}"

    SQL_QUERY="UPDATE $TABLE_NAME SET $COLUMN_NAME = '$newValue' WHERE $COLUMN_NAME = '$oldValue';"

    # Execute the MySQL command
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "$SQL_QUERY"

    # Check if the command executed successfully
    if [ $? -eq 0 ]; then
        echo "Updated '$oldValue' to '$newValue' successfully."
    else
        echo "Error updating '$oldValue' to '$newValue'."
    fi
done

echo "Database update completed."