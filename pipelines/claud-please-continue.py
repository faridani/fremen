# claud-please-continue.py
# this script will keep sending "Please continue" to claude until it stops
# 
import os
from fremen import Fremen, extract_json
import pandas as pd
from typing import Tuple, Set
import re 

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')


fremen = Fremen()
while True:
    
    fremen.find_on_screen_and_fill_with_text(os.path.join(base_dir, "reply-to-claude.png"), "Please continue")
    fremen.press('enter')
    fremen.wait(5*60)

quit()
