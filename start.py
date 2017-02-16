import sys
from random import randint
import requests

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
                                 if word[i] in gameBoard.guesser.guessedChars]:
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
    charPicker = CharPicker()
    # loop through every char in every remaining word and return the letter with
    # the most total occurrences
    for word in gameBoard.wordsList:
        for char in word:
            if char not in gameBoard.guesser.guessedChars:
                if char in charPicker.charMap:
                    charPicker.charMap[char] += 1
                else:
                    charPicker.charMap[char] = 1
                if charPicker.charMap[char] > charPicker.maxCount:
                    charPicker.pickedChar = char
                    charPicker.maxCount = charPicker.charMap[char]
    return charPicker.pickedChar

class Guesser:
    def __init__(self, name):
        self.name = name
        self.guessedChars = {}
        self.incorrectCount = 0
        self.correctCount = 0

    # return 1 if correct guess, return 0 if incorrect guess or user error
    # user errors include guesses that are:
    # 	multiple characters
    # 	no characters
    # 	characters that are not in the alphabet
    # 	uppercase letters
    # 	guesses that have already been guessed
    def make_guess(self, charMap, guess):
        ret = 0
        if len(guess) != 1 or not guess.isalpha() or not guess.islower():
            print("Please input a single, lowercase letter.")
        elif guess in self.guessedChars:
            print("You've already guessed that, try again.")
        elif guess in charMap:
            print("Correct guess!")
            self.guessedChars[guess] = 1
            self.correctCount += charMap[guess]
            ret = 1
        else:
            print("Incorrect guess.")
            self.guessedChars[guess] = 1
            self.incorrectCount += 1
        return ret

    # resets info of self and returns whether or not user wants to play again
    def playAgain(self):
        self.guessedChars = {}
        self.incorrectCount = 0
        self.correctCount = 0
        while True:
            response = input("Play again? [y/n] ")
            if (response == "y" or response == "n"):
                break
        return True if response == "y" else False

class SecretKeeper:
    def __init__(self):
        self.difficulty = self.get_difficulty()
        self.receivedWordsList = []
        self.word = self.get_word()
        self.wordLen = len(self.word)
        self.charMap = self.initialize_char_map()

    # return difficulty when a numeric number between 1 and 10 has been selected by user
    def get_difficulty(self):
        difficulty = input("Select difficulty (1-10) ")
        while True:
            if difficulty.isnumeric() and 0 < int(difficulty) < 11:
                break
            difficulty = input("Please put in a number between 1 and 10 ")
        return int(difficulty)

    # GET word list from provided api, parse it, and select a random word from the list
    # throw error if requests library returns anything other than a 200 - "OK" - status code
    def get_word(self):
        apiEndPoint = "http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words"
        try:
            payload = {'difficulty': self.difficulty}
            wordsResponse = requests.get(apiEndPoint, payload)
            if wordsResponse.status_code != 200:
                raise
        except Exception as e:
            print("Error requesting from server.")
            print("Error: " + str(e))
            sys.exit()
        self.receivedWordsList = wordsResponse.text.split()
        selection = randint(0, len(self.receivedWordsList) - 1)
        return self.receivedWordsList[selection]

    def initialize_char_map(self):
        charMap = {}
        for i in range(self.wordLen):
            if self.word[i] in charMap:
                count = charMap[self.word[i]]
            else:
                count = 0
            charMap[self.word[i]] = count + 1
        return charMap

class GameBoard:
    def __init__(self, guesser, secretKeeper):
        self.guesser = guesser
        self.secretKeeper = secretKeeper
        self.currentBoard = ['_' for char in self.secretKeeper.word]
        self.wordsList = [word for word in self.secretKeeper.receivedWordsList
                          if len(word) == self.secretKeeper.wordLen]
        self.wordsListLen = len(self.wordsList)

    def print_current_board(self):
        printBoard = [' ', ' ']
        for i in range(len(self.secretKeeper.word)):
            printBoard.append(self.currentBoard[i])
            printBoard.append(' ')
        printBoard.append('\n')
        print(''.join(printBoard))

    def print_hangman(self):
        leftLeg = " " if self.guesser.incorrectCount < 1 else "/"
        rightLeg = " " if self.guesser.incorrectCount < 2 else "\\"
        body = " " if self.guesser.incorrectCount < 3 else "|"
        leftArm = " " if self.guesser.incorrectCount < 4 else "-"
        rightArm = " " if self.guesser.incorrectCount < 5 else "-"
        head = " " if self.guesser.incorrectCount < 6 else "O"

        print("     ___")
        print("    /   |")
        print("    {}   |     All guesses:".format(head))
        print("   {}{}{}  |     {}".format(leftArm, body, rightArm,
                                           list(self.guesser.guessedChars)))
        print("   {} {}  |".format(leftLeg, rightLeg))
        print("       ___\n")

    def print_game_area(self):
        self.print_hangman()
        self.print_current_board()

    def update_current_board(self, guess):
        for i in range(len(self.secretKeeper.word)):
            if self.secretKeeper.word[i] == guess:
                self.currentBoard[i] = guess

# insert color - turtle library
# understand errors better

if __name__ == '__main__':
    print("Welcome to Hangman!")
    guesser = Guesser(input("Your name: "))
    secretKeeper = SecretKeeper()
    gameBoard = GameBoard(guesser, secretKeeper)

    while True:
        gameBoard.print_game_area()
        guess = input("Your guess: ")

        if guess == "best":
            guess = get_best_move(gameBoard)
        if guesser.make_guess(secretKeeper.charMap, guess):
            gameBoard.update_current_board(guess)

        if guesser.incorrectCount == 6 or guesser.correctCount == secretKeeper.wordLen:
            gameBoard.print_game_area()
            if guesser.incorrectCount == 6:
                print("You have lost!")
                print('The solution was "' + secretKeeper.word + '".')
            else:
                print("You won!!")
            if guesser.playAgain():
                secretKeeper = SecretKeeper()
                gameBoard = GameBoard(guesser, secretKeeper)
            else:
                break
