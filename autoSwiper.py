from pynput.mouse import Button, Controller
import random
import time

mouse = Controller()

dislike = (1189, 1025)
like = (1346, 1017)


while True:
    choice = random.choice([like, dislike])
    
    mouse.position = choice
    mouse.click(Button.left, 1)
    
    time.sleep(3)