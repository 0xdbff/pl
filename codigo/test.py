import ply.lex as plex

tokens = ("I", "V", "IV", "OTHER")

total = 0


def t_I(t):
    r"I"
    global total
    total += 1
    pass


def t_V(t):
    r"V"
    global total
    total += 5
    pass


def t_IV(t):
    r"IV"
    global total
    total += 4
    pass


def t_OTHER(t):
    r".|\n"
    global total
    pass


def t_error(t):
    exit(1)


lexer = plex.lex()
lexer.input("IV")
lexer.token()

print(f"{total}")
