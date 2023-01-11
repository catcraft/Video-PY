import os
import shutil

# Get the path to the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "files" folder
files_dir = os.path.join(current_dir, 'files')

# Get a list of all files in the "files" folder
files = os.listdir(files_dir)

# Create a variable for documents directory of the current user
user_doc = os.path.join(os.environ['USERPROFILE'], 'Documents')

# Construct the path to the "py" folder in the user's Documents directory
py_dir = os.path.join(user_doc, 'py')

# Create the "py" folder if it doesn't exist
os.makedirs(py_dir, exist_ok=True)

# Iterate through the files in the "files" folder
for file in files:
    # Construct the full path to the current file
    file_path = os.path.join(files_dir, file)
    # Construct the full path to the file's destination
    dest_path = os.path.join(py_dir, file)
    # Check if the file already exists in the "py" folder
    if os.path.isfile(dest_path):
        # If it exists, skip the file
        print(f"{file} already exists in {py_dir}, skipping.")
        continue
    # Otherwise, copy the file
    shutil.copy(file_path, py_dir)
    print(f"{file} has been copied to {py_dir}")
