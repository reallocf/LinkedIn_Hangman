from termcolor import colored, cprint
from hangman_printers import print_best

class CharPicker:
    def __init__(self):
        self.charMap = {}
        self.maxCount = 0
        self.pickedChar = ''

# remove guesses that absolutely CANNOT be the correct solution based on
# what is currently on the game board
def remove_incorrect_words(gameBoard):
    for i in range(len(gameBoard.currentBoard)):
        if gameBoard.currentBoard[i] == '_':
            gameBoard.wordsList = [word for word in gameBoard.wordsList
                                   if word[i] not in gameBoard.guesser.guessedChars]
        else:
            gameBoard.wordsList = [word for word in gameBoard.wordsList
                                   if word[i] == gameBoard.currentBoard[i]]

# loop through every char in every remaining word and return the letter that
# occurs in the most words
def select_which_char(gameBoard):
    charPicker = CharPicker()
    for word in gameBoard.wordsList:
        wordSet = set()
        for char in word:
            if char not in gameBoard.guesser.guessedChars and char not in wordSet:
                wordSet.add(char)
                charPicker.charMap[char] = charPicker.charMap.get(char, 0) + 1
                if charPicker.charMap[char] > charPicker.maxCount:
                    charPicker.pickedChar = char
                    charPicker.maxCount = charPicker.charMap[char]
    return print_best(gameBoard.wordsList, gameBoard.verbose, charPicker)

# the computer decides which is the right move and selects it for you
def get_best_move(gameBoard):
    remove_incorrect_words(gameBoard)
    if len(gameBoard.wordsList) == 1:
        return print_best(gameBoard.wordsList, gameBoard.verbose, gameBoard.wordsList[0])
    else:
        return select_which_char(gameBoard)
