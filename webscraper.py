
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep

def getVersions(browser: webdriver.Edge):
    versionLinks =[]
    try:
        browser.find_element(By.XPATH, '/html/body/div/main/div/article[1]/div[1]/nav/div/div/div').click()
        versions = browser.find_elements(By.XPATH, '/html/body/div/main/div/article[1]/div[1]/nav/div/ul/li')
        for version in versions:
            link = version.find_element(By.TAG_NAME, 'a').get_attribute('href')
            versionLinks.append(link)
    except (NoSuchElementException, ElementClickInterceptedException):
        versionLinks.append(browser.current_url)
    
    return versionLinks


browser = webdriver.Edge()
output = {}
linksToIndex = []

browser.get(f'https://db.pokemongohub.net/pokemon/0')
sleep(2)
browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div/div[2]').click()

for i in range(1,1026):
    
    #hande some edge cases
    match i:
        case 386:
            browser.get('https://db.pokemongohub.net/pokemon/386-Normal')
        case 422:
            browser.get('https://db.pokemongohub.net/pokemon/422-East_Sea')
        case 423:
            browser.get('https://db.pokemongohub.net/pokemon/423-East_Sea')
        case 487:
            browser.get('https://db.pokemongohub.net/pokemon/487-Origin')
        case 493:
            browser.get('https://db.pokemongohub.net/pokemon/493-Bug')
        case 649:
            browser.get('https://db.pokemongohub.net/pokemon/649-Normal')
        case 720:
            browser.get('https://db.pokemongohub.net/pokemon/720-Confined')
        case 1017:
            browser.get('https://db.pokemongohub.net/pokemon/1017-Cornerstone_Mask')
        case 1024:
            browser.get('https://db.pokemongohub.net/pokemon/1024-Normal')
        case _:
            browser.get(f'https://db.pokemongohub.net/pokemon/{i}')
    
    linksToIndex.append(getVersions(browser))

for links in linksToIndex:
    print(str(links) + ',')

for links in linksToIndex:
    for link in links:
        browser.get(link)
        
        name = browser.find_element(By.ID, 'overview-and-stats').text
        evos = []
        
        try:
            table = browser.find_elements(By.XPATH, '/html/body/div/main/div/article[5]/div/table/tbody/tr')
        except NoSuchElementException:
            table = []
            
        for row in table:
            try:
                evos.pop()
            except IndexError:
                pass
            evos.append(row.find_element(By.XPATH, './td[1]/a/span').text)
            evos.append(row.find_element(By.XPATH, './td[3]/a/span').text)
        
        output.update({name: {'link': link, 'evos': evos}})

browser.quit()

with open('index.json', 'w') as file:
    data = json.dump(output,file, indent=4)

#{
#   name: {
#       link: 'URL'
#       evos: [*evo1, *evo2, *evo3]
#    }
#}