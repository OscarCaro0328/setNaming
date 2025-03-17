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


#takes the query results already separated in rows, and splits results in 3 arrays
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

    
    # print(f"ID Array: {id_array}")
    # print(f"Name Array: {name_array}")
    # print(f"Channel ID Array: {channel_id_array}")


def is_failover(input_string):
    """Defines if a set_name is failover based on different variations of the name."""
    if not input_string:
        return "Error: Input string is empty."

    # Added variations: Failaover, Backup, Failvoer, set 2 and others found in data
    failover_pattern = (
    r"\b("
    r"fail[\s\-/]*o[\s\-/]*v[\s\-/]*e?r|"  # Handles different spacing variations of "failover"
    r"fo|failvover|faiolver|failolver|faiover|faover|"
    r"faillover|feilover|failove|failver|faillover|failover|backup|"
    r"filover|failoverbak|falover|failovr|failloverr|failovered|"
    r"failovering|failaover|failvoer|Set 2"
    r")\b|failover\b|failover\w+"
    )
  
    if re.search(failover_pattern, input_string, re.IGNORECASE):
        return FAILOVER
    else:
        return NOT_FAILOVER
    
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
    
def more_than_one_set(channel_id_value):
    """Checks 1 condition to validate if site has more than 1 set.
        Args: 
        channel_id_value: Any value from the Column channel_id
    Returns:
        True if channel_id has 2 or more values in the whole database table
        THis means that the solution (For example FC BR Combo has 2 sets created in SB Local )
      """
    count = channel_id_list.count(channel_id_value)
    return count >= 2

def name_constructor_one_set_solution(channel_id_value):
    count = channel_id_list.count(channel_id_value)
    


############### MAIN #####################
test_db_connection()
data = query_screen_set()
if data:
    #print(f" query preprocessing: {data}")
    process_query_results(data)



#Name creation
for i in range(len(id_list)):
    
    print(f"""ID={id_list[i]}, Name={name_list[i]}, Channel ID={channel_id_list[i]}, 
          solution count {count_solution_instances(channel_id_list[i])}""")
    
    if count_solution_instances(channel_id_list[i]) == 1:
        new_name = channel_name_map[channel_id_list[i]] + SET_1
        print(f"New name would be: {new_name}" )
    if count_solution_instances(channel_id_list[i]) == 2:
        new_name = channel_name_map[channel_id_list[i]] + SET_1 + is_failover(name_list[i])
        print(f"New name would be: {new_name}" )