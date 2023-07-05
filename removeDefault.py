import re
import os 

def remove_block_from_file(file_path, file_name):
    pattern = f"default{file_name[0:-3]}"

    print(pattern)
    start_pattern = re.escape(pattern)
    end_pattern = r"}"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_line = None
    end_line = None
    for i, line in enumerate(lines):
        if re.search(start_pattern, line) and start_line is None:
            start_line = i
        if start_line is not None and re.search(end_pattern, line):
            end_line = i
            break

    if start_line is not None and end_line is not None:
        lines = lines[:start_line] + lines[end_line + 1:]

    with open(file_path, 'w') as file:
        file.writelines(lines)

# Usage example
folder_path = '/Users/akhilesh.b/Desktop/nammayatri/Backend/app/provider-platform/dynamic-offer-driver-app/Main/src/Storage/Beam'
file_name = 'DriverFlowStatus'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.hs'):
        file_path = os.path.join(folder_path, file_name)
        remove_block_from_file(file_path, file_name)
