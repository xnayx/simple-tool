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
    def __init__(self, initPlayer, tableSize):
        self.players = { "X": self.blue('X'), "O": self.red('O') }

        self.tttConfig = {
            "board": self.createMatrix(tableSize, tableSize),
            "winner": None,
            "gameOver": False,
            "player": self.players[initPlayer]
        }

        self.winning_combinations = []

        self.positions = {}

        self.setPositions()
        print(self.positions)
        print(self.winning_combinations)
        self.setWinningCombinations()

    def setPositions(self):
        for iRow, row in enumerate(self.tttConfig["board"]):
            
            for iPos, pos in enumerate(row):
                self.positions[int(pos)] = [iRow, iPos]
    
    def setWinningCombinations(self):
        boardLength = len(self.tttConfig["board"])

        # rectas (filas/columnas)

        for i in range(boardLength):
            row = []
            column = []
            for j in range(boardLength):
                row.append(int(self.tttConfig["board"][i][j]))
                column.append(int(self.tttConfig["board"][j][i]))

            self.winning_combinations.append(row)
            self.winning_combinations.append(column)


        # diagonales (superior-derecha - inferior-izquierda / superior-izquierda - inferior-derecha)
        combination = []


        i, j = 0, 1

        while i < boardLength: # izq
            combination.append(i * boardLength + j)
            i += 1
            j += 1

        self.winning_combinations.append(combination)

        combination = []

        i, j = 0, boardLength

        while i < boardLength: # der
            combination.append(i * boardLength + j)
            i += 1
            j -= 1

        self.winning_combinations.append(combination)

    def createMatrix(self, rows, columns):
        matriz = []
        acc = 0

        for _ in range(rows):
            row = []
            for _ in range(columns):
                row.append(str(acc+1))
                acc += 1

            matriz.append(row)

        return matriz

    def blue(self, text):
        return Fore.BLUE + text + Fore.RESET

    def red(self, text):
        return Fore.RED + text + Fore.RESET

    def getPos(self, p):
        print(self.positions[p][1])
        return self.tttConfig["board"][self.positions[p][0]][self.positions[p][1]]

    def updateTable(self, pos):
        self.tttConfig["board"][pos[0]][pos[1]] = self.players["X"] if self.tttConfig["player"] == self.players["X"] else self.players["O"]
        self.tttConfig["player"] = self.players["O"] if self.tttConfig["player"] == self.players["X"] else self.players["X"]


        if any(all(self.getPos(p) == self.getPos(winning_combination[0]) for p in winning_combination) for winning_combination in self.winning_combinations):
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

        if not list(self.positions.keys()).count(position):
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

    def TicTacToe(self, initPlayer, tableSize):
        ttt = TicTacToe(initPlayer, tableSize)
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
            tableSize = int(input("Enter an table size: "))
            self.options.TicTacToe(self, player, tableSize)

        elif response == '3':
            Fore.RESET
            exit()

        else:
            print(Fore.RED+'Invalid option')
            Fore.RESET
            exit()

        self.returnToQuestions()

myTool().init()
