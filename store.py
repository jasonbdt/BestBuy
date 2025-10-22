from typing import Self

from products import Product

ProductList = list[Product]
ShoppingList = list[tuple[Product, int]]


class Store:

    def __init__(self, products: ProductList) -> None:
        self.products = products


    def add_product(self: Self, product: Product) -> None:
        if product in self.products:
            raise ValueError("This product is already in store inventory.")

        self.products.append(product)


    def remove_product(self: Self, product: Product) -> None:
        if product not in self.products:
            raise ValueError("This product does not exist in store inventory.")

        self.products.remove(product)


    def get_total_quantity(self: Self) -> int:
        return sum(map(lambda product: product.quantity, self.products))


    def get_all_products(self: Self) -> ProductList:
        return list(filter(lambda product: product.is_active(), self.products))


    def order(self: Self, shopping_list: ShoppingList) -> float:
        total_price = 0
        for product, amount in shopping_list:
            total_price += product.buy(amount)

        return total_price
