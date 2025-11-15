from typing import Any, Optional
import sys

from products import Product
from store import Store


def display_menu() -> None:
    print("\n   Store Menu")
    print("   ----------")
    for idx, command in enumerate(COMMANDS, start=1):
        print(f"{idx}. {command}")


def get_user_choice(prompt: str) -> Optional[tuple[Any, str]]:
    while True:
        try:
            num = int(input(f"{prompt} "))
            menu_keys = [item for item in COMMANDS]
            return COMMANDS[menu_keys[num-1]]
        except ValueError:
            print("Error with your choice! Try again!")
        except IndexError:
            break


def display_all_products(store: Store) -> None:
    print("------")
    for idx, product in enumerate(store.get_all_products(), start=1):
        print(f"{idx}. ", end="")
        product.show()
    print("------")


def exit_app() -> None:
    sys.exit(0)


def start(store: Store) -> None:
    while True:
        display_menu()
        user_cmd, cmd_args = get_user_choice("Please choose a number:")

        if user_cmd is not None:
            if cmd_args is not None:
                user_cmd(store)
            else:
                user_cmd()


COMMANDS = {
    "List all products in store": (display_all_products, "store"),
    "Quit": (exit_app, None)
}


def main() -> None:
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]

    start(Store(product_list))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit_app()
