from blessed import Terminal
from users import load_users, update_user

term = Terminal()
PRODUCTS = [
    {"name": "Big vacuum", "price": 120},
    {"name": "Monitor 4k", "price": 350},
    {"name": "Silent Keyboard", "price": 50},
    {"name": "Wireless mouse", "price": 30},
    {"name": "DDR 5 Ram 8 GB", "price": 80},
]
MENU_WIDTH = 40

def shop_page(username):
    users = load_users()
    user = users[username]
    selected = 0

    def build_bordered_line(text, is_selected=False):
        left_border = "|"
        right_border = "|"
        content_width = MENU_WIDTH - 2
        if is_selected:
            highlighted = term.reverse + term.bold_yellow + text.center(content_width) + term.normal
        else:
            highlighted = term.white + text.center(content_width) + term.normal
        return left_border + highlighted + right_border

    def draw_shop():
        print(term.clear)
        top = term.height // 2 - len(PRODUCTS) // 2 - 2
        left = (term.width - MENU_WIDTH) // 2

        # Top border
        print(term.move_yx(top - 3, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
        print(term.move_yx(top - 2, left) + "|" + "Shop".center(MENU_WIDTH-2) + "|")
        print(term.move_yx(top - 1, left) + "+" + "-"*(MENU_WIDTH-2) + "+")


        for i, product in enumerate(PRODUCTS):
            line_text = f"{product['name']} - ${product['price']}"
            print(term.move_yx(top + i, left) + build_bordered_line(line_text, selected == i))


        print(term.move_yx(top + len(PRODUCTS), left) + "+" + "-"*(MENU_WIDTH-2) + "+")
        print(term.move_yx(top + len(PRODUCTS)+1, left) + "|" + "Press Enter to buy, q to exit".center(MENU_WIDTH-2) + "|")
        print(term.move_yx(top + len(PRODUCTS)+2, left) + "+" + "-"*(MENU_WIDTH-2) + "+")

    with term.cbreak(), term.hidden_cursor():
        while True:
            draw_shop()
            key = term.inkey()
            if not key:
                continue
            if key.name == "KEY_DOWN":
                selected = (selected + 1) % len(PRODUCTS)
            elif key.name == "KEY_UP":
                selected = (selected - 1) % len(PRODUCTS)
            elif key.name == "KEY_ENTER":
                item = PRODUCTS[selected]
                user["purchases"].append(item)
                update_user(username, user)
                print(term.clear)
                print(term.move_yx(term.height // 2, 0) + f"✅ You bought {item}! Press any key to continue...")
                term.inkey()
            elif key.lower() == "q":
                return
