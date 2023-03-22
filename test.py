transition_table = {
    "q0": {
        "+": "q1",
        "-": "q1",
        "0": "q2",
        "1": "q2",
        "2": "q2",
        "3": "q2",
        "4": "q2",
        "5": "q2",
        "6": "q2",
        "7": "q2",
        "8": "q2",
        "9": "q2",
        ".": "q3",
    },
    "q1": {
        "0": "q2",
        "1": "q2",
        "2": "q2",
        "3": "q2",
        "4": "q2",
        "5": "q2",
        "6": "q2",
        "7": "q2",
        "8": "q2",
        "9": "q2",
        ".": "q3",
    },
    "q2": {
        "0": "q2",
        "1": "q2",
        "2": "q2",
        "3": "q2",
        "4": "q2",
        "5": "q2",
        "6": "q2",
        "7": "q2",
        "8": "q2",
        "9": "q2",
        ".": "q3",
        "e": "q4",
        "E": "q4",
    },
    "q3": {
        "0": "q6",
        "1": "q6",
        "2": "q6",
        "3": "q6",
        "4": "q6",
        "5": "q6",
        "6": "q6",
        "7": "q6",
        "8": "q6",
        "9": "q6",
    },
    "q4": {
        "+": "q5",
        "-": "q5",
        "0": "q5",
        "1": "q5",
        "2": "q5",
        "3": "q5",
        "4": "q5",
        "5": "q5",
        "6": "q5",
        "7": "q5",
        "8": "q5",
        "9": "q5",
    },
    "q5": {
        "0": "q5",
        "1": "q5",
        "2": "q5",
        "3": "q5",
        "4": "q5",
        "5": "q5",
        "6": "q5",
        "7": "q5",
        "8": "q5",
        "9": "q5",
    },
    "q6": {
        "0": "q6",
        "1": "q6",
        "2": "q6",
        "3": "q6",
        "4": "q6",
        "5": "q6",
        "6": "q6",
        "7": "q6",
        "8": "q6",
        "9": "q6",
        "e": "q4",
        "E": "q4",
    },
}

final_states = {"q2", "q6", "q5"}


def is_float(string):
    """ """
    current_state = "q0"
    for char in string:
        current_state = transition_table.get(current_state, {}).get(char, None)
        if current_state is None:
            return False
    return current_state in final_states


test_cases = [
    ("123", True),
    ("-123", True),
    ("+123", True),
    ("123.45", True),
    (".45", True),
    ("-123.45", True),
    ("+123.45", True),
    ("1.23e-4", True),
    ("-1.23E4", True),
    ("1.23e+4", True),
    ("1.23E-4", True),
    ("1.23E4", True),
    ("2.", False),
    ("abc", False),
    ("123a", False),
    ("--123", False),
    ("123.45.67", False),
    ("123.45.67", False),
    ("123.45a", False),
    ("123a2", False),
    ("123e2.2", False),
    ("123    ", False),
    ("  123  ", False),
]


def test():
    """ """
    matched_tests = 0
    for string, expected in test_cases:
        result = is_float(string)
        padded_string = f"'{string}'".ljust(11)
        if result == expected:
            matched_tests += 1
        print(
            f"str: {padded_string} is a float? expected({str(expected).ljust(5)}) got -> {result}"
        )
    print(f"\nMatched {matched_tests} out of {len(test_cases)} test cases!")


test()

import ply.lex as lex

t_ignore = " \t\n"
# Define tokens
tokens = ("FLOAT", "INVALID")
# Ignore whitespace


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
