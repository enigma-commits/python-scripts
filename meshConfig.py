def replace_string_with_indentation(file_path):
    # Read the file contents
    print("here")
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    line_to_be_removed = ['let modelName', 'let updatedMeshConfig']
    words_to_be_removed = ["dbConf'", "updatedMeshConfig"]
    # Iterate over each line
    modified_lines = []
    for line in lines:
        f = False
        lineNew = line
        for content in line_to_be_removed:
            if content in line:
                f = True
                break
        if f: 
            continue
        for content in words_to_be_removed:
            if content in line:
                lineNew = lineNew.replace(content, "")
        if "L.getOption KBT.PsqlDbCfg" in lineNew:
                lineNew = lineNew.replace("L.getOption KBT.PsqlDbCfg", "getMasterDBConfig'")
        modified_lines.append(lineNew)
    # Join the modified lines back into a string
    modified_content = '\n'.join(modified_lines)
    for line in modified_content.splitlines():
        print(line)
    # Write the modified content back to the file
    # with open(file_path, 'w') as file:
    #     file.write(modified_content)

file_path = '/Users/akhilesh.b/Desktop/nammayatri/Backend/app/rider-platform/rider-app/Main/src/Storage/Queries/Booking.hs'
replace_string_with_indentation(file_path)