from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Edge()


output = {}

for i in range(1007,1026):
    browser.get(f'https://db.pokemongohub.net/pokemon/{i}')
    browser.implicitly_wait(1)
    
    try:
        name = browser.find_element(By.ID, 'overview-and-stats')
        output.update({name.text: str(i)})
    except NoSuchElementException:
        pass

browser.quit()

with open('./index.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)