import sys
import os
import requests
from termcolor import colored, cprint

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    clear_screen()
    cprint("\n\n   Welcome to Hangman!\n\n", "yellow", attrs=["bold"])

def playAgain():
    while True:
        response = input("Play again? [y/n]: ")
        if (response == "y" or response == "n"):
            break
    return True if response == "y" else False
