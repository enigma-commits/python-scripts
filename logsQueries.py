

import re
import json
from collections import Counter

def helper(str):
    ans = ''
    for i in range(len(str)):
        if str[i] == '\\' or str[i] == '"' or str[i] == "'" or str[i]=='{' or str[i]=='}':
            continue
        ans += str[i]
    # print(ans)
    value = ans.split("msg:")[-1]
    # print(value)
    return value

def extract_queries(log_line):
    # Regular expression pattern to match SQL queries
    query_pattern = r".*?(?i)SELECT\s+.+?\s+FROM\s+(\w+)"
    # print(log_line)
    # Extract the JSON message from the log line
    log_json = re.search(r'{"level":"info".+?"message":"(.+?)"}', log_line)
    # print(log_json)
    if log_json:
        log_message = log_json.group(1)
        # print(log_line)
        # Replace escaped double quotes with double quotes
        log_message = helper(log_message)
        # log_message = log_message.replace('\\"', '"')
        # print(log_message)
        if "SELECT" in log_message or "INSERT" in log_message or "UPDATE" in log_message or "DELETE" in log_message:
            # Extract the table name from the query
            # table = re.search(query_pattern, log_message)
            print(log_message)
            if table:
                return table.group(1)
    return None

log_file_path = '/Users/akhilesh.b/Desktop/nammayatri/Backend/dynamic-offer-driver-app-exe.log'

# Read the log file
with open(log_file_path, 'r') as file:
    log_lines = file.readlines()

# Extract SQL queries and count their occurrences
query_counter = Counter()
for log_line in log_lines:
    table = extract_queries(log_line)
    if table:
        query_counter[table] += 1

# Print the query counts and accessed tables
for table, count in query_counter.items():
    print("Table:", table)
    print("Count:", count)
    print("---")
