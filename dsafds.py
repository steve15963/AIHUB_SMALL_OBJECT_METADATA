import os
import re

# Define the directory path
directory_path = r'Z:\yolov9-main\valid\labels'

# Function to remove non-ASCII characters from filenames
def clean_filenames(directory):
    for filename in os.listdir(directory):
        # Full path to the file
        file_path = os.path.join(directory, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Remove non-ASCII characters from the filename
            new_filename = re.sub(r'[^\x00-\x7F]+', '', filename)
            
            # Full path for the new filename
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file if the new filename is different
            if new_filename != filename:
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")

# Execute the function to clean filenames
clean_filenames(directory_path)

print("All filenames have been cleaned.")
