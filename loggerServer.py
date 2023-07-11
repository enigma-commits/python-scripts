import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
data = {"rider":{"INSERT_INTO": [], "UPDATE": [], "DELETE_FROM": [], "SELECT": []}, "driver":{"INSERT_INTO": [], "UPDATE": [], 
                                                                                              "DELETE_FROM": [], "SELECT": []}}
count = {"rider":{"INSERT_INTO": [], "UPDATE": [], "DELETE_FROM": [], "SELECT": []}, "driver":{"INSERT_INTO": [], "UPDATE": [], 
                                                                                              "DELETE_FROM": [], "SELECT": []}}

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


@app.route('/')
def execute_script():
    # Read the log file
    paths = {"rider": "/Users/akhilesh.b/Desktop/nammayatri/Backend/rider-app-exe.log", "driver": "/Users/akhilesh.b/Desktop/nammayatri/Backend/dynamic-offer-driver-app-exe.log"}
    request_name = request.args.get('request_name')
    for log_file_path in paths.keys():
        log_file_path1 = paths[log_file_path]
        with open(log_file_path1, 'r') as file:
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
        count[log_file_path]["INSERT_INTO"] = len(insert["INSERT INTO"]) - len(data[log_file_path]["INSERT_INTO"])
        count[log_file_path]["UPDATE"] = len(update["UPDATE"]) - len(data[log_file_path]["UPDATE"])
        count[log_file_path]["DELETE_FROM"] = len(delete["DELETE FROM"]) - len(data[log_file_path]["DELETE_FROM"])
        count[log_file_path]["SELECT"] = len(select["SELECT"]) - len(data[log_file_path]["SELECT"])
        data[log_file_path]["INSERT_INTO"] = insert["INSERT INTO"]
        data[log_file_path]["UPDATE"] = update["UPDATE"]
        data[log_file_path]["DELETE_FROM"] = delete["DELETE FROM"] 
        data[log_file_path]["SELECT"] = select["SELECT"]
        f = open("./logFiles.txt", "a")
        f.write(request_name+'\n')
        f.write(log_file_path+'\n')
        f.write("INSERT_INTO:" + str(data[log_file_path]["INSERT_INTO"]) + ' with length ' + str(len(data[log_file_path]["INSERT_INTO"]))+'\n')
        f.write("==============================================================================\n")
        f.write("UPDATE:" + str(data[log_file_path]["UPDATE"]) + ' with length ' + str(len(data[log_file_path]["UPDATE"]))+ '\n')
        f.write("==============================================================================\n")
        f.write("DELETE_FROM: " + str(data[log_file_path]["DELETE_FROM"]) + ' with length ' + str(len(data[log_file_path]["DELETE_FROM"]))+ '\n')
        f.write("==============================================================================\n")
        f.write("SELECT:" + str(data[log_file_path]["SELECT"]) + ' with length ' + str(len(data[log_file_path]["SELECT"]))+ '\n')
        f.write("******************************************************************************\n")
        f.write("******************************************************************************\n")
        f.close()


    return "logs Generated."
    



if __name__ == '__main__':
    app.run()
