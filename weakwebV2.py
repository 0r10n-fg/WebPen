import requests
from bs4 import BeautifulSoup

def check_password_input(soup):
    password_input = soup.find("input", type="password")
    if password_input:
        return True, "Password input found."
    return False, "No password input found."

def check_cookies(headers):
    cookies = headers.get('set-cookie','')
    if 'secure' not in cookies.lower() or 'httponly' not in cookies.lower():
        return True, "Insecure cookies found."
    return False, "No insecure cookies found."

def check_file_uploads(soup):
    file_upload_form = soup.find("form", enctype="multipart/form-data").find("input", type="file")
    if file_upload_form:
        return True, "Insecure file upload form found."
    return False, "No insecure file upload form found."

def check_csrf_protection(soup):
    csrf_token = soup.find("input", {"name":"csrf_token"})
    if not csrf_token:
        return True, "Forms without CSRF protection found."
    return False, "No forms without CSRF protection found."

def check_xss_vulnerabilities(soup):
    script_tag = soup.find("script")
    eval_func = soup.find(string=lambda text: 'eval' in text)
    if script_tag or eval_func:
        return True, "XSS vulnerabilities found."
    return False, "No XSS vulnerabilities found."

def check_ido_vulnerabilities(soup):
    user_supplied_param = soup.find_all(href=lambda value: "id=" in value)
    if user_supplied_param:
        return True, "Insecure Direct Object Reference vulnerabilities found."
    return False, "No Insecure Direct Object Reference vulnerabilities found."

def check_sql_injection(soup):
    sql_reserved_words = ['SELECT', 'UPDATE', 'DROP']
    for word in sql_reserved_words:
        sql_input = soup.find(string=lambda text: word in text)
        if sql_input:
            return True, "SQL injection vulnerabilities found."
    return False, "No SQL injection vulnerabilities found."

# Define the target URL
url = "http://example.com"

# Make a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

vulns = [
    check_password_input,
    check_cookies,
    check_file_uploads,
    check_csrf_protection,
    check_xss_vulnerabilities,
    check_ido_vulnerabilities,
    check_sql_injection
]

for vuln in vulns:
    result, message = vuln(soup if vuln in [check_password_input, check_file_uploads, check_csrf_protection, check_xss_vulnerabilities, check_ido_vulnerabilities, check_sql_injection] else response.headers)
