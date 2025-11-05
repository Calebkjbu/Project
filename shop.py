from blessed import Terminal
from users import load_users, update_user

term = Terminal()
PRODUCTS = [
    {"name": "Big vacuum", "price": 120},
    {"name": "Monitor 4K", "price": 350},
    {"name": "Silent Keyboard", "price": 50},
    {"name": "Wireless Mouse", "price": 30},
    {"name": "DDR5 RAM 8GB", "price": 80},
]
MENU_WIDTH = 40

def shop_page(username):
    users = load_users()
    user = users[username]
    user["balance"] = user.get("balance", 200.0)
    update_user(username, user)
    selected = 0

    while True:
        print(term.clear)
        top = term.height // 2 - len(PRODUCTS) // 2 - 2
        left = (term.width - MENU_WIDTH) // 2
        print(term.move_yx(top - 3, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
        print(term.move_yx(top - 2, left) + "|" + f"Shop - Balance: ${user['balance']:.2f}".center(MENU_WIDTH-2) + "|")
        print(term.move_yx(top - 1, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
        for i, item in enumerate(PRODUCTS):
            line = f"{item['name']} - ${item['price']:.2f}"
            if i == selected:
                line = term.reverse + term.bold_yellow + line.center(MENU_WIDTH-2) + term.normal
            else:
                line = line.center(MENU_WIDTH-2)
            print(term.move_yx(top + i, left) + "|" + line + "|")
        print(term.move_yx(top + len(PRODUCTS), left) + "+" + "-"*(MENU_WIDTH-2) + "+")
        print(term.move_yx(top + len(PRODUCTS)+1, left) + "|" + "Enter=Buy, Q=Quit".center(MENU_WIDTH-2) + "|")
        print(term.move_yx(top + len(PRODUCTS)+2, left) + "+" + "-"*(MENU_WIDTH-2) + "+")

        key = term.inkey()
        if not key:
            continue
        if key.name == "KEY_DOWN":
            selected = (selected + 1) % len(PRODUCTS)
        elif key.name == "KEY_UP":
            selected = (selected - 1) % len(PRODUCTS)
        elif key.name == "KEY_ENTER":
            product = PRODUCTS[selected]
            if user["balance"] >= product["price"]:
                user["balance"] -= product["price"]
                user["purchases"].append(product)
                update_user(username, user)
                print(term.clear + f"✅ Bought {product['name']} for ${product['price']:.2f}. Remaining: ${user['balance']:.2f}")
            else:
                print(term.clear + f"❌ Not enough money! Balance: ${user['balance']:.2f}")
            term.inkey()
        elif key.lower() == "q":
            break
