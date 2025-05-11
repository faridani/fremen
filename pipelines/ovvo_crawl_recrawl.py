
import os
from fremen import Fremen, extract_json
import pandas as pd
from typing import Tuple, Set
import re 

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
attorney_list = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data\\attorney_list.tsv')
data = pd.read_csv(attorney_list, sep='\t')
folder_path = "C:\\Users\\farid\\Desktop\\Fremen\\ovvo-recrawl-set"
items = os.listdir(folder_path)
ids: Set[int] = set()

files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
for f in files:
    print(f"bro --> {f}")
    print(f.split("-"))
    match = re.search(r'\d+', f)
    id = int(match.group())
    ids.add(id)
    print(id)


folder_path = "C:\\Users\\farid\\Desktop\\attorney_images"
items = os.listdir(folder_path)

files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
for f in files:
    print(f"bro --> {f}")
    print(f.split("-"))
    match = re.search(r'\d+', f)
    id = int(match.group())
    ids.remove(id)
    print(id)

for item in ids:
    print(item)


fremen = Fremen()
fremen.activate_chrome()
chrome_activated = fremen.activate_chrome()
if not chrome_activated:
    print("Failed to activate Chrome window.")
with open("ovvo-attorney-data.tsv", "a") as file:
    for row in data.sample(frac=1).itertuples():
        print("============================================")
        print(f"{row.Index}, {row.Attorney_id}, {row.Name}")
        name = row.Name
        id = row.Attorney_id
        if id not in ids:
            continue
        try:
            fremen.wait(2)
            fremen.open_new_tab_on_chrome(os.path.join(base_dir, 'new_tab_light.png'))
            fremen.wait(2)
            fremen.open_url("https://www.avvo.com/")
            fremen.click_and_wait(os.path.join(base_dir, "ovvo_search.png"),1, confidence=0.7)
            fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, "ovvo_search_box.png"), name)
            fremen.press('enter')
            fremen.wait(3)
            fremen.click_and_wait(os.path.join(base_dir, "ovvo_view_profile.png"),2)
            filename = "-".join(name.split(" "))+"-id-"+str(id)
            fremen.find_face(os.path.join(base_dir, "test.png"),filename )
            content = fremen.select_all_and_return()
            free_consultation = True if 'Free Consultation' in content else False
            file.write(f"{id}\tSuccess\t{name}\t{free_consultation}\t{filename}\n")
            file.flush()
        except KeyboardInterrupt:
            file.write(f"{id}\tFailed\t{name}\t\t\n")
            file.flush()
            quit()
        except:
            try:
                file.write(f"{id}\tFailed\t{name}\t\t\n")
            except UnicodeEncodeError:
                pass
            file.flush()


        
quit()

