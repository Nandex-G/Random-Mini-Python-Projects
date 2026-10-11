import random
import time
import sys

class HangMan:
    def __init__(self, list_of_words, attempts):
        word = random.choice(list_of_words).lower()


        self.WORD = list(word)
        self.GUESSED_CHARS = list()

        self.left_attempts = attempts

    def run(self):
        name = input("What's your name? ")
        self.printer(f"Welcome {name} to my word guessing game...")
        time.sleep(1)
        
        while len(self.WORD) > 0:
            print()
            for char in self.GUESSED_CHARS:
                print(char, end=" ")
            print("_ " * len(self.WORD))

            guessed_char = input("What's your guess? ").strip().lower()

            if guessed_char == self.WORD[0]:
                self.WORD.pop(0)
                self.GUESSED_CHARS.append(guessed_char)

            else:
                self.left_attempts -= 1

                if self.left_attempts == 0:
                    self.failed()
                    sys.exit()

                print("WRONG GUESS!")
                time.sleep(1)
                print(f"You have {self.left_attempts} attempt(s) left.") 
                time.sleep(1)
                print("Be careful...")     
                time.sleep(2)      

        self.won()

    def failed(self):   
        print()
        
        time.sleep(2)
        self.printer("It's over...")

        time.sleep(1)
        self.printer("It's so over...", .07)
        
        time.sleep(1.5)
        self.printer("You ran out of guesses.")

        time.sleep(1.5)
        self.printer("YOU LOST.", .2)
        print()

        time.sleep(2)
        self.printer("Execution initializing...", .02)

        time.sleep(1)
        self.printer("Activating electric chair...", .02)
        print()

        time.sleep(3)
        self.printer("Maybe in another life.........", .09)

        time.sleep(4)
        self.printer("zhkzhkzhkzhkzhkzhzhzhkzkhzhzhkzhkzkhzkhzhkzkhkhkh", .02)


    def won(self):
        print()
        self.printer("Ohhhhhh!", .1)
        
        time.sleep(1.5)
        self.printer("Interesting.....", .07)

        time.sleep(2)
        self.printer("Looks like you successfully guessed the word!")

        time.sleep(1.5)
        self.printer("You're the first person to win my game!", .06)

        time.sleep(1)
        self.printer("Good for you.", .08)

        time.sleep(2)
        self.printer("Now...", .13)

        time.sleep(1.5)
        self.printer("You'r free to go", .06)

        time.sleep(2)
        self.printer("BUT", .2)

        time.sleep(1)
        self.printer("Remember", .08)

        time.sleep(1.5)
        self.printer("Enjoy your life as much as you can...")

        time.sleep(1)
        self.printer("Because...", .1)

        time.sleep(1.5)
        self.printer("Next time I get you...", .06)

        time.sleep(1.5)
        self.printer("There'll be no games to play........", .13)

    def printer(self, statement, delay = .05):
        for char in statement:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()


words = [
    "apple", "window", "ocean", "rocket", "forest",
    "pencil", "mirror", "cloud", "dragon", "coffee",
    "planet", "guitar", "bridge", "shadow", "garden",
    "thunder", "river", "castle", "camera", "diamond",
    "keyboard", "mountain", "sunset", "puzzle", "butterfly",
    "island", "robot", "blanket", "volcano", "rainbow",
    "helmet", "desert", "candle", "spaceship", "library",
    "telescope", "bottle", "snowflake", "pyramid", "compass",
    "elephant", "lantern", "village", "whistle", "magnet",
    "calendar", "sandwich", "airport", "jungle", "umbrella",
    "throne", "notebook", "waterfall", "penguin", "submarine",
    "pocket", "train", "adventure", "galaxy", "hammer",
    "window", "island", "feather", "engine", "museum",
    "volcano", "basket", "signal", "planet", "anchor",
    "forest", "ticket", "piano", "mirror", "battery",
    "cactus", "helmet", "camera", "river", "rocket",
    "keyboard", "castle", "diamond", "cloud", "guitar",
    "bridge", "dragon", "coffee", "mountain", "puzzle",
    "butterfly", "robot", "library", "telescope", "rainbow"
]

def main():
    game = HangMan(words, 3)

    game.run()






if __name__ == "__main__":
    main()