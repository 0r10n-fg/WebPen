import requests
from bs4 import BeautifulSoup

# Define the target URL
url = "http://example.com"

# Make a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Search for the presence of a common OSWP security weakness, such as an input field with the "password" type
password_input = soup.find("input", type="password")
if password_input:
    print("A password input field was found on the page.")
else:
    print("No password input field was found on the page.")

# Search for insecure cookies
if 'secure' not in response.headers.get('set-cookie','').lower() or 'httponly' not in response.headers.get('set-cookie','').lower():
    print("Insecure cookies found.")
else:
    print("No insecure cookies found.")

# Search for insecure file uploads
file_upload_form = soup.find("form", enctype="multipart/form-data")
if file_upload_form:
    file_upload_input = file_upload_form.find("input", type="file")
    if file_upload_input:
        print("Insecure file upload form found.")
    else:
        print("No insecure file upload form found.")
else:
    print("No insecure file upload form found.")

# Search for forms without CSRF protection
csrf_token = soup.find("input", {"name":"csrf_token"})
if not csrf_token:
    print("Forms without CSRF protection found.")
else:
    print("No forms without CSRF protection found.")

# Search for XSS vulnerabilities
script_tag = soup.find("script")
eval_func = soup.find(string=lambda text: 'eval' in text)
if script_tag or eval_func:
    print("XSS vulnerabilities found.")
else:
    print("No XSS vulnerabilities found.")

# Search for Insecure Direct Object Reference vulnerabilities
user_supplied_param = soup.find_all(href=lambda value: "id=" in value)
if user_supplied_param:
    print("Insecure Direct Object Reference vulnerabilities found.")
else:
    print("No Insecure Direct Object Reference vulnerabilities found.")

# Search for SQL injection vulnerabilities
sql_reserved_words = ['SELECT', 'UPDATE', 'DROP']
for word in sql_reserved_words:
    sql_input = soup.find(string=lambda text: word in text)
    if sql_input:
        print("SQL injection vulnerabilities found.")
        break
else:
    print("No SQL injection vulnerabilities found.")
