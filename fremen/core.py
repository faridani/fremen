
import pyautogui
import time
import pygetwindow as gw
import os
import json
import ollama
import pyperclip
import re
import json
import cv2 
from retinaface import RetinaFace
from PIL import Image
import numpy as np

def clean_string(text):
    # Remove extra newlines and spaces while preserving the JSON structure
    lines = text.split('\n')
    # Remove empty lines and strip each line
    lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(lines)

def extract_json(text):
    # Clean the text first
    text = clean_string(text)
    
    # Find content between ```json and ``` using regex
    # json_match = re.search(r'```json\s*(\[[\s\S]*?\])\s*```', text)
    json_match = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", text)
    json_match = re.search(r'```(?:json)?\s*(\[[\s\S]*?\])\s*```', text)

    if json_match:
        json_str = json_match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

class Fremen:
    def __init__(self):
        self.name = "Fremen"
    
    def greet(self):
        return f"Greetings from {self.name}!"
    

    # Function to bring Chrome to the foreground
    def activate_chrome(self):
        # Attempt to find the Chrome window
        chrome_windows = [w for w in gw.getAllWindows() if "Google Chrome" in w.title]

        if chrome_windows:
            chrome_windows[0].activate()
            return True
        else:
            print("Chrome window not found.")
            return False
        
        
    def click_and_wait(self,image_path: str, wait_time: int, confidence: int =0.9):
        clickable_area = pyautogui.locateOnScreen(image_path, confidence)
        if clickable_area:
            new_clickable_center = pyautogui.center(clickable_area)
            pyautogui.click(new_clickable_center)
            time.sleep(wait_time)
        else:
            print(image_path, "not found on page")

    def if_image_exists(image_path: str, wait_time:int, confidence = 0.7):
        if pyautogui.locateOnScreen(image_path, confidence):
            return True
        else:
            return False
        
    def wait(self, seconds: int):
        time.sleep(seconds)
    def press(self, key: str):
        pyautogui.press(key)

    def find_face(self, outputfile: str, name:str) -> None: 
        pyautogui.screenshot("delete_later.png")
        
        # Load the image
        image = cv2.imread("delete_later.png")
        if image is None:
            raise ValueError("Invalid image path provided!")
    
        faces = RetinaFace.extract_faces(img_path = "delete_later.png", align = False)
        """
        
        
        
        # Convert the image to grayscale for better detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=7, minSize=(25, 25))
        
        
        if len(faces) == 0:
           raise ValueError("No faces detected in the image!")
    
        # Assuming the first detected face is the one to crop
        x, y, w, h = faces[0]
    
        # Crop the image to the face
        cropped_image = image[y:y+h, x:x+w]
        

        # Save the cropped image
        cv2.imwrite(outputfile, cropped_image)
        """
        if len(faces) == 0:
           raise ValueError("No faces detected in the image!")
    
        cropped_image = Image.fromarray(faces[0].astype("uint8"))
        cropped_image.save(outputfile)
        clickable_area = pyautogui.locateOnScreen(outputfile, .9)

        if clickable_area:
            new_clickable_center = pyautogui.center(clickable_area)
            pyautogui.rightClick(new_clickable_center)
            
            
            base_dir = 'C:\\Users\\farid\\Desktop\\attorney_images\\'

            self.click_and_wait('C:\\Users\\farid\\Desktop\\Fremen\\images\\chrome_save_image_as.png',1,.9)
            pyautogui.typewrite(base_dir+name, interval=0.1)
            pyautogui.press('enter')
            time.sleep(1)
        else:
            print(outputfile, "not found on page")



    def find_on_screen_and_fill_with_text(self,image_path: str, text_content: str):
        # Locate the address bar on the screen using the screenshot
        new_tab_location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if new_tab_location:
            # Get the center of the located address bar
            new_tab_center = pyautogui.center(new_tab_location)
            
            # Click on the address bar
            pyautogui.click(new_tab_center)
            
            # Brief pause to ensure the address bar is ready for input
            time.sleep(3)
            # Type 'www.example.com' in the address bar

            for i in range(1,20):
                pyautogui.press('backspace')
            pyautogui.typewrite(text_content, interval=0.1)

        else:
            print(image_path, " not found")

    def open_new_tab_on_chrome(self, image_path: str):
        new_tab_location = pyautogui.locateOnScreen(image_path, confidence=0.7)
        if new_tab_location:
            # Get the center of the located address bar
            new_tab_center = pyautogui.center(new_tab_location)
                
            # Click on the address bar
            pyautogui.click(new_tab_center)


    def open_url(self, url: str):
        pyautogui.typewrite(url, interval=0.1)
        pyautogui.press('enter')

    def ask(self, model:str = 'llama3.1:8b', question:str = "Is the sky blue?", ollama_url:str = "http://localhost:11434/api/generate"):
        response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': question,
        },
        ])
        print(response['message']['content'])
        return response['message']['content']
    

    def select_all_and_return(self):
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        self.wait(2)
        #pyautogui.click()
        
        return pyperclip.paste()
