import ply.lex as lex

# Ignore whitespace
t_ignore = " \t\n"
# Define tokens
tokens = ("FLOAT", "INVALID")


# Regular expression for FLOAT token
def t_FLOAT(t):
    r"^[+-]?((\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)$"
    t.value = float(t.value)
    return t


# Regular expression for INVALID token
def t_INVALID(t):
    r"[^\s]+"
    return t


# Build the lexer
lexer = lex.lex()

test_cases = [
    # valid
    "123",
    "-123",
    "+123",
    "123.45",
    ".45",
    "-123.45",
    "+123.45",
    "1.23e-4",
    "-1.23E4",
    "1.23e+4",
    "1.23E-4",
    "1.23E4",
    # invalid
    "2.",
    "abc",
    "123a",
    "--123",
    "123.45.67",
    "123.45.67",
    "123.45a",
    "123a2",
    "123e2.2",
    "123    ",
    "  123  ",
]

for test_case in test_cases:
    lexer.input(test_case)
    tokens = list(lexer)

    if len(tokens) == 1 and tokens[0].type == "FLOAT":
        print(f"{test_case}: {tokens[0].type} {tokens[0].value}")
    else:
        print(f"{test_case}: INVALID")
