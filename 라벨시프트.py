import os

def modify_labels(directory):
    # Iterate through all the files in the specified directory
    for filename in os.listdir(directory):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        
        # Check if the file is a .txt file
        if filename.endswith(".txt"):
            # Open and read the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the first value of each line
            modified_lines = []
            for line in lines:
                values = line.split()
                if len(values) > 0:
                    # Convert the first value to integer, subtract 1, and convert back to string
                    values[0] = str(int(values[0]) - 1)
                    # Join the modified values back into a single line
                    modified_lines.append(' '.join(values) + '\n')

            # Write the modified lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)
            print(f"Modified file: {filename}")

# Directory containing the label files
label_directory = r"Z:\yolov9-main\train\labels"

# Call the function to modify the labels
modify_labels(label_directory)
