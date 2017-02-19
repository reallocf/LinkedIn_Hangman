LinkedIn_Hangman

A simple command line hangman game


Build instructions:

    If you do not have python 3, follow the guide here:

    https://wiki.python.org/moin/BeginnersGuide/Download

    If you do not have pip3, follow the first stackoverflow response here:

    http://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3

    Now that that's taken care of, all you have to do is run the following command from the command line while in the directory of this codebase:

        pip3 install -r requirements.txt

    And voila! You should be able to run this code.


Run instructions:

    All it takes is one line on the command line while in the codebase's root directory:

        python3 project/main.py


Play instructions:

    Hopefully the game is relatively self-explanatory due to a help feature ('-help') that details what a user can do at any point in the game.

    Going into further detail, when a user first enters the game they're asked for a difficulty level.

    After that, they are prompted to make a guess (either single characters or full-word guesses).

    Should they be correct or incorrect, the game board will update as expected and the user will be prompted again.

    This continues until either a win or a loss occurs. At that point, the user is asked if they would like to play again.

    If they would, the program repeats. If not, the program exits.

    The one more complicating factor is the '-best' feature, which is explained in depth below.


Extensions:

    I implemented a number of extensions in order to more fully flesh out the game.

    These include:

        Adding support for guessing full words

        Adding an actual hangman diagram that is filled in when the user guesses incorrectly

        Adding a user-selected difficulty level that adjusts the api request to make the puzzle easier or harder

        Adding coloring and improving layout within the command line interface

        Adding a leaderboard that connects to a postgresql database on a digital ocean droplet, allowing players to have a record of their number of wins

        Implementing the '-best' feature and it's '-v' verbose mode


    It is this last feature that I spent the most time on and what I found most compelling about the project.

    Putting it simply, '-best' may be input instead of a normal guess to have the computer figure out which letter is best for the current board and then select it.

    It figures out which letter/word is best to guess via a 2 step process.


    STEP ONE, -best goes through all of the words in the dictionary of the correct size (found by another api request without knowledge of the difficulty level) and tries to figure out which words it can eliminate.

    It can eliminate a given word for one of two reasons:

        1. A letter in the given word that should be filled in, but is not

            Example, board:             _ _ _

                     incorrect guesses: ['c']

                     given word:        cat

            Would remove cat because there isn't a 'c' on the board in the first spot

        2. A letter on the board is not in the corresponding spot of the given word

            Example, board:             b _ _

                     incorrect guesses: []

                     given word:        cat

            Would remove cat because there's a 'b' in the first spot on the board and cat's first letter isn't 'b'

    This process ultimately removes a ton of words after a few guesses, greatly minimizing the potential words to select from.

    Of course, if this process leaves only 1 word remaining, -best will guess it and succeed in finishing the problem. But what if there are still a large number of words?


    STEP TWO, -best now loops through every word and removes the letter that occurs in the most words. This does one of two things:

        If the letter it selects is a correct guess, that's great! You're now one letter closer to solving the problem.

        If -best guesses an incorrect letter, that's often even better! Now you've removed the maximum amount of remaining words, so -best will have an even easier time if called again.

    And it does all of this incredibly quickly due to it being only O(n) time relative to the number of charaters in the remaining words and through the power of list comprehensions.


    Ultimately, -best is designed to be a game playing agent that can help you solve your hangman challenges even when they're really difficult.

    It's also fun to play with only -best selecting moves for you. If you're playing with -best from the beginning, it is very unlikely that you will lose.


    In order to better visualize -best, I also implemented '-v', or verbose mode.

    This can be toggled at any guess by inputting '-v' or can be initially set to on by providing a flag at the initial execution:

        python3 project/main.py -v

    -v is used to better visualize what -best is doing at every step. When on, -v displays details about each of the two steps. Namely:

        1. A list of all the words considered after step one filters through them

        2. A tally of the counts for each letter considered, with the selected letter highlighted in green as generated by step two

    I believe that these two pieces of information provide valuable insight to how the algorithm is working and why it works as well as it does.

    It also gives interesting information into why it fails when it does.

    For example, the algorithm does not work well with very short words - when at 3 or 4 letters there are just too many similar options to allow for the problem to be properly constrained.

    Then again, a human would have similar difficulty at this point, and would likely attempt solving the problem in a very similar fashion.



    In terms of extending -best, I'd be interested in learning more about how prefix trees (tries) work to see if those would be useful. I know they're used for autocompletion and problems like that, so maybe there is an interesting overlap.

    I've also conceptualized a way to split the problem into multiple threads, further speeding up the runtime, but I don't know enough about threading to do so at this time - but I hope to learn!

    Finally, it would be really interesting to see how this challenge would be tackled with an even larger dictionary. I figure that, at scale (hundreds of millions of words), this algorithm won't work because it will take too long, so maybe approaching it from another perspective (is this where prefix trees come in?) will be more effective at the cost of accuracy.


What I learned:

     I learned a ton while working on this project.

     I've been coding in C for the past 6 months, so switching gears to python took a few days. I also am not at all experienced in python, and I learned a ton about list comprehensions, dictionaries, and general python best practices over the last week.

     I also had never set up a postgres database from scratch and I was really pleased that it took only an hour or two of tinkering before I got it working.

     In terms of logic, at the very end of the project I did a complete overhaul where I used a rather abstract function (input_looper) and based all of the elements that required user input - so much of the game - around it. I think that this ultimately lead to much more readable, logical code where handling user input was always taken care of via this function instead of on the fly.

What I now know I need to learn:

     I will definitely be seeking to understand Python commenting, file structure, and directory structure best practices.

     I also need to practice writing code more python-like (pythonically?) in general, especially in terms of leaning on existing standard Python functions.

     I'd love to learn more about how to optimize runtime in Python. At first I wrote '-best' without leveraging list comprehensions and it was orders of magnitude slower than when I refactored it into what it is now. I'll definitely be looking into why list comprehensions are so much faster.

     I'm also really interested in better ways of visualizing how '-best' works. I just started an Udacity Nanodegree in Artifical Intelligence on Friday (Feb 17th) and the program appears to be going over some agent visualization techniques (as well as general data visualization techniques) so hopefully that will be applicable!


Anyways, thank you for the problem and I hope you have as much fun playing with my implementation as I did building it.

I look forward to talking to you about this solution during my interview!
