#!/usr/bin/env python3
#Script to update screen_set db table in media players for Prod Dunkin Domain



import sys
import subprocess
import re

# Database Configuration
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "switchboard"
SCREEN_SET_TABLE = "screen_set"
QUERY = "SELECT * FROM screen_set ORDER BY id;"

# SET name conventions
SET_1 = " 1 "
SET_2 = " 2 "
FAILOVER = "Failover"
NOT_FAILOVER = ""

# Initialize lists
id_list = []
name_list = []
channel_id_list = []
failover_list = []

#Domains in which implementation is defined
DUNKIN_PROD = "us.dunkindonuts.switchboardcms.com"
DUNKIN_QA_UAT = "us-dunkindonuts-qa.uat.switchboardcms.com"
DOMAIN_FILE_PATH = "/var/lib/switchboard/data/domain.name"
channel_name_map = {}


# Channel ID to Name mapping for us.dunkindonuts.switchboardcms.com
channel_name_map_dunkin_prod = {
    "1": "Drive Thru -",
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
    "31": "DT DNK Non-OT -",
    "32": "Int Promo DNK -",
    "33": "Ext Promo DNK -",
    "34": "Ext Promo DNK -",
    "35": "FC DNK -",
    "37": "FC BR -",
    "38": "DT BR -",
    "42": "FC BR Combo -",
    "43": "FC BR Combo -",
    "44": "FC BR Standalone -",
    "45": "DT DNK-Combo -",
}

# Channel_id to Name mapping for us-dunkindonuts-qa.uat.switchboardcms.com
channel_name_map_dunkin_qa_uat = {
    "1" : "Drive Thru - Vertical -",
    "2" : "DT DNK Presell -",
    "3" : "WUW DNK - V -",
    "5" : "Coates-System -",
    "6" : "FC DNK - V -",
    "7" : "FC DNK - V -",
    "8" : "FC DNK- H -",
    "9" : "FC DNK- H -",
    "10" : "OSB DNK - H -",
    "11" : "Int Promo DNK -",
    "12" : "FC BR Combo - H -",
    "13" : "WUW DNK - V -",
    "14" : "Logos -",
    "15" : "FC BR Standalone - H -",
    "16" : "FC DNK - V -",
    "17" : "Int Promo DNK -",
    "18" : "FC DNK- H -",
    "19" : "Ext Promo DNK -",
    "20" : "Ext Promo DNK -",
    "21" : "FC DNK- H -",
    "22" : "FC DNK- H -",
    "23" : "FC BR - H -",
    "24" : "DT BR - V -",
    "26" : "Front Counter BR - Horizontal - 4 -",
    "27" : "Front Counter BR - Horiz - 4 -",
    "29" : "FC BR Combo - H -",
    "30" : "FC BR Combo - H -",
    "31" : "FC BR Standalone - H -",
    "32" : "DT DNK Non-OT - V -",
    "33" : "DT DNK Combo - V -",
    "34" : "Smithfields -",
    "35" : "content test -",
    "36" : "Albert - test - Horizontal -",
}



# --------------------------------FUNCTIONS -----------------------------

def define_current_domain():
    """
    Defines the domain of the mp based on /var/lib/switchboard/data/domain.name 
    """
    global channel_name_map
    try:
        with open(DOMAIN_FILE_PATH, "r") as file:
            domain_name = file.read().strip()  # Read and remove leading/trailing whitespace

        if domain_name == DUNKIN_PROD:
            print("Production environment detected.")
            print("Using production values for the channels.")
            channel_name_map = channel_name_map_dunkin_prod
            
        elif domain_name == DUNKIN_QA_UAT:
            print("QA/UAT environment detected.")
            print("Using QA/UAT values for the channels.")
            channel_name_map = channel_name_map_dunkin_qa_uat
            
        else:
            print(f"Domain : {domain_name} not implemented. Names can not be changed")
            sys.exit(0)
            

    except FileNotFoundError:
        print(f"Error: File not found at {DOMAIN_FILE_PATH}. Unable to define domain")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)



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
        sys.exit(1)


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
            sys.exit(0)

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


def create_failover_values_lists():
    """
    Creates a list of failover values (1 or 0) based on the name_list.

    Args:
        name_list: A list of names to check for failover sets.

    Returns:
        A list of bools (1 or 0) representing failover sets.
    """    
    failover_list = [0] * len(name_list)
    for i in range(len(name_list)):
        if is_failover(name_list[i]) == "Failover":
            failover_list[i] = 1
    return failover_list

    #
def channel_failover_identifier(target_channel_id):
    """
    Checks if a the target_channel has a positively identified failover set.

    Args:
        target_channel_id: The channel ID to search for.

    Returns:
        True if at least one corresponding flag is 1, False otherwise.
        This means Failover has been identified succesfully in target channel
    """

    if len(channel_id_list) != len(failover_list):
        raise ValueError("channel_id_list and flag_list must have the same length.")

    failover_found = False

    for i in range(len(channel_id_list)):
        if channel_id_list[i] == target_channel_id and failover_list[i] == 1:
            failover_found = True
            break  # No need to continue searching if a 1 is found

    return failover_found    


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

    #Sb package is needed to updated db information on slaves
