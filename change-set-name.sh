#!/bin/bash
#This script changes the media players screen_set_name from local db.

#!/bin/bash

# Database Configuration
DB_USER="root"  
DB_PASSWORD="root"  
DB_NAME="switchboard"  
SCREEN_SET_TABLE="screen_set"  
CHANNEL_TABLE="channel" 
QUERY_CHANNEL_ID="SELECT id FROM channel;"

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


# Test database connection
mysql -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "SELECT 1" &>/dev/null

# If the connection fails, exit with an error message
if [ $? -ne 0 ]; then
    echo "Error: Unable to connect to the MySQL database. Please check your credentials and database settings."
    exit 1
fi

echo "Connected to MySQL database successfully."

#get data from the channel table to see what channels has the location added
CHANNEL_ID_DATA=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "$QUERY_CHANNEL_ID")
#CHANNEL_DATA=$(mysql -u root -proot -D switchboard -e "SELECT * FROM channel;")
#echo "IDs of the channels available in the location $CHANNEL_ID_DATA"

# Check if the query returned any data (excluding the header)
CHANNEL_ID_DATA_NO_HEADER=$(echo "$CHANNEL_ID_DATA" | tail -n +2) #remove header.

if [[ -z "$CHANNEL_ID_DATA_NO_HEADER" ]]; then
    echo "No channel IDs found."
    exit 0 #Exit No channels added to this location. No need to change anything.
fi

#pending: REVIEW IF HEAD IS PRESENT IN TABLE EVEN IF NO VALUE HAVE BEEN ADDED

#echo "Raw CHANNEL_ID_DATA:"
echo "$CHANNEL_ID_DATA" 


# Remove the header (header will always be there, data might not)
CHANNEL_ID_DATA=$(echo "$CHANNEL_ID_DATA" | tail -n +2)
echo "$CHANNEL_ID_DATA" 





#CHANNEL_DATA is a string, we need to change iot to an array
#using newline as the delimiter
IFS=$'\n' read -rd '' -a CHANNEL_ID_ARRAY <<< "$CHANNEL_ID_DATA"


# Remove any empty elements (due to potential extra whitespace)
CHANNEL_ID_ARRAY=("${CHANNEL_ID_ARRAY[@]}")




# Iterate through the array
for id in "${CHANNEL_ID_ARRAY[@]}"; do
  # Remove leading and trailing whitespace from each ID
  id=$(echo "$id" | tr -d '[:space:]')
  if [[ -n "$id" ]]; then #check if the id is not empty.
    #echo "Channel ID: $id present in location"
    # Perform actions with each ID here
  fi
done

echo "Element at index 0: ${CHANNEL_ID_ARRAY[0]}"