#!/usr/bin/env python3

import subprocess
import re

# Database Configuration
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "switchboard"
SCREEN_SET_TABLE = "screen_set"
QUERY = "SELECT * FROM screen_set ORDER BY id;"

SET_1 = " 1 "
SET_2 = " 2 "
FAILOVER = "Failover"
NOT_FAILOVER = ""

# Initialize lists
id_list = []
name_list = []
channel_id_list = []
failover_list = []



# Channel ID to Name mapping
channel_name_map = {
    "1": "DT DNK Combo -",
    "3": "Coates-System -",
    "4": "DT DNK Presell -",
    "5": "FC DNK -",
    "6": "WUW DNK -",
    "7": "WUW DNK -",
    "8": "FC BR Combo -",
    "9": "OSB DNK -",
    "10": "FC DNK -",
    "11": "FC DNK -",
    "12": "FC DNK -",
    "15": "FC BR Standalone -",
    "19": "FC DNK -",
    "20": "FC DNK -",
    "29": "Int Promo DNK -",
    "30": "FC DNK -",
    "31": "DT DNK Non -",
    "32": "Int Promo DNK -",
    "33": "Ext Promo DNK -",
    "34": "Ext Promo DNK -",
    "35": "FC DNK -",
    "37": "FC BR -",
    "38": "DT BR -",
    "42": "FC BR Combo -",
    "43": "FC BR Combo -",
    "44": "FC BR Standalone -",
}



# ----------------------- FUNCTIONS -----------------------------


def test_db_connection():
    """Tests the database connection using Bash."""
    try:
        command = f"mysql -u {DB_USER} -p'{DB_PASSWORD}' -D {DB_NAME} -e 'SELECT 1'"
        subprocess.run(command, shell=True, check=True, capture_output=True)
        print("Connected to MySQL database successfully.")
    except subprocess.CalledProcessError as e:
        print(
            f"Error: Unable to connect to the MySQL database. Please check your credentials and database settings. {e}"
        )
        exit(1)


def query_screen_set():
    """Queries the sql screen_set table using Bash .
    Returns: 
        all the values separated in rows without header 
         id | name            | channel_id |
        +----+-----------------+------------+
        |  1 | Lane 1          |          1 |

    """
    try:
        command = f"mysql -u {DB_USER} -p'{DB_PASSWORD}' -D {DB_NAME} -e '{QUERY}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        output = result.stdout.strip()  # Clear leading and trailing whitespaces
        lines = output.split("\n")[1:]  # Split lines and remove header
        
        if not lines:  # Check if empty
            print("No data found in the table. Exiting since we got nothing to change here.")
            exit(0)

        return lines  # Return list 
    except subprocess.CalledProcessError as e:
        print(f"Error executing MySQL command: {e}")
        return None


#takes the query results already separated in rows, and splits results in 3 lists
def process_query_results(query_result):
    """Processes the query results from Bash output and creates 3 lists.
    Args: 
        query_result: Values returned from querying screen_set
    Returns:
        3 lists (id_list, name_list, channel_id_list) containing all the values in  
        id | name            | channel_id |  
    """
    if query_result:
        for line in query_result:  # Iterate over list
            parts = line.split("\t")
            if len(parts) == 3:
                id_list.append(parts[0])
                name_list.append(parts[1])
                channel_id_list.append(parts[2])


def count_solution_instances(channel_id_value):
    """
    Counts occurrences of a solution value (channel_id).

    Args: 
        channel_id_value (any): Any value from the column `channel_id`.

    Returns:
        int: Count of occurrences of the solution value in `channel_id_list`.
    """
    count = channel_id_list.count(channel_id_value)
    return count




