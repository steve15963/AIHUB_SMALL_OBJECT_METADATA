import re

# Define the file path
file_path = r'Z:\yolov9-main\data\train.txt'

# Function to remove non-ASCII characters from a file
def remove_non_ascii(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Use regex to remove all non-ASCII characters
    cleaned_content = re.sub(r'[^\x00-\x7F]+', '', content)
    return cleaned_content

# Clean the content and overwrite the original file
cleaned_content = remove_non_ascii(file_path)

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(cleaned_content)

print(f"Non-ASCII characters removed and saved back to {file_path}")
