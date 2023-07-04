import os
import fileinput

# Folder path to be processed
folder_path = "/Users/akhilesh.b/Desktop/nammayatri/Backend/app/provider-platform/dynamic-offer-driver-app/Main/src/Storage/Queries/Booking"

# String to search for
search_string = "L.MonadFlow m"

# Replacement string
replacement_string = "(L.MonadFlow m, EsqDBFlow m r, HasFlowEnv m r '[\"tables\" ::: KVTables])"

# Process all files in the folder
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)

        # Process the file line by line and perform the replacement if found
        with fileinput.FileInput(file_path, inplace=True) as file:
            for line in file:
                line = line.replace(search_string, replacement_string)
                print(line, end="")
