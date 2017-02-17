from termcolor import colored, cprint

def print_game_area(gameBoard):
    print_guesses_remaining(gameBoard)
    print_hangman(gameBoard)
    print_current_board(gameBoard)

def print_guesses_remaining(gameBoard):
    print("\nNumber of incorrect guesses remaining: " + str(6 - gameBoard.incorrectCount))

def print_hangman(gameBoard):
    leftLeg = " " if gameBoard.incorrectCount < 1 else colored("/", "blue", attrs=["bold"])
    rightLeg = " " if gameBoard.incorrectCount < 2 else colored("\\", "blue", attrs=["bold"])
    body = " " if gameBoard.incorrectCount < 3 else colored("|", "red", attrs=["bold"])
    leftArm = " " if gameBoard.incorrectCount < 4 else colored("-", "red", attrs=["bold"])
    rightArm = " " if gameBoard.incorrectCount < 5 else colored("-", "red", attrs=["bold"])
    head = " " if gameBoard.incorrectCount < 6 else colored("O", "cyan", attrs=["bold"])
    incorrectGuesses = [word for word in gameBoard.guessedChars if word not in gameBoard.currentBoard and word != gameBoard.secretKeeper.word]
    pole = colored('|', "magenta", attrs=["bold"])
    cprint("     ___", "magenta")
    cprint("    /   |", "magenta")
    print("    {}   {}    Incorrect guesses:".format(head, pole))
    print("   {}{}{}  {}    {}".format(leftArm, body, rightArm, pole, incorrectGuesses))
    print("   {} {}  {}".format(leftLeg, rightLeg, pole))
    cprint("       ___\n", "magenta")

def print_current_board(gameBoard):
    printBoard = [' ', ' ']
    for i in range(len(gameBoard.secretKeeper.word)):
        printBoard.append(gameBoard.currentBoard[i])
        printBoard.append(' ')
    printBoard.append('\n')
    print(''.join(printBoard))

def print_difficulty_help():
    cprint("   Input a number between 1 and 10", "cyan", attrs=["bold"])
    cprint("   The generated word will be more complex if you put in a higher difficulty\n", "cyan", attrs=["bold"])


def print_guess_help():
    cprint("   Select a letter to guess,", "cyan", attrs=["bold"])
    cprint("   try to guess the full word,", "cyan", attrs=["bold"])
    cprint("   or input '-best' to have the computer guess for you", "cyan", attrs=["bold"])

def verbose_print(gameBoard, charPicker):
    print(colored("Words considered:\n", attrs=["bold"]) ,gameBoard.wordsList, "\n")
    cprint("Characters considered:", attrs=["bold"])
    for key in charPicker.charMap.keys():
        if key == charPicker.pickedChar:
            cprint(key + " :  " + str(charPicker.charMap[key]), "green", attrs=["bold"])
        else:
            print(key, ": ", charPicker.charMap[key])
    print()
