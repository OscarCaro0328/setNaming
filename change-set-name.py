#!/usr/bin/env python3
# Script to update screen_set db table in media players for Prod Dunkin Domain. 
# It uses DUnkin standards Channel name + set number + is_Failover?
# Works with python 3.4 version and above. No other requirenments




import sys
import subprocess
import re

# Database Configuration
SCREEN_SET_TABLE = "screen_set"
QUERY_SCREEN_SET_TABLE = "SELECT * FROM screen_set ORDER BY channel_id;"
QUERY_TEST_CONNECTION = "SELECT 1;"

# SET name conventions
SET_1 = "1"
SET_2 = "2"
FAILOVER = " Failover"
NOT_FAILOVER = ""

# Constants
DUNKIN_PROD = "us.dunkindonuts.switchboardcms.com"
DUNKIN_QA_UAT = "us-dunkindonuts-qa.uat.switchboardcms.com"
DUNKIN_LAB = "lab.us.dunkindonuts.coates.io"
DOMAIN_FILE_PATH = "/var/lib/switchboard/data/domain.name"
UPSTREAM_FILE_PATH = "/var/lib/switchboard/data/network.upstream"
HQ_FILE_PATH = "/var/lib/switchboard/data/network.hq"
channel_name_map = {}

#auxiliars
set_count = 0


# Channel ID to Name mapping for us.dunkindonuts.switchboardcms.com
channel_name_map_dunkin_prod = {
    "1": "DT DNK Combo - ",
    "3": "Coates-System - ",
    "4": "DT DNK Presell - ",
    "5": "FC DNK - ",
    "6": "WUW DNK - ",
    "7": "WUW DNK - ",
    "8": "FC BR Combo - ",
    "9": "OSB DNK - ",
    "10": "FC DNK - ",
    "11": "FC DNK - ",
    "12": "FC DNK - ",
    "15": "FC BR Standalone - ",
    "19": "FC DNK - ",
    "20": "FC DNK - ",
    "29": "Int Promo DNK - ",
    "30": "FC DNK - ",
    "31": "DT DNK Non-OT - ",
    "32": "Int Promo DNK - ",
    "33": "Ext Promo DNK - ",
    "34": "Ext Promo DNK - ",
    "35": "FC DNK - ",
    "37": "FC BR - ",
    "38": "DT BR - ",
    "42": "FC BR Combo - ",
    "43": "FC BR Combo - ",
    "44": "FC BR Standalone - ",
    "45": "DT DNK-Combo - ",
    "46": "FC BR Special - ",
    "47": "FC BR Combo-special - ",
}

# Channel_id to Name mapping for us-dunkindonuts-qa.uat.switchboardcms.com
channel_name_map_dunkin_qa_uat = {
    "1" : "Drive Thru - ",
    "2" : "DT DNK Presell - ",
    "3" : "WUW DNK - ",
    "5" : "Coates-System - ",
    "6" : "FC DNK - ",
    "7" : "FC DNK - ",
    "8" : "FC DNK - ",
    "9" : "FC DNK - ",
    "10" : "OSB DNK - ",
    "11" : "Int Promo DNK - ",
    "12" : "FC BR Combo - ",
    "13" : "WUW DNK - ",
    "14" : "Logos - ",
    "15" : "FC BR Standalone - ",
    "16" : "FC DNK - ",
    "17" : "Int Promo DNK - ",
    "18" : "FC DNK - ",
    "19" : "Ext Promo DNK - ",
    "20" : "Ext Promo DNK - ",
    "21" : "FC DNK - ",
    "22" : "FC DNK - ",
    "23" : "FC BR - ",
    "24" : "DT BR - ",
    "26" : "Front Counter BR - ",
    "27" : "Front Counter BR - ",
    "29" : "FC BR Combo - ",
    "30" : "FC BR Combo - ",
    "31" : "FC BR Standalone - ",
    "32" : "DT DNK Non-OT - ",
    "33" : "DT DNK Combo - ",
    "34" : "Smithfields - ",
    "35" : "content test - ",
    "36" : "Albert - test - ",
    "38" : "FC BR Combo-special - ",
}

