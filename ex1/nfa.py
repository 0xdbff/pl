V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "e", "E", "+", "-", "."}
Q = {"n0", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10"}

tt = {
    "n0": {
        "+": "n1",
        "-": "n1",
        "ε": "n1",
    },
    "n1": {
        "0": "n2",
        "1": "n2",
        "2": "n2",
        "3": "n2",
        "4": "n2",
        "5": "n2",
        "6": "n2",
        "7": "n2",
        "8": "n2",
        "9": "n2",
        "ε": "n3",
    },
    "n2": {
        "0": "n2",
        "1": "n2",
        "2": "n2",
        "3": "n2",
        "4": "n2",
        "5": "n2",
        "6": "n2",
        "7": "n2",
        "8": "n2",
        "9": "n2",
        "ε": "n4",
    },
    "n3": {
        "ε": "n5",
        ".": "n6",
    },
    "n4": {
        "ε": "n10",
        "e": "n7",
        "E": "n7",
    },
    "n5": {
        "0": "n5",
        "1": "n5",
        "2": "n5",
        "3": "n5",
        "4": "n5",
        "5": "n5",
        "6": "n5",
        "7": "n5",
        "8": "n5",
        "9": "n5",
    },
    "n6": {
        "ε": "n10",
        "e": "n7",
        "E": "n7",
    },
    "n7": {
        "ε": "n8",
        "+": "n8",
        "-": "n8",
    },
    "n8": {
        "0": "n9",
        "1": "n9",
        "2": "n9",
        "3": "n9",
        "4": "n9",
        "5": "n9",
        "6": "n9",
        "7": "n9",
        "8": "n9",
        "9": "n9",
    },
    "n9": {
        "0": "n9",
        "1": "n9",
        "2": "n9",
        "3": "n9",
        "4": "n9",
        "5": "n9",
        "6": "n9",
        "7": "n9",
        "8": "n9",
        "9": "n9",
    },
    # "n10": "",
}


q0 = "n0"
F = {"n3", "n5", "n9"}


def is_float(string):
    """ """
    current_state = q0
    for char in string:
        current_state = tt.get(current_state, {}).get(char, None)
        if current_state is None:
            return False
    return current_state in F


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
    ("2E2", True),
    ("2e2", True),
    ("2e2.2", False),
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


from graphviz import Digraph

dot = Digraph("nfa")

dot.format = "png"
dot.attr("graph", dpi="300")
dot.attr("graph", height="50", width="10")

for state in tt.keys():
    if state in F:
        shape = "doublecircle"  # Use doublecircle shape for final states
    else:
        shape = "circle"
    dot.node(state, state, shape=shape)

# Add transitions
for state, transitions in tt.items():
    for symbol, next_state in transitions.items():
        dot.edge(state, next_state, label=symbol)

# Visualizar e guardar o grafo
dot.view()
