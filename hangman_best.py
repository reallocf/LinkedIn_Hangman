from termcolor import colored, cprint
from hangman_printers import verbose_print

class CharPicker:
    def __init__(self):
        self.charMap = {}
        self.maxCount = 0
        self.pickedChar = ''

# remove guesses that absolutely CANNOT be the correct solution based on what is known
def remove_incorrect_words(gameBoard):
    for i in range(gameBoard.secretKeeper.wordLen):
        # remove words where letters would have been filled based on guesses
        if gameBoard.currentBoard[i] == '_':
            for wordToRemove in [word for word in gameBoard.wordsList
                                 if word[i] in gameBoard.guessedChars]:
                gameBoard.wordsList.remove(wordToRemove)
                gameBoard.wordsListLen -= 1
        # remove words that don't have letters that have been filled by guesses
        else:
            for wordToRemove in [word for word in gameBoard.wordsList
                                 if word[i] != gameBoard.currentBoard[i]]:
                gameBoard.wordsList.remove(wordToRemove)
                gameBoard.wordsListLen -= 1

# the computer decides which is the right move and selects it for you via a decision tree
def get_best_move(gameBoard):
    remove_incorrect_words(gameBoard)
    if gameBoard.wordsListLen == 1:
        if gameBoard.verbose:
            print(colored("Words considered:\n", attrs=["bold"]), gameBoard.wordsList, "\n")
        print("Best selected: ", gameBoard.wordsList[0], "\n")
        return gameBoard.wordsList[0]
    charPicker = CharPicker()
    # loop through every char in every remaining word and return the letter with
    # the most total occurrences
    for word in gameBoard.wordsList:
        wordMap = {}
        for char in word:
            if char not in gameBoard.guessedChars and char not in wordMap:
                wordMap[char] = 1
                if char in charPicker.charMap:
                    charPicker.charMap[char] += 1
                else:
                    charPicker.charMap[char] = 1
                if charPicker.charMap[char] > charPicker.maxCount:
                    charPicker.pickedChar = char
                    charPicker.maxCount = charPicker.charMap[char]
    if gameBoard.verbose:
        verbose_print(gameBoard, charPicker)
    print("Best selected: ", charPicker.pickedChar)
    print("\nInput -v to toggle -best's verbose mode\n")
    return charPicker.pickedChar
