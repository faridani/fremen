
import time
import os
from fremen import Fremen, extract_json
import re

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

def extract_number(text):
    # Find number between "of" and "entries"
    match = re.search(r'of (\d+) entries', text)
    if match:
        return int(match.group(1))
    return None


def extract_first_entry(text):
    # Skip the header line
    lines = text.split('\n')
    if len(lines) < 2:
        return None
    
    # Get the first data line
    data_line = lines[1]
    
    # Define the pattern to match the structure
    pattern = r'([A-Za-z]+)([A-Za-z]+)([A-Za-z.]+)([A-Za-z\s]+VS [A-Za-z]+)([0-9A-Z]+)([A-Z]+)(\d{2}/\d{2}/\d{4})'
    
    match = re.search(pattern, data_line)
    if match:
        return {
            'LastName': match.group(1),
            'FirstName': match.group(2),
            'MiddleName': match.group(3),
            'CaseName': match.group(4).strip(),
            'CaseNumber': match.group(5),
            'Type': match.group(6),
            'DateFiled': match.group(7)
        }
    return None

lawyers = [{'firstName': 'Donna', 'lastName': 'Gibbs'},
{'firstName': 'Katharine', 'lastName': 'Hooker'},
{'firstName': 'Debra', 'lastName': 'Schoenberg'}]
"""
{'firstName': 'Terry', 'lastName': 'Szucsko'},
{'firstName': 'Charles', 'lastName': 'DeLacey'},
{'firstName': 'Gina Marie', 'lastName': 'Mariani'},
{'firstName': 'Lita Annette', 'lastName': 'Pettusdotson'},
{'firstName': 'Richard', 'lastName': 'Flanders'},
{'firstName': 'Gregory Allen', 'lastName': 'Silva'},
{'firstName': 'John Lloyd', 'lastName': 'Adams'},
{'firstName': 'Robert A', 'lastName': 'Goodman'},   
{'firstName': 'Robert', 'lastName': 'Goodman'},
{'firstName': 'Dina', 'lastName': 'Keiser'},
{'firstName': 'David', 'lastName': 'Keiser'},
{'firstName': 'Debra', 'lastName': 'Hopper'},
{'firstName': 'Gerard A', 'lastName': 'Falzone'},
{'firstName': 'Gina', 'lastName': 'Silva'}]
"""


fremen = Fremen()
fremen.wait(20)
results = []

for lawyer in lawyers:
    first_name = lawyer['firstName']
    last_name = lawyer['lastName']
    print(f"searching for {lawyer['firstName']} {lawyer['lastName']}")

    fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, 'first_name.png'), first_name)
    fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, 'last_name.png'), last_name)
    fremen.click_and_wait(os.path.join(base_dir, 'submit.png'), 10)
    fremen.wait(20)
    fremen.click_and_wait(os.path.join(base_dir, 'name_search.png'), 10)
    content = fremen.select_all_and_return()
    print(content)
    cases = extract_number(content)

    print(f"{first_name} {last_name}: has {cases} cases")
    datefiled = fremen.ask(model="llama3.1:8b", question=f"when is the lastest filing date in this document: {content}")
    results.append({"firstName": first_name, "lastName": last_name, "cases": cases, "lastCaseFiled": datefiled})


for result in results:
    for key, value in result.items():
        print(f"{key}: {value}")


quit()

"""

"""
fremen.activate_chrome()
chrome_activated = fremen.activate_chrome()
if not chrome_activated:
    print("Failed to activate Chrome window.")

fremen.wait(2)
fremen.open_new_tab_on_chrome(os.path.join(base_dir, 'new_tab_light.png'))
fremen.wait(2)
fremen.open_url("https://www.google.com/")
query = "family lawyer in alameda county"
fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, 'google_search.png'), query)
fremen.press('enter')
fremen.wait(3)
content = fremen.select_all_and_return()
print(content)
lawyers = fremen.ask(model="llama3.1:8b", question=f"find the first name and the last name of every laywer presented in the folloiwng content and return as list of first names and last names: {content}")
print(lawyers)
json_lawyers = fremen.ask(model="llama3.1:8b", question=f"convert the following list of first names and last names to json format: {lawyers}")
print(json_lawyers)
lawyers_list = extract_json(json_lawyers)
for lawyer in lawyers_list:
    print(lawyer)

fremen.wait(10)
fremen.open_new_tab_on_chrome("https://eportal.alameda.courts.ca.gov/?q=Login")
fremen.wait(2)
fremen.click_and_wait(os.path.join(base_dir, 'alameda_county_login.png'), 5)


