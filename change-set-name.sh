#!/bin/bash
#This script changes the media players screen_set_name from local db.

#!/bin/bash

# Database Configuration
DB_USER="root"  
DB_PASSWORD="root"  
DB_NAME="switchboard"  
SCREEN_SET_TABLE="screen_set"  
QUERY="SELECT * FROM screen_set ORDER BY id;"


# Initialize arrays
declare -a id_array
declare -a name_array
declare -a channel_id_array

declare -A channel_id_map
channel_name_map["1"]="DT DNK Combo - "
channel_name_map["4"]="DT DNK Presell - "
channel_name_map["5"]="FC DNK - "
channel_name_map["6"]="WUW DNK - "
channel_name_map["7"]="WUW DNK - "
channel_name_map["8"]="FC BR Combo - "
channel_name_map["9"]="OSB DNK - "
channel_name_map["10"]="FC DNK - "
channel_name_map["11"]="FC DNK - "
channel_name_map["12"]="FC DNK - "
channel_name_map["15"]="FC BR Standalone - "
channel_name_map["19"]="FC DNK - "
channel_name_map["20"]="FC DNK - "
channel_name_map["29"]="Int Promo DNK - "
channel_name_map["30"]="FC DNK - "
channel_name_map["31"]="DT DNK Non - "
channel_name_map["32"]="Int Promo DNK - "
channel_name_map["33"]="Ext Promo DNK - "
channel_name_map["34"]="Ext Promo DNK - "
channel_name_map["35"]="FC DNK - "
channel_name_map["37"]="FC BR - "
channel_name_map["38"]="DT BR - "
channel_name_map["42"]="FC BR Combo - "
channel_name_map["43"]="FC BR Combo - "
channel_name_map["44"]="FC BR Standalone - "





##----------------------- FUNCTIONS -----------------------------##



function test_db_connection {
# Test database connection
mysql -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "SELECT 1" &>/dev/null

# If the connection fails, exit with an error message
if [ $? -ne 0 ]; then
    echo "Error: Unable to connect to the MySQL database. Please check your credentials and database settings."
    exit 1
fi
echo "Connected to MySQL database successfully."
}

#

function query_screen_set {
local QUERY_RESULT=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "$QUERY")

# Remove the header row
local QUERY_RESULT=$(echo "$QUERY_RESULT" | tail -n +2)

# Check if there are any results
if [[ -z "$QUERY_RESULT" ]]; then
    echo "No data found in the table. Exiting since we got nothing to change here."
    exit 0
fi

echo "$QUERY_RESULT"
}



function process_query_results {
  local parameter="$1"
  local QUERY_RESULT="$parameter"
  # Process each row
while IFS=$'\t' read -r id name channel_id; do
    id_array+=("$id")
    name_array+=("$name")
    channel_id_array+=("$channel_id")
done <<< "$QUERY_RESULT"

# Print the arrays 
#echo "ID Array: ${id_array[@]}"
#echo "Name Array: ${name_array[@]}"
#echo "Channel ID Array: ${channel_id_array[@]}"

}





test_db_connection
data=$(query_screen_set)
#echo "this is the query preprocessing: $data"
process_query_results "$data"












# Example usage: Accessing related data
for i in "${!id_array[@]}"; do
    echo "Row ${i}: ID=${id_array[$i]}, Name=${name_array[$i]}, Channel ID=${channel_id_array[$i]}"
   if [[ "${channel_id_array[$i]}" -eq 1 ]]; then
    echo "Screen set belogs to a DT"
    # Add your code here to do something
   fi

done






