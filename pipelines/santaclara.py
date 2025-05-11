import os
import random
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

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')


fremen = Fremen()
fremen.activate_chrome()
chrome_activated = fremen.activate_chrome()
fremen.wait(2)
if not chrome_activated:
    print("Failed to activate Chrome window.")
    quit()
results = []
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/names.txt')) as f:
    lines = [line for line in f]
    random.shuffle(lines)
    
    for nameString in lines:
        fremen.wait(5)

        file_path = os.path.join(base_dir,'new_tab_light.png')
        fremen.open_new_tab_on_chrome(file_path)
        fremen.wait(2)

        firstName, lastName = nameString.replace("\n","").split(" ")
        print(f"Collecting fisrtName={firstName} and lastName={lastName}")
        fremen.open_url(f'https://portal.scscourt.org/search/party?firstName={firstName}&lastName={lastName}')
        fremen.wait(20)
        fremen.click_and_wait(os.path.join(base_dir, 'party_search_request.png'), 10)
        content = fremen.select_all_and_return()
        cases = extract_number(content)

        print(f"{firstName} {lastName}: has {cases} cases")
        if cases==0:
            continue
        datefiled = fremen.ask(model="llama3.1:8b", question=f"when is the lastest filing date in this document: {content}")
        results.append({"firstName": firstName, "lastName": lastName, "cases": cases, "lastCaseFiled": datefiled})


for result in results:
    for key, value in result.items():
        print(f"{key}: {value}")
