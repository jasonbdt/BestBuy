"""Console interface for a simple store demo.

Provides menu display, input validation, product listing, order placement,
and application startup utilities. Depends on the ``products`` and
``store`` modules for domain logic.
"""
from typing import Any, Optional
import sys

from products import Product, ProductNotActiveError, ProductQuantityError
from store import Store


NumRange = tuple[int, int]

def display_menu() -> None:
    """Print the numbered command menu to stdout."""
    print("\n   Store Menu")
    print("   ----------")
    for idx, command in enumerate(COMMANDS, start=1):
        print(f"{idx}. {command}")


def get_user_choice(prompt: str) -> Optional[tuple[Any, str]]:
    """
    Read a menu selection and return the mapped command.

    Prompts the user for a 1-based menu index and returns the corresponding
    ``(callable, argument-key)`` pair from ``COMMANDS``.

    Args:
        prompt: Prompt shown before reading input.

    Returns:
        The ``(callable, argument-key)`` pair if a valid index was entered;
        otherwise ``None``. Invalid numeric input is reported and the user
        is asked again; an out-of-range index ends the loop and yields
        ``None``.
    """
    while True:
        try:
            num = int(input(f"{prompt} "))
            menu_keys = list(COMMANDS)
            return COMMANDS[menu_keys[num-1]]
        except ValueError:
            print("Error with your choice! Try again!")
        except IndexError:
            break


def get_valid_int(
    prompt: str, num_range: NumRange = (0, 1),
    allow_empty: bool = False
) -> int | None:
    """
    Prompt for an integer within an inclusive range.

    The user is repeatedly prompted until a valid integer within the given
    bounds is entered. If ``allow_empty`` is ``True`` and the user enters
    an empty string, ``None`` is returned.

    Args:
        prompt: Message shown before the numeric range hint.
        num_range: Inclusive ``(min_value, max_value)`` bounds.
        allow_empty: Whether to accept empty input and return ``None``.

    Returns:
        The validated integer, or ``None`` if empty input is allowed and
        provided. Error messages are printed for invalid input.
    """
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
    """
    Print all products with 1-based numbering.

    Args:
        store: Store to read products from.

    Notes:
        Delegates per-item formatting to ``Product.show()``.
    """
    print("------")
    for idx, product in enumerate(store.get_all_products(), start=1):
        print(f"{idx}. ", end="")
        product.show()
    print("------")


def display_total_amount(store: Store) -> None:
    """
    Print the total item count currently in the store.

    Args:
        store: Store whose inventory is summarized.
    """
    print(f"Total of {store.get_total_quantity()} items in store")


def order_items(store: Store) -> None:
    """
    Interactively build a shopping list and place an order.

    Shows all products, lets the user select products and quantities, and
    submits the order to the store.

    Args:
        store: Store handling inventory and ordering.

    Side Effects:
        Prints status messages and the final payment amount.

    Exceptions:
        ProductNotActiveError: Reported and suppressed if a chosen product
            is inactive.
        ProductQuantityError: Reported and suppressed if the requested
            quantity is unavailable.
    """
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
    """Terminate the process with exit code 0."""
    sys.exit(0)


def start(store: Store) -> None:
    """
    Run the interactive CLI loop.

    Displays the menu, reads a command using ``get_user_choice()``, and
    invokes the selected function.

    Args:
        store: Store instance passed to commands that require it.
    """
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
    """
    Entry point for running the CLI demo.

    Initializes a store with sample products and starts the UI.
    """
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
