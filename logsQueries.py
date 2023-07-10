import re
import json
from collections import Counter
def helper(str):
    ans = ''
    for i in range(len(str)):
        if str[i] == '\\' or str[i] == '"' or str[i] == "'" or str[i]=='{' or str[i]=='}':
            continue
        ans += str[i]
    value = ans.split("msg:")[-1]
    return value
def extract_queries(log_line):
    # Extract the JSON message from the log line
    if "INSERT INTO" in log_line or "UPDATE" in log_line or "SELECT" in log_line or "DELETE FROM":
        log_json = re.search(r'{"level":"info".+?"message":"(.+?)"}', log_line)
        if log_json:
            log_message = log_json.group(1)
            # Replace escaped double quotes with double quotes
            log_message = helper(log_message)
            return log_message
    return None
def extract_query_info(input_string):
    if not isinstance(input_string, str):
        return None
    input = str(input_string)
    # Define the regular expression pattern to extract the required information
    pattern = r'(INSERT INTO|UPDATE|DELETE FROM) (\w+)\.(\w+)'
    # Search for the pattern in the input string
    match = re.search(pattern, input_string)
    if match:
        # Extract the query name, schema name, and table name from the matched groups
        query_name = match.group(1)
        schema_name = match.group(2)
        table_name = match.group(3)
        return  (query_name, table_name)
    else:
        selectPattern = r'FROM (\w+)\.(\w+)'
        selectMatch = re.search(selectPattern, input_string)
        if selectMatch:
            query_name = "SELECT"
            table_name = selectMatch.group(2)
            return  (query_name, table_name)
log_file_path = '/Users/akhilesh.b/Desktop/nammayatri/Backend/dynamic-offer-driver-app-exe.log'
# Read the log file
with open(log_file_path, 'r') as file:
    log_lines = file.readlines()
insert = {"INSERT INTO" : []}
update = {"UPDATE" : []}
delete = {"DELETE FROM" : []}
select = {"SELECT" : []}
for log_line in log_lines:
    log_msg = extract_queries(log_line)
    result = extract_query_info(log_msg)
    #print("jshdkfgkshg",result)
    if result != None:
        if result[0] == "INSERT INTO":
            insert[result[0]].append(result[1])
        if result[0] == "UPDATE":
            update[result[0]].append(result[1])
        if result[0] == "DELETE FROM":
            delete[result[0]].append(result[1])
        if result[0] == "SELECT":
            select[result[0]].append(result[1])
print("insertLOG:::::", insert)
print()
print("updateLOG:::::", update)
print()
print("deleteLOG:::::", delete)
print()
print("selectLOG:::::", select)