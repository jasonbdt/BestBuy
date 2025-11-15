from typing import Any, Optional
import sys

from products import Product, ProductNotActiveError, ProductQuantityError
from store import Store


NumRange = tuple[int, int]

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


def get_valid_int(prompt: str, num_range: NumRange = (0, 1), allow_empty: bool = False) -> int | None:
    while True:
        min_value, max_value = num_range

        try:
            user_num = input(f"{prompt} ({min_value}-{max_value}): ")

            if allow_empty and user_num == "":
                return None

            user_num = int(user_num)
            if min_value > user_num or user_num > max_value:
                print("Error: You entered an invalid number. Please only use "
                      f"numbers between {min_value} and {max_value}.\n")
                continue

            return user_num
        except ValueError:
            print("ValueError")
            print("Error: You entered an invalid number. Please only use "
                  f"numbers between {min_value} and {max_value}.\n")


def display_all_products(store: Store) -> None:
    print("------")
    for idx, product in enumerate(store.get_all_products(), start=1):
        print(f"{idx}. ", end="")
        product.show()
    print("------")


def display_total_amount(store: Store) -> None:
    print(f"Total of {store.get_total_quantity()} items in store")


def order_items(store: Store) -> None:
    shopping_list = []
    display_all_products(store)
    print("When you want to finish order, enter empty text.")

    while True:
        products = store.get_all_products()
        user_order = get_valid_int("Which product # do you want", (1, len(products)), True)

        if user_order:
            product = products[user_order-1]
            user_amount = get_valid_int("What amount do you want", (1, product.quantity))
            shopping_list.append((products[int(user_order)-1], user_amount))
            print("Product added to list!\n")
        else:
            break

    if shopping_list:
        try:
            total_price = store.order(shopping_list)
        except (ProductNotActiveError, ProductQuantityError) as err:
            print(f"Error while making order:\n{err}\n")
        else:
            print("********")
            print(f"Order made! Total payment: ${total_price}")
    else:
        print("Your shopping list is empty. Order cancelled!")


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
    "Show total amount in store": (display_total_amount, "store"),
    "Make an order": (order_items, "store"),
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
