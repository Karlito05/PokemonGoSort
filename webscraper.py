from selenium import webdriver
from selenium.webdriver.common.by import By

data = []

for i in range(0,10):
    
    if i < 10:
        istr = f"0{i}"
    else:
        istr = str(i)
        
    browser = webdriver.Edge()
    browser.get(f'https://db.pokemongohub.net/pokemon/0{istr}')

    name = browser.find_element(By.ID, 'overview-and-stats')
    data.append(name.text)
    
for i in data:
    print(i)