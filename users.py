import json
import os
from blessed import Terminal

term = Terminal()
USERS_FILE = "users.json"
MENU_WIDTH = 40

# --- User persistence ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def update_user(username, data):
    users = load_users()
    users[username] = data
    save_users(users)

# --- Build highlighted menu line ---
def build_line(text, is_selected=False, width=MENU_WIDTH):
    if is_selected:
        return term.reverse + term.bold_yellow + text.center(width-2) + term.normal
    else:
        return text.center(width-2)

# --- Login / Signup menu ---
def login_signup_menu():
    options = ["Login", "Sign Up", "Exit"]
    selected = 0

    while True:
        choice = None
        # --- Draw menu and handle arrows inside cbreak ---
        with term.cbreak(), term.hidden_cursor():
            print(term.clear)
            top = term.height // 2 - len(options) // 2 - 2
            left = (term.width - MENU_WIDTH) // 2

            # Top border
            print(term.move_yx(top, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
            print(term.move_yx(top+1, left) + "|" + "🔑 Welcome!".center(MENU_WIDTH-2) + "|")
            print(term.move_yx(top+2, left) + "+" + "-"*(MENU_WIDTH-2) + "+")

            # Menu options
            for i, option in enumerate(options):
                line = build_line(option, selected == i)
                print(term.move_yx(top+3+i, left) + "|" + line + "|")

            # Bottom border
            print(term.move_yx(top+3+len(options), left) + "+" + "-"*(MENU_WIDTH-2) + "+")

            # Get key
            key = term.inkey()
            if key.name == "KEY_DOWN":
                selected = (selected + 1) % len(options)
            elif key.name == "KEY_UP":
                selected = (selected - 1) % len(options)
            elif key.name == "KEY_ENTER":
                choice = options[selected]

        # --- Handle choices outside cbreak ---
        if choice == "Login":
            username = login_input()
            if username:
                return username  # Exit menu only after successful login
        elif choice == "Sign Up":
            signup_input()       # Return to menu after signup
        elif choice == "Exit":
            return None

# --- Login input ---
def login_input():
    users = load_users()
    print(term.clear)
    print(term.center("=== Login ==="))
    print(term.center("Type your username and password below\n"))

    username = input("Username: ")
    password = input("Password: ")

    user = users.get(username)
    if not user:
        print("\n⚠️ Username not found. Press Enter to continue...")
        input()
        return None
    if user["password"] != password:
        print("\n⚠️ Wrong password. Press Enter to continue...")
        input()
        return None

    print(f"\n✅ Welcome back, {username}! Press Enter to continue...")
    input()
    return username

# --- Signup input ---
def signup_input():
    users = load_users()
    print(term.clear)
    print(term.center("=== Sign Up ==="))
    print(term.center("Type your username and password below\n"))

    username = input("Username: ")
    if username in users:
        print("\n⚠️ Username already exists. Press Enter to continue...")
        input()
        return None
    password = input("Password: ")

    users[username] = {"password": password, "cards": [], "purchases": []}
    save_users(users)
    print(f"\n✅ User '{username}' created! Press Enter to continue...")
    input()