# Channel_id to Name mapping for lab.us.dunkindonuts.coates.io
channel_name_map_dunkin_lab = {
    "3" : "Coates-System - ",
    "30" : "FC DNK - ",
    "31" : "FC DNK - ",
    "32" : "FC DNK - ",
    "33" : "FC DNK - ",
    "34" : "OSB DNK - ",
    "35" : "DT DNK Combo - ",
    "36" : "DT DNK Presell - ",
    "37" : "WUW DNK - ",
    "38" : "Int Promo DNK - ",
    "45" : "FC BR Combo - ",
    "46" : "WUW DNK - ",
    "47" : "Logos - ",
    "50" : "FC BR Standalone - ",
    "53" : "FC DNK - ",
    "55" : "Int Promo DNK - ",
    "56" : "FC DNK - ",
    "58" : "Ext Promo DNK - ",
    "59" : "Ext Promo DNK - ",
    "67" : "FC DNK - ",
    "68" : "FC DNK - ",
    "69" : "DT DNK Non-OT - ",
    "70" : "FC BR - ",
    "74" : "DT BR - ",
    "75" : "FC BR Combo - ",
    "76" : "FC BR Combo - ",
    "77" : "FC BR Standalone - ",
    "78" : "FC BR Combo-special - ",
    "79" : "FC BR Special - ",
}



# --------------------------------FUNCTIONS -----------------------------

def define_current_domain(domain_file_path):
    """
    Defines the domain of the mp based on domain path
    """
    global channel_name_map
    try:
        with open(domain_file_path, "r") as file:
            domain_name = file.read().strip()  # Read and remove leading/trailing whitespace

        if domain_name == DUNKIN_PROD:
            print("Production environment detected.")
            print("Using production values for the channels.")
            channel_name_map = channel_name_map_dunkin_prod

        elif domain_name == DUNKIN_QA_UAT:
            print("QA/UAT environment detected.")
            print("Using QA/UAT values for the channels.")
            channel_name_map = channel_name_map_dunkin_qa_uat

        elif domain_name == DUNKIN_LAB:
            print("Dunkin LAB environment detected.")
            print("Using Dunkin LAB values for the channels.")
            channel_name_map = channel_name_map_dunkin_lab

        else:
            print("Domain : {} not implemented. Names can not be changed".format(domain_name))
            sys.exit(0)


    except FileNotFoundError:
        print("Error: File not found at {}. Unable to define domain".format(domain_file_path))
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
        sys.exit(1)


    #switchboard dev mysqlQuery implemented and tested in 2025-04/30
def test_db_connection():
    """Tests the database connection using switchboard dev mysqlQuery."""
    try:
        command = "switchboard dev mysqlQuery '{}'".format(QUERY_TEST_CONNECTION)
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Connected to MySQL database successfully.")
    except subprocess.CalledProcessError as e:
        print(
            "Error: Unable to connect to the MySQL database. Please check mysql service. {}".format(e)
        )
        sys.exit(1)


def query_screen_set():
    """Queries the sql screen_set table using switchboard dev mysqlQuery .
    Returns:
        A strings representing the screen_set table. RAW data

         id | name            | channel_id |
        +----+-----------------+------------+
        |  1 | Lane 1          |          1 |

    """
    try:
        #
        command = "switchboard dev mysqlQuery '{}'".format(QUERY_SCREEN_SET_TABLE)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        raw_data = result.stdout.decode('utf-8').strip()  # Clear leading and trailing whitespaces


        if not raw_data:  # Check if empty
            print("No data found in the table. Exiting since we got nothing to change here.")
            sys.exit(0)

        return raw_data  # Return query rows
    except subprocess.CalledProcessError as e:
        print("Error executing MySQL command: {}".format(e))
        print("Exiting script since we can't query the database")
        sys.exit(1)

