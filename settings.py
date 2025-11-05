from users import load_users
from blessed import Terminal

term = Terminal()
MENU_WIDTH = 40

def View_History(username):
    users = load_users()
    user = users[username]
    history = user.get("purchases", [])

    print(term.clear)
    top = term.height // 2 - len(history) // 2 - 2
    left = (term.width - MENU_WIDTH) // 2

    print(term.move_yx(top - 3, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")
    print(term.move_yx(top - 2, left) + "|" + "Purchase History".center(MENU_WIDTH - 2) + "|")
    print(term.move_yx(top - 1, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")

    if not history:
        print(term.move_yx(top, left) + "|" + "No purchases yet.".center(MENU_WIDTH - 2) + "|")
    else:
        for i, item in enumerate(history):
            line = f"{item['name']} - ${item['price']:.2f}"
            print(term.move_yx(top + i, left) + "|" + line.center(MENU_WIDTH - 2) + "|")
        total = sum(i['price'] for i in history)
        print(term.move_yx(top + len(history) + 1, left) + "|" + f"Total: ${total:.2f}".center(MENU_WIDTH - 2) + "|")

    print(term.move_yx(top + len(history) + 3, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")
    print(term.move_yx(top + len(history) + 4, left) + "|" + "Press any key to return".center(MENU_WIDTH - 2) + "|")
    print(term.move_yx(top + len(history) + 5, left) + "+" + "-" * (MENU_WIDTH - 2) + "+")
    term.inkey()
