import re
import os

# List of regular expressions to search for
patterns = [
    r"SQL injection",
    r"Cross-site scripting (XSS)",
    r"File inclusion",
    r"Command injection",
    r"Cross-site request forgery (CSRF)",
    r"Unvalidated redirects and forwards"
]

# A dictionary to store the results
results = {}

# A function to check a file for vulnerabilities
def check_file(file):
    with open(file, "r") as f:
        source_code = f.read()
        for pattern in patterns:
            match = re.search(pattern, source_code)
            if match:
                if file not in results:
                    results[file] = []
                results[file].append(match.group())

# A function to search a directory for files
def search_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                check_file(os.path.join(root, file))

# Ask the user for the directory to search
directory = input("Enter the directory to search: ")

# Search the directory for files
search_directory(directory)

# Print the results
for file in results:
    print(f"Possible vulnerabilities found in {file}:")
    for vulnerability in results[file]:
        print(f"- {vulnerability}")
