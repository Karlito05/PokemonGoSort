import PIL
import easyocr
import pyautogui
from time import sleep

isRunning = True
data = []

while isRunning:
    reader = easyocr.Reader(['en'])

    screenshot = PIL.ImageGrab.grab(bbox=[1650, 590, 2100, 635])
    screenshot.save("image.png")

    name = reader.readtext("image.png")[0][1]

    pyautogui.moveTo(1650, 690)
    pyautogui.dragTo(1650, 545, duration=1)
    pyautogui.click()

    sleep(1)

    screenshot = PIL.ImageGrab.grab(bbox=[1690, 1225, 1876, 1270])
    screenshot.save("image.png")

    attack1 = reader.readtext("image.png")[0][1]

    screenshot = PIL.ImageGrab.grab(bbox=[1690, 1260, 1876, 1320])
    screenshot.save("image.png")

    attack2 = reader.readtext("image.png")[0][1]

    data.append((name, (attack1, attack2)))
    
    pyautogui.moveTo(2000, 740)
    pyautogui.dragRel(-500,0, duration=1)

    sleep(2)

