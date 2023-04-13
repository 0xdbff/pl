import re
import sys
from ply.lex import lex

tokens = (
    "QUANTIA",
    "PRODUTO",
    "CANCELAR",
    "COIN",
)

t_QUANTIA = r"QUANTIA"
t_PRODUTO = r"PRODUTO"
t_CANCELAR = r"CANCELAR"
t_COIN = r"c\d+|e\d+"

t_ignore = " \t\n"


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex()


def vending_machine(input_string):
    balance = 0
    price = 0
    product = None
    coins_accepted = {
        "c5": 0.05,
        "c10": 0.10,
        "c20": 0.20,
        "c50": 0.50,
        "e1": 1.00,
        "e2": 2.00,
    }

    commands = re.split(
        r"\. ?|, ?", input_string
    )  # Split the input string into separate commands
    for command in commands:
        lexer.input(command)

        for token in lexer:
            if token.type == "QUANTIA":
                coins = re.findall(t_COIN, command)
                for coin in coins:
                    if coin in coins_accepted:
                        value = coins_accepted[coin]
                        balance += value
                        print(f"valor inserido: €{value:.2f} (saldo: €{balance:.2f})")
                    else:
                        print(f"({coin} moeda não aceite!)")
            elif token.type == "PRODUTO":
                product_search = re.search(r"PRODUTO=(\w+)", command)
                if product_search:
                    product = product_search.group(1)
                    price = 2.30  # Set the price for the product
                    if balance >= price:
                        balance -= price
                        print(f"compra: '{product}', €{price:.2f} (sem troco)")
                    else:
                        print(
                            f"preço: €{price:.2f} (quantia insuficiente) (saldo: €{balance:.2f})"
                        )
                else:
                    print("Invalid product format")
            elif token.type == "CANCELAR":
                print(f"valor devolvido: €{balance:.2f} (1 moeda de e1)")
                balance = 0


if __name__ == "__main__":
    input_string = " ".join(sys.argv[1:])
    vending_machine(input_string)
