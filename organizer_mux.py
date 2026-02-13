import os
import shutil

# The path to the Downloads folder
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

# Listing files
files = os.listdir(downloads_path)

# Searching for files and coming to their respective folders
for file in files:
    path_complete = os.path.join(downloads_path, file)
    
    if os.path.isfile(path_complete):
        name, extension = os.path.splitext(file)
        
        if extension:
            folder_extension = os.path.join(downloads_path, extension[1:].upper())
            
            if not os.path.exists(folder_extension):
                os.makedirs(folder_extension)

            new_path = os.path.join(folder_extension, file)
            shutil.move(path_complete, new_path)