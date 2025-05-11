
import os
from fremen import Fremen, extract_json
import pandas as pd

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
attorney_list = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data\\attorney_list.tsv')
data = pd.read_csv(attorney_list, sep='\t')



fremen = Fremen()
fremen.activate_chrome()
chrome_activated = fremen.activate_chrome()
if not chrome_activated:
    print("Failed to activate Chrome window.")
with open("ovvo-attorney-data.tsv", "a") as file:
    for row in data.itertuples():
        print(f"{row.Index}, {row.Attorney_id}, {row.Name}")
        name = row.Name
        id = row.Attorney_id
        try:
            fremen.wait(2)
            fremen.open_new_tab_on_chrome(os.path.join(base_dir, 'new_tab_light.png'))
            fremen.wait(2)
            fremen.open_url("https://www.avvo.com/")
            fremen.click_and_wait(os.path.join(base_dir, "ovvo_search.png"),1, confidence=0.7)
            fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, "ovvo_search_box.png"), name)
            fremen.press('enter')
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


"""
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

"""
