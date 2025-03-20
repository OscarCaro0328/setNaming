#!/bin/bash

# Database Configuration
DB_HOST="localhost"      # Change if using a remote database
DB_USER="your_username"  # Replace with your MySQL username
DB_PASSWORD="your_password"  # Replace with your MySQL password
DB_NAME="your_database"  # Replace with your database name
TABLE_NAME="your_table"  # Replace with your table name
COLUMN_NAME="screen_set_name"  # Replace with your column name

: <<'END_COMMENT'
1	" Drive Thru - Vertical - 2"
3	" Coates-System"
4	" DT Presell - Vertical"
5	" Front Counter - Horizontal - 4"
6	" Walk Up Window - Vertical - 1"
7	" Walk Up Window - Vertical - 2"
8	" Front Counter BR - Horizontal -4- Combo"
9	" Order Status Board - Horizontal - 1"
10	" Front Counter - Vertical - 3"
11	" Front Counter - Vertical - 4"
12	" Front Counter - Horizontal - 3"
15	" Front Counter BR - Horizontal -4- Standalone"
19	" Front Counter - Horizontal - 2"
20	" Front Counter - Vertical - 2"
29	" Int Promo - Vertical"
30	" Front Counter - Horizontal - 5"
31	" Drive Thu - Vertical - Single Panel - Non-OT"
32	" Int Promo - Horizontal"
33	" Ext Promo - Vertical"
34	" Ext Promo - Horizontal"
35	" Front Counter - Horizontal - 1"
37	" FC BR - H - 1"
38	" DT BR - V - 2"
42	" FC BR Combo - H - 2"
43	" FC BR Combo - H - 3"
44	" FC BR Standalone - H - 3"
END_COMMENT
                                    

                  


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