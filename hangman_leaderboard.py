import os
import psycopg2
from termcolor import cprint
from hangman_printers import print_game_area, print_leaderboard, print_leaderboard_help

# connect to database on Digital Ocean droplet. If it cannot, print error and return False.
def connect_to_db():
    try:
        conn = psycopg2.connect("dbname='hangman' user='postgres' host='138.197.204.184' password='hhhhijdkfl12d3a'")
        return conn
    except Exception as e:
        cprint("Error connecting to leaderboard database", "red")
        cprint("Error message: " + str(e), "red")
    return False

def get_leaderboard():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM leaderboard ORDER BY win_count DESC LIMIT 10")
        print_leaderboard(cur)
        cur.close()
        conn.close()

def get_leaderboard_name(gameBoard):
    name = input("Input your 3 character name for the leaderboard (input '-help' for assistance): ")
    while True:
        if name == "-help":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_game_area(gameBoard)
            print_leaderboard_help()
        elif len(name) == 3 and name != '"""': # guard against pesky sql injection by disallowing three double quotes
            return name
        elif name == "":
            return False
        name = input("Please input a 3 character name for the leaderboard (input '-help' for assistance): ")

def update_leaderboard(gameBoard):
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        name = get_leaderboard_name(gameBoard)
        if name:
            cur.execute("""SELECT * FROM leaderboard WHERE name='{}'""".format(name))
            row = cur.fetchall()
            if len(row) == 1:
                new_win_count = row[0][1] + 1
                cur.execute("""UPDATE leaderboard SET win_count={} WHERE name='{}'""".format(new_win_count, name))
            else:
                cur.execute("""INSERT INTO leaderboard (name, win_count) VALUES ('{}', 1)""".format(name))
            conn.commit()
        cur.close()
        conn.close()
