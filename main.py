import json
from colorama import Fore
from requests import get
from time import sleep
import os
from tabulate import tabulate
import random

# update 0.0.4

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class TicTacToe:
    def __init__(self, initPlayer):
        self.players = { "X": self.blue('X'), "O": self.red('O') }

        self.tttConfig = {
            "board": [
                ['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9']
            ],
            "winner": None,
            "gameOver": False,
            "player": self.players[initPlayer]
        }

        self.positions = {
            1: [0,0],
            2: [0,1],
            3: [0,2],
            4: [1,0],
            5: [1,1],
            6: [1,2],
            7: [2,0],
            8: [2,1],
            9: [2,2]
        }

    def blue(self, text):
        return Fore.BLUE + text + Fore.RESET

    def red(self, text):
        return Fore.RED + text + Fore.RESET

    def getPos(self, p):
        return self.tttConfig["board"][self.positions[p][0]][self.positions[p][1]]

    def updateTable(self, pos):
        self.tttConfig["board"][pos[0]][pos[1]] = self.players["X"] if self.tttConfig["player"] == self.players["X"] else self.players["O"]
        self.tttConfig["player"] = self.players["O"] if self.tttConfig["player"] == self.players["X"] else self.players["X"]

        winning_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]

        if any(self.getPos(p1) == self.getPos(p2) == self.getPos(p3) for p1, p2, p3 in winning_combinations):
            self.tttConfig["winner"] = self.players["X"] if self.tttConfig["player"] == self.players["O"] else self.players["O"]
            self.tttConfig["gameOver"] = True  

        if self.tttConfig["gameOver"]:
            clear()
            print(tabulate(self.tttConfig["board"], tablefmt="fancy_grid"))
            print(f'Game Over! {self.tttConfig["winner"]} won!')

        else:
            self.load()

    def load(self):
        clear()

        print(tabulate(self.tttConfig["board"], tablefmt="fancy_grid"))
        print('turn: '+str(self.tttConfig["player"]))

        position = int(input('Enter a position: '))
        
        if not [1,2,3,4,5,6,7,9].count(position):
            print(self.red('Invalid position'))
            sleep(2)
            self.load()

        else:
            if self.getPos(position) == self.players["X"] or self.getPos(position) == self.players["O"]:
                print(self.red('Position already taken'))
                sleep(2)
                self.load()

            else:
                self.updateTable(self.positions[position])


class options:
    def __init__(self, option):
        self.option = option

    def mdnSearch(self):
        clear()

        print(Fore.GREEN+'MDN is a JavaScript, CSS, and HTML5 documentation.\nit is a website that provides a search engine for JavaScript,\nCSS, HTML5, and APIs.\n\n')

        mdnSearching = input(Fore.BLUE+'Enter the text you want to search: ')
        mdnSearchResult = get(f'https://developer.mozilla.org/api/v1/search?q={mdnSearching}&locale=es')
        mdnResults = json.loads(mdnSearchResult.text)
        if len(mdnResults['documents']) <= 0:
            print(Fore.RED+'No results found')
            self.returnToQuestions()

        mdnResultsSorted = sorted(mdnResults['documents'], key=lambda k: k['popularity'], reverse=True)[0:11]

        titles = []
        for i in mdnResultsSorted:
            titles.append(f"Result: {i['title']} {Fore.CYAN}<|>{Fore.GREEN} More Info: {self.link('https://developer.mozilla.org/'+i['mdn_url'],'Click Here')}")

        print(Fore.MAGENTA+'First 10 results: '+Fore.GREEN)
        print('\n'.join(titles))

    def TicTacToe(self, initPlayer):
        ttt = TicTacToe(initPlayer)
        ttt.load()


class myTool:
    def __init__(self):
        self.options = options

    def link(self, uri, label=None):
        if label is None: 
            label = uri
        parameters = ''

        escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

        return escape_mask.format(parameters, uri, label)

    def returnToQuestions(self):
        r = input(Fore.BLUE+'return to questions?[Y/N]: ')

        if r.upper() == 'Y':
            self.init()

        elif r.upper() == 'N':
            Fore.RESET
            exit()

        else:
            print(Fore.RED+'invalid input')
            Fore.RESET
            exit()

    def init(self):
        clear()
        print(Fore.GREEN)
        print('[1] - MDN search')
        print('[2] - Tic Tac Toe game')
        print('[3] - exit'+Fore.RESET)

        response = input(Fore.BLUE+'\nEnter your selection here: ')

        if response == '1':
            print(Fore.RESET)
            self.options.mdnSearch(self)

        elif response == '2':
            print(Fore.RESET)
            player = random.choice(['X','O'])
            self.options.TicTacToe(self, player)

        elif response == '3':
            Fore.RESET
            exit()

        else:
            print(Fore.RED+'Invalid option')
            Fore.RESET
            exit()

        self.returnToQuestions()

myTool().init()
