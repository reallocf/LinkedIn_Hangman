import sys
import signal
from random import randint
from termcolor import colored, cprint
from hangman_helpers import exit_gracefully, clear_screen, input_looper, make_api_request
from hangman_printers import print_game_area, print_difficulty_help, print_guess_help
from hangman_best import get_best_move
from hangman_leaderboard import get_leaderboard, update_leaderboard

def play_game(verbose):
    welcome_message()
    guesser = Guesser()
    secretKeeper = SecretKeeper(guesser.difficulty)
    gameBoard = GameBoard(guesser, secretKeeper, verbose)
    clear_screen()
    while True:
        guess = input_looper(correct_guess, # loop until a valid guess is given by the user
                             "Your guess (input '-help' for assistance): ",
                             extraData = {"word": secretKeeper.word, "guessedChars": guesser.guessedChars,
                                          "statement": "Your guess (input '-help' for assistance): "},
                             start_function = print_game_area,
                             startParams = gameBoard,
                             middle_function = clear_screen,
                             flags = ['-help', '-best', '-v'],
                             flag_function = handle_guess_flag,
                             flagParams = {"gameBoard": gameBoard})
        if guesser.make_guess(guess, secretKeeper):
            secretKeeper.update_current_board(gameBoard, guess)
        if gameBoard.game_over():
            break
    if play_again(gameBoard):
        play_game(gameBoard.verbose)

def welcome_message():
    clear_screen()
    cprint("\n\n   Welcome to Hangman!\n\n", "yellow", attrs=["bold"])
    get_leaderboard()

def correct_guess(looper):
    incorrectInput = colored("Incorrect input, submit '-help' for assistance.", "blue", attrs=["bold"])
    alreadyGuessed = colored("You've already guessed that, try again.", "blue", attrs=["bold"])
    if (len(looper.ret) != 1 and len(looper.ret) != len(looper.data["word"])) or not looper.ret.isalpha() or not looper.ret.islower():
        looper.statement = incorrectInput + "\n\n" + looper.data["statement"]
    elif looper.ret in looper.data["guessedChars"]:
        looper.statement = alreadyGuessed + "\n\n" + looper.data["statement"]
    else:
        clear_screen()
        return True
    return False

def handle_guess_flag(looper):
    if looper.ret == "-help":
        print_guess_help()
    elif looper.ret == "-v":
        looper.flagParams["gameBoard"].verbose = not looper.flagParams["gameBoard"].verbose
        print("Verbose mode is now", "on" if looper.flagParams["gameBoard"].verbose else "off")
    else:
        looper.ret = get_best_move(looper.flagParams["gameBoard"])
        return True
    looper.statement = looper.data["statement"]
    return False

def play_again(gameBoard):
    def corr_input(looper):
        return True if looper.ret == "y" or looper.ret == "n" else False
    print_game_area(gameBoard)
    if gameBoard.guesser.incorrectCount == 6:
        print("You have lost!")
        print("The solution was '" + gameBoard.secretKeeper.word + "'.")
    else:
        print("You won!!")
        update_leaderboard()
    response = input_looper(corr_input, "\nPlay again? [y/n]: ")
    return True if response == "y" else False

class Guesser:
    def __init__(self):
        self.difficulty = self.get_difficulty()
        self.guessedChars = {}
        self.incorrectCount = 0
        self.correctCount = 0

    def get_difficulty(self):
        def corr_input(looper):
            if looper.ret.isnumeric() and 0 < int(looper.ret) < 11:
                looper.statement = "Please input a number between 1 and 10 (input -help for assistance): "
                return True
            else:
                False
        difficulty = input_looper(corr_input,
                                  "Select difficulty (1-10) (input -help for assistance): ",
                                  middle_function = welcome_message,
                                  flags = ['-help'],
                                  flag_function = print_difficulty_help)
        return int(difficulty)

    def make_guess(self, guess, secretKeeper):
        if guess == secretKeeper.word or guess in secretKeeper.charMap:
            cprint("Correct guess!", "green", attrs=["bold"])
            if guess == secretKeeper.word:
                self.correctCount = len(secretKeeper.word)
            else:
                self.guessedChars[guess] = 1
                self.correctCount += secretKeeper.charMap[guess]
            return True
        else:
            cprint("Incorrect guess.", "red", attrs=["bold"])
            self.guessedChars[guess] = 1
            self.incorrectCount += 1
            return False

class SecretKeeper:
    def __init__(self, difficulty):
        self.word = self.get_word(difficulty)
        self.charMap = self.initialize_char_map()

    # get random word from api response at given difficulty
    def get_word(self, difficulty):
        wordsResponse = make_api_request({"difficulty": difficulty})
        receivedWordsList = wordsResponse.text.split()
        return receivedWordsList[randint(0, len(receivedWordsList) - 1)]

    def initialize_char_map(self):
        charMap = {}
        for i in self.word:
            charMap[i] = charMap.get(i, 0) + 1
        return charMap

    def update_current_board(self, gameBoard, guess):
        if len(guess) > 1:
            gameBoard.currentBoard = [char for char in self.word]
        else:
            gameBoard.currentBoard = [char if char == guess or char in gameBoard.currentBoard
                                      else '_' for char in self.word]

class GameBoard:
    def __init__(self, guesser, secretKeeper, verbose):
        self.guesser = guesser
        self.secretKeeper = secretKeeper
        self.currentBoard = ['_' for char in self.secretKeeper.word]
        self.wordsList = make_api_request({"minLength": len(self.currentBoard),
                                           "maxLength": len(self.currentBoard) + 1}).text.split()
        self.verbose = verbose

    def game_over(self):
        return True if self.guesser.incorrectCount == 6 or self.guesser.correctCount == len(self.secretKeeper.word) else False

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    play_game(len(sys.argv) > 1 and sys.argv[1] == "-v")
