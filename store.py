from typing import Self

from products import Product


class Store:

    def __init__(self, products: list[Product]) -> None:
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


    def get_all_products(self: Self) -> list[Product]:
        return list(filter(lambda product: product.is_active(), self.products))


    def order(self: Self, shopping_list: list[tuple[Product, int]]) -> float:
        total_price = 0
        for product, amount in shopping_list:
            total_price += product.buy(amount)

        return total_price
