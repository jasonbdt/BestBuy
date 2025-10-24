from typing import Self


class ProductNotActiveError(Exception):
    pass


class ProductQuantityError(Exception):
    pass


class Product:
    """
    Represents a purchasable product with price, stock quantity, and active state.

    A product is active by default. Setting its quantity to zero deactivates it.

    Attributes:
        name: Product name (non-empty).
        price: Unit price (must be ≥ 0).
        quantity: Units in stock (must be ≥ 0).
        active: Availability flag; inactive products should not be sold.
    """
    def __init__(self: Self, name: str, price: float, quantity: int) -> None:
        """
        Initialize a new Product.

        Args:
            name: The product name.
            price: The unit price (≥ 0).
            quantity: Initial stock quantity (≥ 0).

        Raises:
            ValueError: If name is empty, price < 0, or quantity < 0.
        """
        if not name:
            raise ValueError("A product's name cannot be empty.")

        if price < 0:
            raise ValueError("A product's price cannot be less than zero.")

        if quantity < 0:
            raise ValueError("A product's quantity cannot be less than zero.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True


    def get_quantity(self: Self) -> int:
        """
        Return the current stock quantity.

        Returns:
            The number of units in stock.
        """
        return self.quantity


    def set_quantity(self: Self, quantity: int) -> None:
        """
        Set the stock quantity; deactivates the product when set to zero.

        Args:
            quantity: The new stock quantity (≥ 0).

        Raises:
            ValueError: If quantity < 0.
        """
        if quantity < 0:
            raise ValueError("A product's quantity cannot be less than zero.")
        elif quantity == 0:
            self.deactivate()

        self.quantity = quantity


    def is_active(self: Self) -> bool:
        """
        Indicate whether the product is active.

        Returns:
            True if the product is active; otherwise False.
        """
        return self.active


    def activate(self: Self) -> None:
        """Mark the product as active."""
        self.active = True


    def deactivate(self: Self) -> None:
        """Mark the product as inactive."""
        self.active = False


    def show(self: Self) -> None:
        """
        Print a one-line summary of the product.

        Side Effects:
            Writes a formatted summary to stdout.
        """
        print(f"{self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}")


    def buy(self: Self, quantity: int) -> float:
        """
        Purchase units and reduce stock accordingly.

        Args:
            quantity: The number of units to buy (must be ≥ 1 and ≤ stock).

        Returns:
            The total price for the purchase (quantity * unit price).

        Raises:
            ValueError: If quantity < 1 or quantity exceeds available stock.
        """
        if not self.active:
            raise ProductNotActiveError("Product Inactive")
        elif quantity > self.quantity:
            raise ProductQuantityError(f"Product only has {self.quantity} in stock")
        elif quantity < 1:
            raise ProductQuantityError("Product Quantity Invalid")

        self.set_quantity(self.quantity - quantity)
        return quantity * self.price
