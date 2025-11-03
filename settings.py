from users import load_users
from blessed import Terminal


term = Terminal()
MENU_WIDTH = 40

def View_History(username):
    users_history = load_users()
    user = users_history[username]
    user_history = user["purchases"]
    print(term.clear)
    top = term.height // 2 - len(user_history) // 2 - 2
    left = (term.width - MENU_WIDTH) // 2

    # Header
    print(term.move_yx(top - 3, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")
    print(term.move_yx(top - 2, left) + "|" + "Purchase History".center(MENU_WIDTH - 2) + "|")
    print(term.move_yx(top - 1, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")

    # If no purchases
    if not user_history:
        print(term.move_yx(top, left) + "|" + "No purchases yet.".center(MENU_WIDTH - 2) + "|")
        print(term.move_yx(top + 1, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")
    else:

        for i, item in enumerate(user_history):
            line_text = f"{item['name']} - ${item['price']}"
            print(term.move_yx(top + i, left) + "|" + line_text.center(MENU_WIDTH - 2) + "|")
        total = sum(item['price'] for item in user_history)
        print(term.move_yx(top + len(user_history) + 1, left) + "|" + f"Total: ${total}".center(MENU_WIDTH - 2) + "|")

        print(term.move_yx(top + len(user_history), left) + "+" + "-" * (MENU_WIDTH - 2) + "+")

    # Footer
    print(
        term.move_yx(top + len(user_history) + 1, left) + "|" + "Press any key to return".center(MENU_WIDTH - 2) + "|")
    print(term.move_yx(top + len(user_history) + 2, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")

    with term.cbreak():
        term.inkey()
