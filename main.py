import PIL
import PIL.Image
import PIL.ImageGrab
import easyocr
import pyautogui
import json
from pynput.keyboard import Controller
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from time import sleep

class pokeSort():
    def __init__(self):
        self.pokeLookup = self.getData('./pokemonlookup.json')
        self.possibleAttacks = self.getData('./attackLookup.json')
        self.browser = webdriver.Edge(); Options().add_argument('--headless')
        self.reader = easyocr.Reader(['en'])
        self.keyboard = Controller()
        
    def getData(self, fileName: str) -> dict:
        with open(fileName, 'r') as file:
            return json.load(file)
    
    def getName(self) -> str:
        image = PIL.ImageGrab.grab(bbox= (1700, 600, 2150, 630))
        image.save('./image.png', 'PNG')
        name = self.reader.readtext('image.png', detail = 0)[0]
        return name
    
    def search(self, searchTerm: str) -> None:
        pyautogui.click(1900, 300)
        sleep(2)
        self.keyboard.type(searchTerm)
        pyautogui.click(2150, 850)
    
    def getAttacks(self) -> list[str]:
        moveBy = 400
        attacks = []
        
        pyautogui.moveTo(1640, 1230)
        pyautogui.dragRel(0,-moveBy, duration=0.75)
        pyautogui.dragRel(0,-10, duration=0.2)

        image = PIL.ImageGrab.grab(bbox=(1600, 80, 2225, 1350))
        image.save('image.png', 'PNG')
        
        for string in self.reader.readtext('image.png', detail=0):
            if string in self.possibleAttacks['fast']:
                attacks.append(string)
        for string in self.reader.readtext('image.png', detail=0):
            if string in self.possibleAttacks['charge']:
                attacks.append(string)
        
        return attacks
    
    def getPokemonInfo(self, name: str) -> list[str]:
        try:
            self.browser.get(self.pokeLookup[self.pokeLookup[name]['evos'][-1]]['link'])
        except IndexError:
            self.browser.get(self.pokeLookup[name]['link'])
        attacks = []
        
        for row in self.browser.find_elements(By.XPATH, '/html/body/div/main/div/article[1]/section/table/tbody/tr'):
            attacks.append(row.find_element(By.XPATH, './td').text.split('\n')[0])
            
        return attacks
    
    def mainLoop(self) -> None:
        print('We are faching')
        self.browser.quit()

if __name__ == '__main__':
    ps = pokeSort()
    ps.mainLoop()