def run_sb_package():
    """Runs the 'switchboard package' command in a shell and returns the output."""
    print("Running sb package,please hang tight")
    try:
        result = subprocess.run(
            ["switchboard", "package"],  # Command as a list
            text=True,                  # Ensures output is in string format
            capture_output=True,        # Captures stdout and stderr
            check=True                  # Raises an error if the command fails
        )
        return result.stdout  # Return the output of the command
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"  # Return error message if the command fails   
    
def is_device_prime():
    """
    Checks if network.upstream and network.hq files are the same.

    Returns:
        True if MP is prime, False otherwise.
    """
    upstream_file = "/var/lib/switchboard/data/network.upstream"
    hq_file = "/var/lib/switchboard/data/network.hq"

    try:
        with open(upstream_file, "r") as f_upstream, open(hq_file, "r") as f_hq:
            upstream_content = f_upstream.read().strip()
            hq_content = f_hq.read().strip()
            return upstream_content == hq_content

    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def lane1_lane2_identifier(input_string):
    """
    Identifies if a string contains variations of "Lane 1" or "Lane 2",
    regardless of order or location within the string.

    Args:
        input_string: The string to search.

    Returns:
        "Lane 1" if the string contains variations of "Lane 1",
        "Lane 2" if the string contains variations of "Lane 2",
        None otherwise.
    """
    if not isinstance(input_string, str):
        return None  # Handle non-string input

    lane1_pattern = r"[Ll][Aa][Nn][Ee]\s*1"
    lane2_pattern = r"[Ll][Aa][Nn][Ee]\s*2"

    if re.search(lane1_pattern, input_string):
        return "Lane 1"
    elif re.search(lane2_pattern, input_string):
        return "Lane 2"
    else:
        return "Not Identified"


############### MAIN #####################

#If MP is not prime, it exists with a non-error code 0.
if not is_device_prime():
    print("NOT PRIME MP. NOT EXECUTING")
    sys.exit(0)

define_current_domain()

test_db_connection()

data = query_screen_set()

if data:
    process_query_results(data)

failover_list = create_failover_values_lists()

print("-" * 40)  # Prints 40 dashes for formatting purposes 

# Name creation
for i in range(len(id_list)):
    # Prints the 3 values from each row of the screen_set table (for testing)
    print(
    f"ID={id_list[i]}, "
    f"Name={name_list[i]}, "
    f"Channel ID={channel_id_list[i]}, "
    f"solution count {count_solution_instances(channel_id_list[i])}, "
    f"failover_identified: {channel_failover_identifier(channel_id_list[i])}"
        )
    
    try:
        number_of_instances = count_solution_instances(channel_id_list[i])
        failover_identified = channel_failover_identifier(channel_id_list[i])
        set_name_standard = channel_name_map[channel_id_list[i]]

        # If a channel has only one occurrence, no failover or set 2 possible, name changing for sure
        if number_of_instances == 1:
            new_name = set_name_standard + SET_1
            print(f"New name would be: {new_name}")
            change_db_value(int(id_list[i]), new_name) if new_name != name_list[i] else print("Old name is equal to new name. NOT CHANGING")
            

        # If a channel has 2 occurrences one set will be primary and the other one Failover
        # If we are not able to identify failover channel, we will skip name changing in this channel
        # This is to avoid both sets being named the same in a channel.
        if number_of_instances == 2 and failover_identified:
            new_name = set_name_standard + SET_1 + is_failover(name_list[i])
            print(f"New name would be: {new_name}")
            change_db_value(int(id_list[i]), new_name) if new_name != name_list[i] else print("Old name is equal to new name. NOT CHANGING")


        # If a channel has 4 occurences, most likely it is a 2 Lane Drive Thru.
        # If we are able to identify Lane 1 and Lane 2. We change their values
        # Otherwise we leave it as is.
        if number_of_instances == 4 and failover_identified:
            lane = lane1_lane2_identifier(name_list[i])
            if lane == "Lane 1":
                new_name = set_name_standard + SET_1 + is_failover(name_list[i])
            elif lane == "Lane 2":
                new_name = set_name_standard + SET_2 + is_failover(name_list[i])
            else:
                new_name = name_list[i] #Not changing anything.
                print("Lane 1 or Lane 2 not identified, name not changing.")
            print(f"New name would be: {new_name}")
            change_db_value(int(id_list[i]), new_name) if new_name != name_list[i] else print("Old name is equal to new name. NOT CHANGING")

    except KeyError:
        print(f"Error: Channel ID '{channel_id_list[i]}' not found in channel_name_map_dunkin_prod. Skipping this value")
    
    print("-" * 40)  # Prints 40 dashes for formatting purposes  
        


run_sb_package() #Prime media players will update slaves.