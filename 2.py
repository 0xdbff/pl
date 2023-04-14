import re
import json
from typing import Dict
import ply.lex as plex
import atexit


class VendingMachine:
    """A simple vending machine class."""

    products: Dict[str, Dict[str, float]] = {}
    coins: Dict[str, int] = {}

    states = (
        ("inserting", "exclusive"),
        ("sell", "exclusive"),
        ("refill", "exclusive"),
    )

    tokens = (
        "QUANTIA",
        "CANCELAR",
        "PRODUTO",
        "ITEM",
        "COIN",
        "OTHER",
        "RESET",
    )

    @plex.TOKEN(r"QUANTIA")
    def t_QUANTIA(self, t):
        """ """

        t.lexer.begin("inserting")

    @plex.TOKEN(r"PRODUTO")
    def t_PRODUTO(self, t):
        """ """

        t.lexer.begin("sell")

    @plex.TOKEN(r"REFILL")
    def t_REFILL(self, t):
        """ """

        t.lexer.begin("refill")

    @plex.TOKEN(r"[ce][0-9]+")
    def t_inserting_COIN(self, t):
        """ """

        if t.value[0:] not in self.coins:
            print("Coin not accepted by te vending machine!")
            return

        multiplier = 1
        self.coins[t.value] += 1

        if t.value[0] == "e":
            multiplier = 100

        value = int(t.value[1:]) * multiplier * 0.01
        self.client_balance += value
        print(f"valor inserido: €{value:.2f} (saldo: €{self.client_balance:.2f})")

    @plex.TOKEN(r"=\w+")
    def t_sell_ITEM(self, t):
        """ """

        t.value = t.value[1:].rstrip(".")

        product = t.value[0:]
        if product not in self.products:
            print("Invalid product item!")
            return

        self.sell_product(product)
        t.lexer.begin("INITIAL")

    @plex.TOKEN(r"=(\w+) (\d+)")
    def t_refill_ITEM(self, t):
        """
        Extract product name and quantity from the given token value using a regex pattern.

        Args:
            t: The token object with a value containing a product name and quantity.
        """

        print("hi")
        pattern = re.compile(r"=(\w+) (\d+)")
        match = pattern.match(t.value)

        if match:
            product_name = match.group(1)
            quantity = int(match.group(2))

            self.refill_product(product_name, quantity)

    @plex.TOKEN(r"CANCELAR")
    def t_ANY_CANCELAR(self, t):
        """ """

        print(f"valor devolvido: €{self.client_balance:.2f}")

        change = self.calculate_change(self.client_balance)
        self.update_coins(change)
        self.client_balance = 0

        t.lexer.begin("INITIAL")

    @plex.TOKEN(r"\.")
    def t_ANY_RESET(self, t):
        """ """

        t.lexer.begin("INITIAL")

    @staticmethod
    @plex.TOKEN(r"\n+")
    def t_ANY_newline(t):
        """ """

        t.lexer.lineno += len(t.value)

    @staticmethod
    @plex.TOKEN(r".")
    def t_ANY_OTHER(t):
        """ """

        t.value = None

    def t_ANY_error(self, t):
        """ """

        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        """Initialize the vending machine."""

        self.lexer = plex.lex(module=self, **kwargs)
        self.client_balance = 0

        with open("products.json", "r") as file:
            self.products = json.load(file)

        with open("coins.json", "r") as file:
            self.coins = json.load(file)

        atexit.register(self._save_state)

    def _save_state(self):
        """ """

        with open("products.json", "w") as file:
            json.dump(self.products, file, indent=4)

        with open("coins.json", "w") as file:
            json.dump(self.coins, file, indent=4)

    def reset_coins(self):
        for coin in self.coins:
            self.coins[coin] = 20

    def sell_product(self, product):
        """
        Attempt to sell a product if the balance is sufficient.

        Args:
            product (str): The name of the product to sell.
        """

        price = self.products[product]["price"]
        if not price or price <= 0:
            print(f"Invalid product, aborting item purchase! ({product})")
            return

        stock = self.products[product]["stock"]
        if not stock or stock <= 0:
            print(f"There are no products to sell, aborting! ({product})")
            return

        if self.client_balance >= price:
            change_needed = self.client_balance - price
            change = self.calculate_change(change_needed)

            if change is not None:
                print(
                    f"Purchased: '{product}', €{price:.2f} "
                    f"(change = {self.client_balance - price})"
                )
                self.client_balance = 0
                self.update_coins(change)
                self.products[product]["stock"] -= 1
            else:
                print(
                    "Cannot provide change for the purchase "
                    "(Aborting the item purchase!)"
                )
        else:
            print(
                f"Price: €{price:.2f} (insufficient funds) "
                f"(client balance: €{self.client_balance:.2f})"
            )

    def calculate_change(self, change_needed):
        """
        Calculate the change to be given using the available coins.

        Args:
            change_needed (float): The amount of change needed.

        Returns:
            Optional[List[str]]: A list of coin names representing the change,
            or None if exact change cannot be given.
        """

        coin_values = {
            "c5": 0.05,
            "c10": 0.10,
            "c20": 0.20,
            "c50": 0.50,
            "e1": 1.00,
            "e2": 2.00,
        }
        coins_copy = self.coins.copy()
        change = []

        for coin_name, coin_value in sorted(
            coin_values.items(), key=lambda x: x[1], reverse=True
        ):
            while coins_copy[coin_name] > 0 and change_needed >= coin_value:
                change_needed -= coin_value
                change_needed = round(change_needed, 2)
                change.append(coin_name)
                coins_copy[coin_name] -= 1

        if change_needed > 0:
            return None
        else:
            return change

    def update_coins(self, change):
        """
        Update the available coins based on the given change.

        Args:
            change (List[str]): A list of coin names representing the change.
        """

        for coin in change:
            print(coin)
            self.coins[coin] -= 1

    def refill_product(self, product_name, quantity):
        """
        Update the stock of a product in the products dictionary by adding the specified quantity.

        Args:
            product_name (str): The name of the product to be updated.
            quantity (int): The quantity to be added to the stock.
        """

        if product_name in self.products:
            self.products[product_name]["stock"] += quantity
            print(
                f"Refilled {product_name} with {quantity} units. New stock: {self.products[product_name]['stock']}"
            )
        else:
            print(f"Product not found: {product_name}")

    def process(self, data):
        """
        Process the input data to simulate the vending machine.

        Args:
            data (str): The input data containing commands for the vending
            machine.
        """

        if self.lexer is None:
            return

        self.lexer.input(data)

        for f in self.lexer:
            print(f)
            print("hi")
            # continue

        print("hi")


def main():
    data = """
    QUANTIA c10, e1, c50, c50.
    PRODUTO=Cola.
    QUANTIA c20, c70.
    PRODUTO=Cola.
    QUANTIA c20, c10, c5, c50, c10, c5.
    CANCELAR.
    REFILL Cola 2.
    """

    vending_machine = VendingMachine()
    vending_machine.process(data)


if __name__ == "__main__":
    main()
