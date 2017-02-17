from random import randint
from termcolor import colored, cprint
from hangman_helpers import *
from hangman_beater import get_best_move

class SecretKeeper:
    def __init__(self):
        self.difficulty = self.get_difficulty()
        self.receivedWordsList = []
        self.word = self.get_word()
        self.wordLen = len(self.word)
        self.charMap = self.initialize_char_map()

    # return difficulty when a numeric number between 1 and 10 has been selected by user
    def get_difficulty(self):
        difficulty = input("Select difficulty (1-10) (input -help for assistance): ")
        while True:
            if difficulty == "-help":
                cprint("\n\n   Input a number between 1 and 10", "cyan", attrs=["bold"])
                cprint("   The generated word will be more complex if you put in a higher difficulty\n", "cyan", attrs=["bold"])
            if difficulty.isnumeric() and 0 < int(difficulty) < 11:
                break
            welcome_message()
            difficulty = input("Please put in a number between 1 and 10 (input -help for assistance): ")
        return int(difficulty)

    # GET word list from provided api, parse it, and select a random word from the list
    # throw error if requests library returns anything other than a 200 - "OK" - status code
    def get_word(self):
        payload = {"difficulty": self.difficulty}
        wordsResponse = make_api_request(payload)
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
    def __init__(self, secretKeeper, verbose):
        self.secretKeeper = secretKeeper
        self.currentBoard = ['_' for char in self.secretKeeper.word]
        self.wordsList = self.get_word_list()
        self.wordsListLen = len(self.wordsList)
        self.verbose = verbose
        self.guessedChars = {}
        self.incorrectCount = 0
        self.correctCount = 0

    def get_word_list(self):
        payload = {"minLength": self.secretKeeper.wordLen,
                   "maxLength": self.secretKeeper.wordLen + 1}
        wordsResponse = make_api_request(payload)
        return wordsResponse.text.split()

    # return 1 if correct guess, return 0 if incorrect guess or user error
    # user errors include guesses that are:
    # 	multiple characters and not a guess of the full word
    # 	no characters
    # 	characters that are not in the alphabet
    # 	uppercase letters
    # 	guesses that have already been guessed
    def make_guess(self, guess):
        ret = 0
        if (len(guess) != 1 and len(guess) != self.secretKeeper.wordLen) or not guess.isalpha() or not guess.islower():
            cprint("Incorrect input, submit '-help' for assistance.", "blue", attrs=["bold"])
        elif guess in self.guessedChars:
            cprint("You've already guessed that, try again.", "blue", attrs=["bold"])
        elif guess == self.secretKeeper.word:
            cprint("Correct guess!", "green", attrs=["bold"])
            self.guessedChars[guess] = 1
            self.correctCount = self.secretKeeper.wordLen
            ret = 1
        elif guess in self.secretKeeper.charMap:
            cprint("Correct guess!", "green", attrs=["bold"])
            self.guessedChars[guess] = 1
            self.correctCount += self.secretKeeper.charMap[guess]
            ret = 1
        else:
            cprint("Incorrect guess.", "red", attrs=["bold"])
            self.guessedChars[guess] = 1
            self.incorrectCount += 1
        return ret

    def print_game_area(self):
        self.print_guesses_remaining()
        self.print_hangman()
        self.print_current_board()

    def print_guesses_remaining(self):
        print("\nNumber of incorrect guesses remaining: " + str(6 - self.incorrectCount))

    def print_hangman(self):
        leftLeg = " " if self.incorrectCount < 1 else colored("/", "blue", attrs=["bold"])
        rightLeg = " " if self.incorrectCount < 2 else colored("\\", "blue", attrs=["bold"])
        body = " " if self.incorrectCount < 3 else colored("|", "red", attrs=["bold"])
        leftArm = " " if self.incorrectCount < 4 else colored("-", "red", attrs=["bold"])
        rightArm = " " if self.incorrectCount < 5 else colored("-", "red", attrs=["bold"])
        head = " " if self.incorrectCount < 6 else colored("O", "cyan", attrs=["bold"])
        incorrectGuesses = [word for word in self.guessedChars if word not in self.currentBoard and word != self.secretKeeper.word]
        pole = colored('|', "magenta", attrs=["bold"])
        cprint("     ___", "magenta")
        cprint("    /   |", "magenta")
        print("    {}   {}    Incorrect guesses:".format(head, pole))
        print("   {}{}{}  {}    {}".format(leftArm, body, rightArm, pole, incorrectGuesses))
        print("   {} {}  {}".format(leftLeg, rightLeg, pole))
        cprint("       ___\n", "magenta")

    def print_current_board(self):
        printBoard = [' ', ' ']
        for i in range(len(self.secretKeeper.word)):
            printBoard.append(self.currentBoard[i])
            printBoard.append(' ')
        printBoard.append('\n')
        print(''.join(printBoard))

    def print_help(self):
        cprint("\n   Select a letter to guess,", "cyan", attrs=["bold"])
        cprint("   try to guess the full word,", "cyan", attrs=["bold"])
        cprint("   or input '-best' to have the computer guess for you", "cyan", attrs=["bold"])

    def update_current_board(self, guess):
        if len(guess) > 1:
            self.currentBoard = [char for char in self.secretKeeper.word]
        else:
            for i in range(len(self.secretKeeper.word)):
                if self.secretKeeper.word[i] == guess:
                    self.currentBoard[i] = guess

if __name__ == '__main__':
    welcome_message()
    secretKeeper = SecretKeeper()
    gameBoard = GameBoard(secretKeeper, len(sys.argv) > 1 and sys.argv[1] == "-v")
    clear_screen()
    while secretKeeper.word:
        gameBoard.print_game_area()
        guess = input("Your guess (input '-help' for assistance): ")
        clear_screen()
        print()
        if guess == "-help":
            gameBoard.print_help()
            continue
        if guess == "-best":
            guess = get_best_move(gameBoard)
        if gameBoard.make_guess(guess):
            gameBoard.update_current_board(guess)

        if gameBoard.incorrectCount == 6 or gameBoard.correctCount == secretKeeper.wordLen:
            gameBoard.print_game_area()
            if gameBoard.incorrectCount == 6:
                print("You have lost!")
                print("The solution was '" + secretKeeper.word + "'.")
            else:
                print("You won!!")
            if playAgain():
                welcome_message()
                secretKeeper = SecretKeeper()
                gameBoard = GameBoard(secretKeeper, gameBoard.verbose)
            else:
                break
