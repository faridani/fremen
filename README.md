# Fremen AI

A local agentic AI for automating tasks and workflows

<img src="logo.png" alt=" logo" style="height: 300px;"/>

## Setup your environment 
in your anaconda prompt do the following 
```
conda create -n fremen python==3.11 python
conda activate fremen
pip install pyautogui
pip install opencv-python
pip install opencv-python-headless face_recognition numpy
pip install pandas 
pip install retina-face
pip install tf-keras
```



Install your package in development mode:

pip install -e .

Run the main script:

python main.py

Run tests:

python -m unittest discover tests
