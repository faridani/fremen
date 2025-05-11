
import time
import os
from fremen import Fremen

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
print(base_dir)

fremen = Fremen()
fremen.activate_chrome()
print(fremen.greet())



# Activate the Chrome window
chrome_activated = fremen.activate_chrome()

if not chrome_activated:
    print("Failed to activate Chrome window.")

# Brief pause to ensure Chrome window is active
fremen.wait(2)
fremen.open_new_tab_on_chrome(os.path.join(base_dir, 'new_tab_light.png'))
fremen.wait(2)
fremen.open_url("https://en.wikipedia.org/wiki/Robert_Weisberg")
content = fremen.select_all_and_return()

speciality = fremen.ask(model="llama3.1:8b", question=f"find the specility of the lawyer in the following text, your answer should be in one sentence: {content}")
print(speciality)

exit()



