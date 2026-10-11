from colorama import Fore
import random
import sys

def main():
    choices = ["rock", "paper", "scissors"]

    while True:
        player_choice = get_choice(choices)
        computer_choice = generate_choice(choices)
        winner = None

        if player_choice == computer_choice:
            winner = "draw"

            another_round()

        else:
            if player_choice == "rock":
                if computer_choice == "scissors":
                    winner = "player"
                else:
                    winner = "computer"

            elif player_choice == "paper":
                if computer_choice == "rock":
                    winner = "player"
                else:
                    winner = "computer"

            else:
                if computer_choice == "paper":
                    winner = "player"
                else:
                    winner = "computer"

            show_result(winner, computer_choice, player_choice)
            another_round()


def get_choice(choices):
    while True:
        print()
        print(Fore.CYAN + "-------------- Choices -------------" + Fore.RESET)
        print(Fore.BLUE + "    1- Rock")
        print("    2- Paper")
        print("    3- Scissors" + Fore.RESET)
        print()
        choice = input(Fore.MAGENTA + "What's your choice? " + Fore.RESET).strip().lower()

        validation_result, formatted_choice = choice_validator(choice, choices)

        if validation_result:
            return formatted_choice
        else:
            print(Fore.BLACK + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>" + Fore.RESET)
            print(Fore.RED + "Please enter a valid choice (Number or Name)" + Fore.RESET)
            print(Fore.BLACK + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>" + Fore.RESET)

def choice_validator(choice, choices):
    formatted_choice = choice.strip().lower()

    try: 
        formatted_choice = int(formatted_choice)

    except ValueError:
        pass

    else:
        if 1 <= formatted_choice <= 3:
            formatted_choice = choices[formatted_choice - 1]

    finally:
        return formatted_choice in choices, formatted_choice

def print_rules():
    print("Welcome to Rock-Paper-Scissors!\n")
    print("Winning Rules:")
    print("Rock vs Paper -> Paper wins")
    print("Rock vs Scissors -> Rock wins")
    print("Paper vs Scissors -> Scissors wins\n")

def generate_choice(choices):
    return random.choice(choices)

def another_round():
    while True:
        answer = input(Fore.CYAN + "Do you want to player another round? (yes/no or y/n): " + Fore.RESET).lower().strip()

        match answer:
            case "yes" | "y":
                return True

            case "no" | "n":
                sys.exit()

            case _:
                print(Fore.RED + "Please enter a valid answer" + Fore.RESET)

def show_result(winner, computer_c, player_c):  
    print()

    if winner == "player":
        print(Fore.GREEN + "===== You Win! =====" + Fore.RESET)
    elif winner == "computer":
        print(Fore.RED + "===== Computer Wins! =====" + Fore.RESET)
    elif winner == "draw":
        print(Fore.YELLOW + "===== Draw! =====" + Fore.RESET)
    else: 
        print(Fore.RED + "INVALID WINNER" + Fore.RESET)

    print()
    print(Fore.MAGENTA + "Computer: " + Fore.RED + computer_c.capitalize() + Fore.RESET)
    print(Fore.MAGENTA + "You: " + Fore.GREEN + player_c.capitalize() + Fore.RESET)
    print()

if __name__ == "__main__":
    main()
