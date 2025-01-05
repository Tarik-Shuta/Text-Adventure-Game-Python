import json
import random
import sys

# Global variables to track game state
has_weapon = False
has_sword = False
gave_beggar_money = False
has_ahmed = False
has_key = False

# Dictionary to hold game text loaded from JSON
game_text = {}

def main():
    load_game_data()

    print(game_text["welcome"])
    player_name = input("Enter your name: ")

    print(game_text["mission"].replace("{playerName}", player_name))
    market_square()

def load_game_data():
    try:
        with open('GameData.json', 'r') as file:
            global game_text
            game_text = json.load(file)
    except Exception as ex:
        print(f"Error loading game data: {ex}")
        sys.exit(1)

def market_square():
    global has_weapon, has_key
    print(game_text["marketSquare_intro"])
    print(game_text["marketSquare_choices"])
    choice = get_choice(2)

    if choice == 1:
        print(game_text["marketSquare_help"])
        if random.randint(1, 101) <= 50:
            print(game_text["marketSquare_key"])
            has_key = True
    elif choice == 2:
        print(game_text["marketSquare_weapon"])
        has_weapon = True

    print(game_text["marketSquare_next"])
    choice = get_choice(2)

    if choice == 1:
        latin_bridge()
    elif choice == 2:
        sebilj()

def latin_bridge():
    print(game_text["latinBridge_intro"])
    if has_weapon:
        print(game_text["latinBridge_fight"])
        end_game(False)
    else:
        print(game_text["latinBridge_defeat"])
        end_game(False)

def sebilj():
    global gave_beggar_money, has_key, has_sword, has_ahmed

    print(game_text["sebilj_intro"])
    print("1. Give him 1 mark.\n2. Ignore him.")
    if has_key:
        print("3. Offer the mysterious key.")
    choice = get_choice(3 if has_key else 2)

    if choice == 1:
        print(game_text["sebilj_beggar_yes"])
        gave_beggar_money = True
    elif choice == 2:
        print(game_text["sebilj_beggar_no"])
    elif choice == 3 and has_key:
        print(game_text["sebilj_beggar_key"])

    print(game_text["sebilj_food"])
    choice = get_choice(2)

    if choice == 1:
        print(game_text["sebilj_cevapi"])
        end_game(False)
    elif choice == 2:
        print(game_text["sebilj_burek"])
        print(game_text["sebilj_ahmed"])
        if has_key:
            print(game_text["sebilj_key"])
        choice = get_choice(3 if has_key else 2)
        if choice == 1:
            print(game_text["sebilj_ahmed_yes"])
            has_ahmed = True
        elif choice == 2:
            print(game_text["sebilj_ahmed_no"])
        elif choice == 3 and has_key:
            print(game_text["sebilj_sword"])
            has_key = False
            has_sword = True

        city_hall()

def city_hall():
    print(game_text["cityHall_intro"])

    if has_sword:
        print(game_text["cityHall_sword"])
        end_game(True)
        return
    if not has_ahmed:
        print(game_text["cityHall_noAhmed"])
        end_game(False)
        return

    print(game_text["cityHall_attack"])
    choice = get_choice(2)

    if choice == 1:
        print(game_text["cityHall_ahmed"])
        if gave_beggar_money:
            print(game_text["cityHall_beggar"])
            end_game(True)
        else:
            print(game_text["cityHall_defeat"])
            end_game(False)
    else:
        print(game_text["cityHall_ambush"])
        end_game(False)

def end_game(victory):
    print(game_text["end_victory"] if victory else game_text["end_defeat"])
    print(game_text["end_replay"])
    choice = get_choice(2)
    if choice == 1:
        reset_game_state()
        market_square()
    else:
        print(game_text["end_exit"])
        sys.exit(0)

def reset_game_state():
    global has_weapon, has_sword, gave_beggar_money, has_ahmed, has_key
    has_weapon = False
    has_sword = False
    gave_beggar_money = False
    has_ahmed = False
    has_key = False

def get_choice(max_option):
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= max_option:
                return choice
        except ValueError:
            pass
        print(f"Invalid input. Please enter a number between 1 and {max_option}.")

if __name__ == "__main__":
    main()