def clean_mysql_output(raw_data):
    """Processes the query raw data, removes formating, returns a list of lists od the wanted data.
    Args:
        query_result: Raw data returned from querying screen_set
    Returns:
        an lsit with of lists with all the rows in the table
        id | name            | channel_id |
    """
    lines = raw_data.strip().splitlines()

    # Remove border lines (start with +) and empty lines
    content_lines = [line for line in lines if not line.startswith('+') and line.strip()]

    # Strip each line and split by |, removing leading/trailing whitespace
    cleaned_rows = []
    for line in content_lines:
        parts = [col.strip() for col in line.strip('|').split('|')]
        cleaned_rows.append(parts)

    return cleaned_rows

def process_query_results(query_data):
    """Processes the query results and separates them in rows and creates a dictionary with 3 lists.
    Args:
        query_result: Values returned from querying screen_set
    Returns:
        an object with 3 lists (id_list, name_list, channel_id_list) containing all the values in
        id | name            | channel_id |
    """
    data_object = {
        "id_list": [],
        "name_list": [],
        "channel_id_list": []
    }
    data_rows = query_data[1:]  # Skips the header row

    if data_rows:
        for row in data_rows:  
            data_object["id_list"].append(row[0])  
            data_object["name_list"].append(row[1])  
            data_object["channel_id_list"].append(row[2]) 
    return data_object



def is_failover(input_string):
    """Defines if a set_name is failover based on different variations of the name."""
    if not input_string:
        return "Error: Input string is empty."

    # Added variations: Failaover, Backup, Failvoer, set 2 and others found in data
    failover_pattern = (
    r"\b("
    r"fail[\s\-/]*o[\s\-/]*v[\s\-/]*e?r|"  # Handles different spacing variations of "failover"
    r"fo|failvover|faiolver|failolver|faiover|faover|"
    r"faillover|feilover|failove|failver|faillover|fail over|fail|failover|backup|"
    r"filover|failoverbak|fail0ver|falover|failovr|failloverr|failovered|"
    r"failovering|failaover|failvoer|Set 2"
    r")\b|failover\b|failover\w+"
    )

    if re.search(failover_pattern, input_string, re.IGNORECASE):
        return FAILOVER
    else:
        return NOT_FAILOVER




def count_solution_instances(channel_id_value,channel_id_list):
    """
    Counts occurrences of a solution value (channel_id).

    Args:
        channel_id_value (int): Any value from the column `channel_id`.
        channel_id_list (list): list with complete `channel_id`values

    Returns:
        int: Count of occurrences of the solution value in `channel_id_list`.
    """
    count = channel_id_list.count(channel_id_value)
    return count


def create_failover_values_lists(name_list):
    """
    Creates a list of failover values (1 or 0) based on the name_list.

    Args:
        name_list: A list of names to check for failover sets.

    Returns:
        A list of bools (1 or 0) representing failover sets.
    """
    failover_list = [0] * len(name_list)
    for i in range(len(name_list)):
        if is_failover(name_list[i]) == FAILOVER:
            failover_list[i] = 1
    return failover_list

    #
def channel_failover_identifier(target_channel_id, channel_id_list, failover_list):
    """
    Checks if a the target_channel has a positively identified failover set.

    Args:
        target_channel_id (int): The channel ID to search for.
        channel_id_list (list): list with complete `channel_id`values
        failover_list (list): List created from the function create_failover_values_lists .

    Returns:
        True if at least one corresponding flag is 1, False otherwise.
        This means Failover has been identified succesfully in target channel
    """

    if len(channel_id_list) != len(failover_list):
        print("Error: channel_id_list and failover_list must have the same length. Aborting")
        sys.exit(1)
        
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

        query_change = "UPDATE {} SET name = \\\"{}\\\" WHERE id = {};".format(SCREEN_SET_TABLE, value, id)
        command = "switchboard dev mysqlQuery \"{}\"".format(query_change)

        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if process.returncode == 0:
            print("Name changed successfully.")
            return True
        else:
            print("Error changing name: {}".format(process.stderr.decode('utf-8')))
            return False

    except subprocess.CalledProcessError as e:
        print("Error: Unable to connect to the MySQL database. Please check mysql service. {}".format(e))
        return False
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
        return False


