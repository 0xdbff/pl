import ply.lex as lex

tokens = (
    "QUANTIA",
    "CANCELAR",
    "PRODUTO",
    "COIN",
)


def t_QUANTIA(t):
    r"QUANTIA"
    return t


def t_CANCELAR(t):
    r"CANCELAR"
    return t


def t_PRODUTO(t):
    r"PRODUTO=\w+\."
    return t


def t_COIN(t):
    r"[ce][0-9]+"
    multiplier = 1
    if t.value[0] == "e":
        multiplier = 100
    t.value = int(t.value[1:]) * multiplier / 100
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_OTHER(t):
    r"[ ,\.]"
    pass


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


class VendingMachine:
    """A simple vending machine class."""

    lexer = lex.lex()

    def __init__(self):
        """Initialize the vending machine."""

        self.products = {
            "twix": 2.30,
        }
        self.coins = []
        self.balance = 0
        self.inserting = False

    def insert_coin(self):
        """Add the coins to the balance and clear the coins list."""

        total = sum(self.coins)
        self.balance += total
        print(f"valor inserido: €{total:.2f} (saldo: €{self.balance:.2f})")
        self.coins = []

    def sell_product(self, product):
        """
        Attempt to sell a product if the balance is sufficient.

        Args:
            product (str): The name of the product to sell.
        """

        price = self.products.get(product)
        if not price:
            print(f"produto não encontrado: {product}")
            return
        if self.balance >= price:
            print(f"compra: '{product}', €{price:.2f} (sem troco)")
            self.balance -= price
        else:
            print(
                f"preço: €{price:.2f} (quantia insuficiente) (saldo: €{self.balance:.2f})"
            )

    def process(self, data):
        """
        Process the input data to simulate the vending machine.

        Args:
            data (str): The input data containing commands for the vending machine.
        """

        self.lexer.input(data)
        product = None

        for token in self.lexer:
            if token.type == "COIN":
                self.coins.append(token.value)

            elif token.type == "QUANTIA":
                if self.inserting:
                    self.insert_coin()
                self.inserting = True

            elif token.type == "PRODUTO":
                if self.inserting:
                    self.insert_coin()
                    self.inserting = False
                product = token.value.split("=")[1].rstrip(".")
                if product is not None:
                    self.sell_product(product)
                product = None

            elif token.type == "CANCELAR":
                if self.coins:
                    self.insert_coin()
                print(f"valor devolvido: €{self.balance:.2f}")
                self.balance = 0

        # if self.inserting and self.coins:
        #     self.insert_coin()


def main():
    data = "QUANTIA c10, e1, c50, c50.\nPRODUTO=twix.\nQUANTIA c20, c70.\nPRODUTO=twix.\nQUANTIA c20, c10, c5, c50, c10, c5.\nCANCELAR"

    vending_machine = VendingMachine()
    vending_machine.process(data)


if __name__ == "__main__":
    main()
