
import os
from fremen import Fremen, extract_json

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')


fremen = Fremen()
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
