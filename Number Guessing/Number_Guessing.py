import time
import random
import sys

def main():
    username = input("Please enter your username: ").strip()


    while True:
        print("Please enter the range of numbers")
        num_range_from = int(input("From: ").strip())
        num_range_to = int(input("To: ").strip())
        stop = False

        if num_range_to - num_range_from < 0:
            printer("Hello?")
            printer("Anyone there?")
            printer("Somebody get this robotic %#$^%$# animal out of here!!")
            printer("Do you even have a brain??")
            printer("I do really wanna know")
            printer("How the hell am I going to choose a number between these two shits?!")
            sys.exit("Go do something else. Computer is not for you buddy...")
        
        elif num_range_to - num_range_from <= 5:
            printer("What the fuck did you think with yourself that you decided these numbers?!")
            printer("The possible numbers are lower than 5.")
            printer("Before you decide to do anything, you'd better think a little longer.")
            printer("Trust me.")
            printer("Go to your room and lock the door...")
            printer("Then, start thinking about your past decisions...")
            printer("There must be one problem that made you this stupid")
            printer("Try better numbers")
            pass
        
        elif num_range_to - num_range_from < 10:
            printer("Broo!")
            printer("What the fuck is this number?!")
            printer("The number of possible numbers between them is lower than 10...")
            printer("Try something better") 
            pass

        else:
            stop = game(username, [num_range_from, num_range_to])

        if stop:
            break            

    print(f"SYL, {username}")

def game(username, num_range):
    tries = 0
    from_n, to_n = num_range

    print()
    printer(f"Welcome, {username}", .1)

    printer(f"In this game, you need to guess a number between {from_n} and {to_n}", .04)

    printer("Soooo, let's start", .09)

    random_number = random.randrange(from_n, to_n)

    while True:
        print()
        guessed_number = int(input("What's your guess? ").strip())

        tries += 1
        if guessed_number == random_number:
            printer("Ohhhhhh", .02, 1)
            printer("Looks like...", .02, .8)
            printer("YOU WON!", .1)
            print()
            printer(f"It took you {tries} to guesses to find the number")
            return should_stop()


        elif guessed_number > random_number:
            printer("Lower, you went too far...", .06, 1)

        elif guessed_number < random_number:
            printer("Higher, don't be shy...", .06, 1)

        if guessed_number > to_n:
            printer("WAIT A SEC!", .07, 2)
            printer("Broooooo!!") 
            printer("Are you a fucking human?!")
            printer("I don't think so...")
            printer(f"The number must be lower than {to_n}.")
            printer("USE YOUR BRAIN")

        elif guessed_number < from_n:
            printer("WAIT WHAT!", .07, 2)
            printer("OMFG!!!")
            printer("Do you even think?!") 
            printer("I mean, do you use than big piece of fat in your skull called brain?!")
            printer(f"Your fucking guess must be higher than {from_n}.")
            printer("USE YOUR BRAIN")
            

def printer(text, interval = .05, wait = 1.5):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(interval)
    print("")
    time.sleep(wait)

def should_stop():
    while True:
        stop = input("Wanna play another round? (Y/N or Yes/No): ").strip().lower()

        if stop == "y" or stop == "yes":
            return False
        elif stop == "n" or stop == "no":
            return True
        else: 
            print("Please enter a valid answer (Y/N or Yes/No)")


if __name__ == "__main__":
    main()