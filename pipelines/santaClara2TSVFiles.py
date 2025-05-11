
import os
from fremen import Fremen, extract_json
import pandas as pd

contentbegin = """
View	Case Number	Case Style	Case Status	Case Type	Filing Date
"""
contentend = """
Showing 
"""


def extract_between_multilines(start: str, end: str, large_string: str):
    import re

    # Escape special regex characters in the multiline strings
    start_pattern = re.escape(start.strip())
    end_pattern = re.escape(end.strip())

    # Create a regex pattern to find text between the start and end patterns
    pattern = rf"{start_pattern}(.*?){end_pattern}"

    # Use re.DOTALL to match across multiple lines
    matches = re.findall(pattern, large_string, re.DOTALL)

    return matches

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
attorney_list = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data\\attorney_list.tsv')
data = pd.read_csv(attorney_list, sep='\t')



fremen = Fremen()
fremen.activate_chrome()
chrome_activated = fremen.activate_chrome()
if not chrome_activated:
    print("Failed to activate Chrome window.")
with open("santa-clara-attorney-data.tsv", "a") as file:
    for row in data.sample(frac=1).itertuples():
        print("============================================")
        print(f"{row.Index}, {row.Attorney_id}, {row.Name}")
        name = row.Name
        id = row.Attorney_id
    
        try:
            firstName, lastName = name.replace("\n","").split(" ")
            fremen.wait(2)
            fremen.open_new_tab_on_chrome(os.path.join(base_dir, 'new_tab_light.png'))
            fremen.wait(2)
            print(f"Collecting fisrtName={firstName} and lastName={lastName}")
            fremen.open_url(f'https://portal.scscourt.org/search/party?firstName={firstName}&lastName={lastName}')
            fremen.wait(4)
            # fremen.click_and_wait(os.path.join(base_dir, 'party_search_request.png'), 4, confidence=.7)
            content = fremen.select_all_and_return()
            filename = f"attorney_tsv_cases\\Attorney_{str(id)}.tsv"
            with open(filename, 'w') as tsvfile:
                results = extract_between_multilines(contentbegin, contentend, content)
                text = "\n".join([s for s in results[0].splitlines() if (s!=os.linesep and s!="\n" and s!=" ")])
                tsvfile.writelines(text)
            file.write(f"{id}\tSuccess\t{name}\t{filename}\n")
            file.flush()
        except KeyboardInterrupt:
            file.write(f"{id}\tFailed\t{name}\t\n")
            file.flush()
            quit()
        except Exception as e:
            try:
                file.write(f"{id}\tFailed\t{name}\t\t{repr(e)}\n")
            except UnicodeEncodeError:
                pass
            print(str(e))
            print(repr(e))
            file.flush()


        
quit()