def change_db_value(id, value):
    """Changes the desired value in the local database.

    Args:
        id: The ID of the row to update.
        value: The new value for the 'name' column.

    Returns:
        True if the update was successful, False otherwise.
    """
    try:
        
        query_change = f"UPDATE {SCREEN_SET_TABLE} SET name = '{value}' WHERE id = {id};"

        # Use double quotes around the query in the -e argument
        command = f"mysql -u {DB_USER} -p'{DB_PASSWORD}' -D {DB_NAME} -e \"{query_change}\""

        process = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if process.returncode == 0:
            print("Name changed successfully.")
            return True
        else:
            print(f"Error changing name: {process.stderr}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error: Unable to connect to the MySQL database. Please check your credentials and database settings. {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    

    
def is_failover():
    """
    Creates a list of 0s and 1s based on the occurrence count of values in channel_id_list. 1s are failover, zeros arent

    Args:
        channel_id_list: A list of channel_id values.

    Returns:
        A list of 0s and 1s, where 1 indicates a failover set, and 0 indicates a primary set.
    """
    occurrence_counts = {}  # Dictionary to store occurrence counts
    result_list = []

    for channel_id in channel_id_list:
        if channel_id not in occurrence_counts:
            occurrence_counts[channel_id] = 0
            result_list.append(0)  # First occurrence, append 0
        else:
            occurrence_counts[channel_id] += 1
            if occurrence_counts[channel_id] == 1: #second occurence
                result_list.append(1)
            else:
                result_list.append(0)
                occurrence_counts[channel_id] = 0 #reset the counter to zero.

    return result_list

def get_channels_list():
  """
  Returns a new list containing only the unique values from the channel_id_list,
  preserving the original order.
  """
  unique_list = []
  seen = set()  # Use a set to track seen values for efficiency

  for item in channel_id_list:
    if item not in seen:
      unique_list.append(item)
      seen.add(item)

  return unique_list    


############### MAIN #####################
test_db_connection()
data = query_screen_set()
if data:
    #print(f" query preprocessing: {data}")
    process_query_results(data)

#get a list of failover sets
failover_list = is_failover()

#get a list of unique channel values
channel_values = get_channels_list()
#empty list to count everytime we name a set in each channel
set_named_counter = [1] * len(channel_values)

#Name creation
for i in range(len(id_list)):
    
    # Prints the 3 values from each row of the screen_set table (for testing)
    print(f"""ID={id_list[i]}, Name={name_list[i]}, Channel ID={channel_id_list[i]}, solution count {count_solution_instances(channel_id_list[i])}""")

    # 
    if set_named_counter[channel_values.index(channel_id_list[i])] <= 2:
        try:
            if failover_list[i]:
                new_name = channel_name_map[channel_id_list[i]] + SET_1 + FAILOVER
                print(f"New name would be: {new_name}")
                change_db_value(int(id_list[i]), new_name)
                set_named_counter[channel_values.index(channel_id_list[i])] +=1
            else:
                new_name = channel_name_map[channel_id_list[i]] + SET_1
                print(f"New name would be: {new_name}")
                change_db_value(int(id_list[i]), new_name)
                set_named_counter[channel_values.index(channel_id_list[i])] +=1
            
        except KeyError:
            print(f"Error: Channel ID '{channel_id_list[i]}' not found in channel_name_map. Skipping this value")
            # Skip the SQL update, Value not found

    elif set_named_counter[channel_values.index(channel_id_list[i])] > 2:
        try:
            if failover_list[i]:
                new_name = channel_name_map[channel_id_list[i]] + SET_2 + FAILOVER
                print(f"New name would be: {new_name}")
                change_db_value(int(id_list[i]), new_name)
                set_named_counter[channel_values.index(channel_id_list[i])] +=1
            else:
                new_name = channel_name_map[channel_id_list[i]] + SET_2
                print(f"New name would be: {new_name}")
                change_db_value(int(id_list[i]), new_name)
                set_named_counter[channel_values.index(channel_id_list[i])] +=1
            
        except KeyError:
            print(f"Error: Channel ID '{channel_id_list[i]}' not found in channel_name_map. Skipping this value")

