function query_channel_data {

CHANNEL_ID_DATA=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" -e "$QUERY_CHANNEL_ID")
echo "with header: $CHANNEL_ID_DATA"

#remove header
CHANNEL_ID_DATA=$(echo "$CHANNEL_ID_DATA" | tail -n +2)
echo "without header: $CHANNEL_ID_DATA"

#check is channel table returned any data
if [[ -z "$CHANNEL_ID_DATA" ]]; then
    echo "No channels found in store. No changes needed to be made"
    exit 0 #Exit 
fi

#CHANNEL_DATA is a string, we need to change it to an array using newline as the delimiter
IFS=$'\n' read -rd '' -a CHANNEL_ID_ARRAY <<< "$CHANNEL_ID_DATA"
echo "array of values: ${CHANNEL_ID_ARRAY[@]}"

# Remove any empty elements (due to potential extra whitespace)
CHANNEL_ID_ARRAY=("${CHANNEL_ID_ARRAY[@]}")
echo "Store has the following solutions: ${CHANNEL_ID_ARRAY[@]}"
}

function iterate {
# Iterate through the array
for id in "${CHANNEL_ID_ARRAY[@]}"; do
  # Remove leading and trailing whitespace from each ID
  id=$(echo "$id" | tr -d '[:space:]')
  if [[ -n "$id" ]]; then #check if the id is not empty.
    query_screen_set_with_channel_id $id
    
  fi
done
}