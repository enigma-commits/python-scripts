import os
import re

def remove_comments(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Remove lines with single-line comments starting with --
    content_without_comments = [line for line in content if not line.strip().startswith('--')]

    # Write the content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content_without_comments)

def process_files(folder_path):
    # Iterate over all files and directories in the given folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Process only files with .hs extension (modify as needed)
            if file.endswith('.hs'):
                remove_comments(file_path)


# Example usage
folder_path = '/Users/akhilesh.b/Desktop/nammayatri/Backend/app/provider-platform/dynamic-offer-driver-app/Main/src/Storage/Beam/'
process_files(folder_path)
