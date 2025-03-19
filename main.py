import PIL
import easyocr
import pyautogui
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from time import sleep


browser = webdriver.Edge()
browser.get("https://db.pokemongohub.net/pokemon/000")
browser.implicitly_wait(5)
accept = browser.find_element(By.XPATH, 'html/body/div[2]/div/div[2]/div[3]/div/div[2]')
accept.click()

def getAttackInfo(browser, name: str, *pokeType: str):

    browser.get("https://db.pokemongohub.net/pokemon/000")
    browser.implicitly_wait(5)

    search = browser.find_element(By.CLASS_NAME, "SearchBox_input__Wz5xz")
    search.click()
    sleep(1)
    search.send_keys(name)
    sleep(1)
    search.click()
    sleep(1)

    ActionChains(browser)\
        .send_keys(Keys.ARROW_DOWN)\
        .send_keys(Keys.ENTER)\
        .perform()

    sleep(1)

    currentURL = browser.current_url


    for char in currentURL[::-1]:
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]:
            break
        currentURL = currentURL[:-1]

    match pokeType:
        case 'shadow':
            currentURL += '-shadow'
        case 'mega':
            currentURL += '-mega'
        case 'dynamax':
            currentURL += '-dynamax'
        case 'gigantamax':
            currentURL += '-gigantamax'
        case _:
            pass


    browser.get(currentURL)

    attackRating = browser.find_elements(By.XPATH, '/html/body/div/main/div/article[1]/section/table/tbody/tr')

    attackRatings = []

    for element in attackRating:
        rating = element.find_element(By.XPATH, './td')
        attackRatings.append(rating.text.split('\n')[0])
        
    return attackRatings


for i in range(0,10):
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
    
    pyautogui.moveTo(2000, 740)
    pyautogui.dragRel(-500,0, duration=1)

    sleep(0.5)
browser.quit()
