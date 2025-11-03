from blessed import Terminal
from users import login_signup_menu
from shop import shop_page
from settings import View_History

term = Terminal()
menu_options = ["Shop", "Cards", "Exit", "View History"]
selected = 0
MENU_WIDTH = 40

def build_bordered_line(text, is_selected=False):
    left_border = "|"
    right_border = "|"
    content_width = MENU_WIDTH - 2
    if is_selected:
        highlighted = term.reverse + term.bold_yellow + text.center(content_width) + term.normal
    else:
        highlighted = term.white + text.center(content_width) + term.normal
    return left_border + highlighted + right_border

def draw_menu():
    print(term.clear)
    top = term.height // 2 - len(menu_options) // 2 - 2
    left = (term.width - MENU_WIDTH) // 2

    # Top border
    print(term.move_yx(top - 3, left) + "+" + "-"*(MENU_WIDTH-2) + "+")
    print(term.move_yx(top - 2, left) + "|" + "🏬 Main Menu".center(MENU_WIDTH-2) + "|")
    print(term.move_yx(top - 1, left) + "+" + "-"*(MENU_WIDTH-2) + "+")

    for i, option in enumerate(menu_options):
        print(term.move_yx(top + i, left) + build_bordered_line(option, selected == i))

    print(term.move_yx(top + len(menu_options), left) + "+" + "-"*(MENU_WIDTH-2) + "+")

def update_highlight(prev, curr):
    top = term.height // 2 - len(menu_options) // 2 - 2
    left = (term.width - MENU_WIDTH) // 2
    print(term.move_yx(top + prev, left) + build_bordered_line(menu_options[prev], False))
    print(term.move_yx(top + curr, left) + build_bordered_line(menu_options[curr], True))

def main_menu(username):
    global selected
    with term.cbreak(), term.hidden_cursor():
        while True:
            draw_menu()
            key = term.inkey()
            if not key:
                continue
            prev = selected
            if key.name == "KEY_DOWN":
                selected = (selected + 1) % len(menu_options)
                update_highlight(prev, selected)
            elif key.name == "KEY_UP":
                selected = (selected - 1) % len(menu_options)
                update_highlight(prev, selected)
            elif key.name == "KEY_ENTER":
                choice = menu_options[selected]
                if choice == "Shop":
                    shop_page(username)
                elif choice == "View History":
                    View_History(username)
                elif choice == "Add Cards":
                    print(term.clear + " Add Cards coming soon! Press any key...")
                    term.inkey()
                elif choice == "Exit":
                    print(term.clear + " See ya Press any key to exit...")
                    term.inkey()
                    return

def start():
    while True:
        username = login_signup_menu()
        if username:
            main_menu(username)
        else:
            print(term.clear + "👋 Goodbye!")
            break

if __name__ == "__main__":
    start()
