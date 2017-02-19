from termcolor import colored, cprint

def print_guesses_remaining(incorrectCount):
    print("\nNumber of incorrect guesses remaining: " + str(6 - incorrectCount))

def print_hangman(currentBoard, incorrectCount, guessedChars):
    hangman = [colored("/", "blue", attrs=["bold"]),
               colored("\\", "blue", attrs=["bold"]),
               colored("|", "red", attrs=["bold"]),
               colored("-", "red", attrs=["bold"]),
               colored("-", "red", attrs=["bold"]),
               colored("O", "cyan", attrs=["bold"])]
    toPrint = [hangman[i] if i < incorrectCount else " " for i in range(len(hangman))]
    incorrectGuesses = [char for char in guessedChars if char not in currentBoard]
    pole = colored('|', "magenta", attrs=["bold"])
    cprint("     ___", "magenta")
    cprint("    /   |", "magenta")
    print("    {0}   {1}    Incorrect guesses:".format(toPrint[5], pole))
    print("   {0}{1}{2}  {3}    {4}".format(toPrint[3], toPrint[2], toPrint[4], pole, incorrectGuesses))
    print("   {0} {1}  {2}".format(toPrint[0], toPrint[1], pole))
    cprint("       ___\n", "magenta")

def print_current_board(currentBoard):
    print("  " + ''.join([char + ' ' for char in currentBoard]) + "\n")

def print_game_area(gameBoard):
    print_guesses_remaining(gameBoard.guesser.incorrectCount)
    print_hangman(gameBoard.currentBoard, gameBoard.guesser.incorrectCount, gameBoard.guesser.guessedChars)
    print_current_board(gameBoard.currentBoard)

def print_difficulty_help(looper):
    cprint("Input a number between 1 and 10", "cyan", attrs=["bold"])
    cprint("The generated word will be more complex if you put in a higher difficulty\n", "cyan", attrs=["bold"])
    return False

def print_guess_help():
    cprint("Select a letter to guess,", "cyan", attrs=["bold"])
    cprint("try to guess the full word,", "cyan", attrs=["bold"])
    cprint("or input '-best' to have the computer guess for you", "cyan", attrs=["bold"])

def print_verbose(wordsList, charPicker):
    cprint("Words considered:", attrs=["bold"])
    print(wordsList, "\n")
    cprint("Characters considered:", attrs=["bold"])
    for key in charPicker.charMap.keys():
        if key == charPicker.pickedChar:
            cprint(key + " :  " + str(charPicker.charMap[key]), "green", attrs=["bold"])
        else:
            print(key, ": ", charPicker.charMap[key])

def print_best(wordsList, verbose, value):
    if len(wordsList) == 1:
        if verbose:
            print(colored("Words considered:\n", attrs=["bold"]), wordsList, "\n")
        return value
    elif verbose:
        print_verbose(wordsList, value)
    print("Best selected:", value.pickedChar + "\n")
    print("Input -v to toggle -best's verbose mode\n")
    return value.pickedChar


def print_leaderboard(cursor):
    cprint("      Leaderboard", "green")
    print("     name  |  wins")
    print("     -------------")
    for row in cursor.fetchall():
        print("    ", row[0], "  |  ", row[1])
    print("\n\n")

def print_leaderboard_help(looper):
    cprint("\nSelect a 3 character ID to add your victory to the leaderboard", "cyan", attrs=["bold"])
    cprint("\nYou can also input nothing to not have your win recorded", "cyan", attrs=["bold"])
    return False