#Sb package is needed to updated db information on slaves
def run_sb_package():
    """Runs the 'switchboard package' command in a shell and returns the output."""
    print("Running sb package,please hang tight")
    try:
        process = subprocess.Popen(
            ["switchboard", "package"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return "Error: {}".format(stderr.decode('utf-8'))
    except OSError as e:
        return "Error executing 'switchboard package': {}".format(e)



def is_device_prime(upstream_file_path, hq_file_path):
    """
    Checks if network.upstream and network.hq files are the same.

    Returns:
        True if MP is prime, False otherwise.
    """

    try:
        with open(upstream_file_path, "r") as f_upstream:
            upstream_content = f_upstream.read().strip()
        with open(hq_file_path, "r") as f_hq:
            hq_content = f_hq.read().strip()
        return upstream_content == hq_content

    except FileNotFoundError as e:
        print("Error: File not found: {}".format(e.filename))
        return False
    except Exception as e:
        print("An unexpected error occurred: {}".format(e))
        return False




################################### MAIN ########################################

#Only meant to be executed in prime MP. Will exit on Slaves
if not is_device_prime(UPSTREAM_FILE_PATH, HQ_FILE_PATH):
    print("NOT PRIME MP. NOT EXECUTING")
    sys.exit(0)

define_current_domain(DOMAIN_FILE_PATH)
test_db_connection()
raw_data = query_screen_set()
parsed_data = clean_mysql_output(raw_data)
data_object= process_query_results(parsed_data)

failover_list = create_failover_values_lists(data_object['name_list']) 

print("-" * 40)  # Prints 40 dashes for formatting purposes 

# Name creation
for i in range(len(data_object["id_list"])):
    # Prints current values

    this_id = data_object['id_list'][i]
    this_name = data_object['name_list'][i]
    this_channel_ID = data_object['channel_id_list'][i]
    number_of_instances = count_solution_instances(this_channel_ID, data_object['channel_id_list'])
    failover_identified = channel_failover_identifier(this_channel_ID, data_object['channel_id_list'], failover_list)
    new_name = this_name  # Default to the current name

    print(
        "ID={}, ".format(this_id) +
        "Name={}, ".format(this_name) +
        "Channel ID={}, ".format(this_channel_ID) +
        "solution count {}, ".format(number_of_instances) +
        "failover_identified: {}".format(failover_identified)
    )

    try:

        set_name_standard = channel_name_map[this_channel_ID]

        # If a channel has only one occurrence, no failover or set 2 possible, name changing for sure
        if number_of_instances == 1:
            new_name = set_name_standard + SET_1


        # If a channel has 2 occurrences one set will be primary and the other one Failover
        # If we are not able to identify failover channel, we will skip name changing in this channel
        # This is to avoid both sets being named the same in a channel.
        if number_of_instances == 2 and failover_identified:
            new_name = set_name_standard + SET_1 + is_failover(this_name)

        # If a channel has 4 occurences, most likely it is a 2 Lane Drive Thru or 2 IDMBs.
        # Values in DB are always in order by creation
        # First 2 are first lane, second 2 are second lane.
        if number_of_instances == 4:
            set_count += 1

            if set_count == 1:
                new_name = set_name_standard + SET_1
            elif set_count == 2:
                new_name = set_name_standard + SET_1 + FAILOVER
            elif set_count == 3:
                new_name = set_name_standard + SET_2
            elif set_count == 4:
                new_name = set_name_standard + SET_2 + FAILOVER
                set_count = 0  # Reset the counter for the next channel


        print("New name would be: {}".format(new_name))
        change_db_value(int(this_id), new_name) if new_name != this_name else print("Old name is equal to new name. NOT UPDATING DB")

    except KeyError:
        print("Error: Channel ID '{}' not found in channel_name_map. Skipping this value".format(this_channel_ID))

    print("-" * 40)  # Prints 40 dashes for formatting purposes


print(run_sb_package()) #Prime media players will update slaves.