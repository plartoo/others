from random import randint
import time

import pyautogui

width, height = pyautogui.size()
while True:
    pyautogui.click(int(width/2), int(height/2))
    # pyautogui.click(randint(0,width), randint(0,height))
    # pyautogui.moveTo(randint(0,width), randint(0,height), duration=0.25)
    time.sleep(5)