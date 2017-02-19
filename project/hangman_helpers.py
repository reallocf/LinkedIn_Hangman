import sys
import os
import requests
from termcolor import colored, cprint

class Looper:
    def __init__(self, initialStatement, extraData, flagParams):
        self.ret = ""
        self.statement = initialStatement
        self.data = extraData
        self.flagParams = flagParams

# allow for a gracefull program exit with interrupt signal is given or api request fails
def exit_gracefully(signal, frame):
    print("\n")
    sys.exit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_looper(bool_function, initialStatement, extraData={},
                 start_function=False, startParams=False,
                 middle_function=False, middleParams=False,
                 flags=[], flag_function=False, flagParams={}):
    looper = Looper(initialStatement, extraData, flagParams)
    while True:
        if start_function and startParams:
            start_function(startParams) if startParams else start_function()
        looper.ret = input(looper.statement)
        if bool_function(looper):
            return looper.ret
        if middle_function:
            middle_function(middleParams) if middleParams else middle_function()
        if looper.ret in flags:
            if flag_function(looper):
                return looper.ret

# GET word list from provided api
# throw error if requests library returns anything other than a 200 - "OK" - status code
def make_api_request(payload):
    apiEndPoint = "http://linkedin-reach.hagbpyjegb.us-west-2.elasticbeanstalk.com/words"
    try:
        wordsResponse = requests.get(apiEndPoint, payload)
        if wordsResponse.status_code != 200:
            raise Exception(colored("\nError requesting from server - status code 200 not returned\n", "red"))
    except Exception as e:
        cprint("\nError message: " + str(e) + "\n", "red")
        sys.exit()
    return wordsResponse
