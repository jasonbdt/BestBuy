from typing import Self

from products import Product

ProductList = list[Product]
ShoppingList = list[tuple[Product, int]]


class Store:
    """
    Represents a store that manages products and customer orders.

    The store maintains a list of available products and provides
    methods to add, remove, and query product information, as well
    as process customer orders.

    Attributes:
        products: A list of Product objects representing the store’s inventory.
    """

    def __init__(self, products: ProductList) -> None:
        """
        Initialize a new Store instance.

        Args:
            products: The initial list of Product objects to include in the store.
        """
        self.products = products


    def add_product(self: Self, product: Product) -> None:
        """
        Add a new product to the store's inventory.

        Args:
            product: The Product instance to add.

        Raises:
            ValueError: If the product already exists in the store inventory.
        """
        if product in self.products:
            raise ValueError("This product is already in store inventory.")

        self.products.append(product)


    def remove_product(self: Self, product: Product) -> None:
        """
        Remove a product from the store’s inventory.

        Args:
            product: The Product instance to remove.

        Raises:
            ValueError: If the product does not exist in the store inventory.
        """
        if product not in self.products:
            raise ValueError("This product does not exist in store inventory.")

        self.products.remove(product)


    def get_total_quantity(self: Self) -> int:
        """
        Return the total quantity of all products in stock.

        Returns:
            The sum of quantities for all products in the store.
        """
        return sum(map(lambda product: product.quantity, self.products))


    def get_all_products(self: Self) -> ProductList:
        """
        Return a list of all active products in the store.

        Returns:
            A list containing only active Product objects.
        """
        return list(filter(lambda product: product.is_active(), self.products))


    def order(self: Self, shopping_list: ShoppingList) -> float:
        """
        Process a customer order and calculate the total purchase cost.

        Args:
            shopping_list: A list of tuples, each containing a Product and the quantity to buy.

        Returns:
            The total price of the order.

        Raises:
            ValueError: If a product in the order has insufficient stock
                or an invalid quantity (handled within Product.buy()).
        """
        total_price = 0
        for product, amount in shopping_list:
            total_price += product.buy(amount)

        return total_price
