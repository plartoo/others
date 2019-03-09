import time
import argparse

import pyautogui

MINUTES = 8 * 60 # 8 hours
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('-m', type=int,
                    help='Minutes to click')
args = parser.parse_args()
t_end = time.time() + (60 * MINUTES)
if args.m is not None:
    t_end = time.time() + (60 * args.m)

width, height = pyautogui.size()
while time.time() < t_end: # while True:
    pyautogui.click(int(width/2), int(height/2))
    # pyautogui.click(randint(0,width), randint(0,height))
    # pyautogui.moveTo(randint(0,width), randint(0,height), duration=0.25)
    time.sleep(5)
