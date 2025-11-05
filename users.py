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

# --- Input handling (temporarily exits cbreak for safe typing) ---
def get_input(prompt):
    print(term.clear)  # optional: clear for clean input screen
    print(prompt, end="", flush=True)

    # temporarily exit cbreak by closing the current context
    # standard input works normally here
    s = input()

    # flush leftover keys to prevent menu from consuming Enter or arrow keys
    with term.cbreak():
        while term.inkey(timeout=0):
            pass
    return s


# --- Login / Signup ---
def login_signup_menu():
    options = ["Login", "Sign Up", "Exit"]
    selected = 0
    while True:
        choice = None
        with term.cbreak(), term.hidden_cursor():
            print(term.clear)
            top = term.height // 2 - len(options) // 2 - 2
            left = (term.width - MENU_WIDTH) // 2
            print(term.move_yx(top, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
            print(term.move_yx(top+1, left) + "|" + "🔑 Welcome!".center(MENU_WIDTH-2) + "|")
            print(term.move_yx(top+2, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
            for i, option in enumerate(options):
                line = option.center(MENU_WIDTH-2)
                if i == selected:
                    line = term.reverse + term.bold_yellow + line + term.normal
                print(term.move_yx(top+3+i, left) + "|" + line + "|")
            print(term.move_yx(top+3+len(options), left) + "+" + "-"*(MENU_WIDTH-2) + "+")
            key = term.inkey()
            if key.name == "KEY_DOWN":
                selected = (selected + 1) % len(options)
            elif key.name == "KEY_UP":
                selected = (selected - 1) % len(options)
            elif key.name == "KEY_ENTER":
                choice = options[selected]
        if choice == "Login":
            username = login_input()
            if username:
                return username
        elif choice == "Sign Up":
            signup_input()
        elif choice == "Exit":
            return None

def login_input():
    users = load_users()
    print(term.clear)
    username = get_input("Username: ")
    password = get_input("Password: ")
    user = users.get(username)
    if not user:
        print("\n⚠️ Username not found. Press any key to continue...")
        term.inkey()
        return None
    if user["password"] != password:
        print("\n⚠️ Wrong password. Press any key to continue...")
        term.inkey()
        return None
    # Ensure balance exists for old users
    if "balance" not in user:
        user["balance"] = 200.0
        update_user(username, user)
    print(f"\n✅ Welcome back, {username}! Press any key to continue")
    term.inkey()
    return username

def signup_input():
    users = load_users()
    print(term.clear)
    username = get_input("Choose a username: ")
    if username in users:
        print("\n⚠️ Username already exists. Press any key to continue...")
        term.inkey()
        return None
    password = get_input("Choose a password: ")
    users[username] = {"password": password, "cards": [], "purchases": [], "balance": 200.0}
    save_users(users)
    print(f"\n✅ User '{username}' created with $200 starting balance! Press any key to continue...")
    term.inkey()

def add_funds(username):
    from users import load_users, update_user
    users = load_users()
    user = users[username]

    print(term.clear)
    print("💳 Add Funds")

    # temporarily exit cbreak for normal input
def add_funds(username):
    users = load_users()
    user = users[username]

    print(term.clear)
    print("💳 Add Funds")

    card_number = get_input("Enter debit card number: ").strip()
    if card_number == "1234-5678-9876-5432":
        try:
            amount_str = get_input("Enter amount to add: $")
            amount = float(amount_str)
            user["balance"] = user.get("balance", 200.0) + amount
            update_user(username, user)
            print(f"✅ Added ${amount:.2f}. New balance: ${user['balance']:.2f}")
        except ValueError:
            print("❌ Invalid amount.")
    else:
        print("❌ Invalid debit card.")
    get_input("Press Enter to return...")



