import sys
import os
import requests
from termcolor import colored, cprint
from hangman_best import get_best_move
from hangman_printers import print_guess_help
from hangman_leaderboard import get_leaderboard, update_leaderboard

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    clear_screen()
    cprint("\n\n   Welcome to Hangman!\n\n", "yellow", attrs=["bold"])
    get_leaderboard()

# GET word list from provided api
# throw error if requests library returns anything other than a 200 - "OK" - status code
def make_api_request(payload):
    apiEndPoint = "http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words"
    try:
        wordsResponse = requests.get(apiEndPoint, payload)
        if wordsResponse.status_code != 200:
            raise Exception(colored("\nError requesting from server.\n", "red"))
    except Exception as e:
        print(str(e))
        sys.exit()
    return wordsResponse

def handle_flag(guess, gameBoard):
    ret = False
    if guess == "-help":
        print_guess_help()
    elif guess == "-v":
        gameBoard.verbose = not gameBoard.verbose
        if (gameBoard.verbose):
            verbose = "on"
        else:
            verbose = "off"
        print("Verbose mode is now ", verbose)
    else:
        ret = get_best_move(gameBoard)
    return ret

def playAgain(won, gameBoard):
    if won:
        update_leaderboard(gameBoard)
    while True:
        response = input("Play again? [y/n]: ")
        if (response == "y" or response == "n"):
            break
    return True if response == "y" else False
