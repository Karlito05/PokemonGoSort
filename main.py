import PIL
import PIL.Image
import PIL.ImageGrab
import easyocr
import pyautogui
import json
import numpy as np
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
        self.attacksCompDict = {'Unknown': 0, 'Not Ranked': 0, 'F Tier': 1, 'D Tier': 2, 'C Tier': 3, 'B Tier': 4, 'A Tier': 5, 'A+ Tier': 6, 'S Tier': 7}
        
        self.browser.get(f'https://db.pokemongohub.net/pokemon/0')
        sleep(2)
        self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div/div[2]').click()
        
    def getData(self, fileName: str) -> dict:
        with open(fileName, 'r') as file:
            return json.load(file)
    
    def getName(self) -> str:
        image = PIL.ImageGrab.grab(bbox= (1700, 600, 2150, 640))
        image.save('./image.png', 'PNG')
        name = self.reader.readtext('image.png', detail = 0)[0]
        return name
    
    def search(self, searchTerm: str) -> None:
        pyautogui.click(1900, 300)
        sleep(1)
        self.keyboard.type(searchTerm)
        sleep(0.5)
        self.click(2150, 850)
    
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
    
    def getPokemonInfo(self, name: str ,isShadow: bool) -> tuple[list[str], list[str], bool]:
            
        if isShadow:
            try:
                self.browser.get(self.pokeLookup['Shadow ' + self.pokeLookup[name]['evos'][-1]]['link'])
                if self.pokeLookup[name]['evos'][-1] == name:
                    afterEvolution = False
                else:
                    afterEvolution = True
            except IndexError:
                self.browser.get(self.pokeLookup[name]['link'])
                afterEvolution = False
        else:
            try:
                self.browser.get(self.pokeLookup[self.pokeLookup[name]['evos'][-1]]['link'])
                if self.pokeLookup[name]['evos'][-1] == name:
                    afterEvolution = False
                else:
                    afterEvolution = True
            except IndexError:
                self.browser.get(self.pokeLookup[name]['link'])
                afterEvolution = False
                
        ratings = []
        
        for row in self.browser.find_elements(By.XPATH, '/html/body/div/main/div/article[1]/section/table/tbody/tr'):
            ratings.append(row.find_element(By.XPATH, './td').text.split('\n')[0])
            
        goodAttacks = [] 
        goodAttacks.append(self.browser.find_element(By.XPATH, '/html/body/div/main/div/article[2]/section/table/tbody/tr[1]/td[2]/a'))
        goodAttacks.append(self.browser.find_element(By.XPATH,'/html/body/div/main/div/article[2]/section/table/tbody/tr[1]/td[3]/a'))
        return (ratings, goodAttacks, afterEvolution)
    
    def setTag(self, attacks: list[str], afterEvolution: bool=False , hasBadAttack: bool=False) -> None:
        pyautogui.moveTo(2145, 1275)
        sleep(0.15)
        pyautogui.click()
        sleep(0.5)
        pyautogui.moveTo(2150, 825)
        sleep(0.15)
        pyautogui.click()
        sleep(0.5)
        pyautogui.moveTo(1900,1100)
        sleep(0.5)
        pyautogui.dragRel(0,-500, duration=0.3)
        sleep(1.5)
        
        pyautogui.moveTo(1800,1000)
        sleep(0.15)
        pyautogui.click()
        
        if hasBadAttack:
            pyautogui.moveTo(1800,900)
            sleep(0.15)
            pyautogui.click()
        
        if afterEvolution:
            pyautogui.moveTo(1800,800)
            sleep(0.15)
            pyautogui.click()
        
        pyautogui.dragRel(0,100, duration=1)
        sleep(2.5)

        rankType = False
        match len(attacks):
            case 3:
                rankType = True
                
                if self.attacksCompDict[attacks[2]] == 0:
                    attacks[2] = 'N Tier'
            case 4:
                rankType = True
                typeAttack1 = self.attacksCompDict[attacks[2]]
                typeAttack2 = self.attacksCompDict[attacks[3]]
                
                if typeAttack1 > typeAttack2:
                    attacks.pop()
                else:
                    attacks.pop(-2)
                    print(attacks)
            case _:
                pass
        
        if attacks[0] not in ['S Tier', 'A+ Tier', 'A Tier', 'B Tier', 'C Tier', 'D Tier', 'F Tier']:
            attacks[0] = 'N Tier'

        if attacks[1] not in ['S Tier', 'A+ Tier', 'A Tier', 'B Tier', 'C Tier', 'D Tier', 'F Tier']:
            attacks[1] = 'N Tier'
        try:
            if attacks[3] not in ['S Tier', 'A+ Tier', 'A Tier', 'B Tier', 'C Tier', 'D Tier', 'F Tier']:
                attacks[3] = 'N Tier'
        except IndexError:
            pass
        image = PIL.ImageGrab.grab(bbox=(1600, 80, 2225, 1350))
        image.save('image.png', 'PNG')
        
        if rankType:
            for tag in self.reader.readtext('./image.png'):
                match attacks[2]:
                    case 'S Tier':
                        if tag[1] == 'S-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'A+ Tier':
                        if tag[1] == 'A+-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'A Tier':
                        if tag[1] == 'A-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'B Tier':
                        if tag[1] == 'B-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'C Tier':
                        if tag[1] == 'C-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'D Tier':
                        if tag[1] == 'D-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case 'F Tier':
                        if tag[1] == 'F-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
                    case _:
                        if tag[1] == 'N-Type':
                            pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                            sleep(0.15)
                            pyautogui.click()
        pyautogui.dragRel(0,245, duration=1)
        sleep(2.5)

        image = PIL.ImageGrab.grab(bbox=(1600, 80, 2225, 1350))
        image.save('image.png', 'PNG')

        for tag in self.reader.readtext('./image.png'):
            match attacks[1]:
                case 'S Tier':
                    if tag[1] == 'S-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'A+ Tier':
                    if tag[1] == 'A+-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'A Tier':
                    if tag[1] == 'A-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'B Tier':
                    if tag[1] == 'B-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'C Tier':
                    if tag[1] == 'C-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'D Tier':
                    if tag[1] == 'D-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'F Tier':
                    if tag[1] == 'F-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case _:
                    if tag[1] == 'N-Defense':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()

        pyautogui.dragRel(0,240, duration=1)
        sleep(2.5)

        image = PIL.ImageGrab.grab(bbox=(1600, 80, 2225, 1350))
        image.save('image.png', 'PNG')

        for tag in self.reader.readtext('./image.png'):
            match attacks[0]:
                case 'S Tier':
                    if tag[1] == 'S-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'A+ Tier':
                    if tag[1] == 'A+-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'A Tier':
                    if tag[1] == 'A-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'B Tier':
                    if tag[1] == 'B-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'C Tier':
                    if tag[1] == 'C-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'D Tier':
                    if tag[1] == 'D-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case 'F Tier':
                    if tag[1] == 'F-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                case _:
                    if tag[1] == 'N-Attack':
                        pyautogui.moveTo(tag[0][0][0].item() + 1600, tag[0][0][1].item() + 80)
                        sleep(0.15)
                        pyautogui.click()
                        
        pyautogui.moveTo(1900,1150)
        sleep(0.15)
        pyautogui.click()

    def getTextFromScreen(self, bbox: tuple[int,int,int,int]) -> str:
            image = PIL.ImageGrab.grab(bbox=bbox)
            image.save('image.png', 'PNG')

            return self.reader.readtext('image.png', detail = 0)[0]

    def click(self, x:int, y:int):
        pyautogui.moveTo(x,y)
        sleep(0.15)
        pyautogui.click()

    def mainLoop(self) -> None:
        print('We are faching')
        
        self.search('torank&!shadow')
        sleep(0.5)
        itorations = int(self.getTextFromScreen((1895,185,1945, 205)).replace('(', '').replace(')', '').split(' ')[-1])
        
        for i in range(0,itorations):
            sleep(0.5)
            self.click(1700,500)
            sleep(0.5)
            name = self.getName()
            hasAttacks = self.getAttacks()
            try:
                ratings, goodAttacks, afterEvolution = self.getPokemonInfo(name, False)
            except KeyError:
                self.click(1920, 1273)
                continue
            if not afterEvolution:
                if hasAttacks == goodAttacks:
                    hasGoodAttacks = True
                else:
                    hasGoodAttacks = False
            else:
                hasGoodAttacks= True # Possibly :')
            
            self.setTag(ratings,afterEvolution ,not(hasGoodAttacks))
            self.click(1920, 1273)

        self.click(1670, 285)

        self.search('torank&&shadow')
        sleep(0.75)
        itorations = int(self.getTextFromScreen((1895,185,1945, 205)).replace('(', '').replace(')', '').split(' ')[-1])
        
        for i in range(0,itorations):
            self.click(1700,500)
            sleep(0.5)
            name = 'Shadow ' + self.getName()
            hasAttacks = self.getAttacks()
            try:
                ratings, goodAttacks, afterEvolution = self.getPokemonInfo(name, True)
            except KeyError:
                self.click(1920, 1273)
                continue
            if not afterEvolution:
                if hasAttacks == goodAttacks:
                    hasGoodAttacks = True
                else:
                    hasGoodAttacks = False
            else:
                hasGoodAttacks= True # Possibly :')
            
            self.setTag(ratings,afterEvolution ,not(hasGoodAttacks))
            self.click(1920, 1273)
        self.browser.quit()

if __name__ == '__main__':
    ps = pokeSort()
    ps.mainLoop()