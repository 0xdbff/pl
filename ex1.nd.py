# \d = [009]
# REGEX "^[+-]?((\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)$"

V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", ".", "e", "E"}
Q = {"p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11"}

tt = {
    "p0": {
        "ε": {"p1", "p2", "p3"},
        "+": {"p2"},
        "-": {"p2"},
    },
    "p1": {"ε": {"p4"}},
    "p2": {
        "0": {"p4"},
        "1": {"p4"},
        "2": {"p4"},
        "3": {"p4"},
        "4": {"p4"},
        "5": {"p4"},
        "6": {"p4"},
        "7": {"p4"},
        "8": {"p4"},
        "9": {"p4"},
    },
    "p3": {".": {"p5"}},
    "p4": {
        "ε": {"p0", "p6"},
        "0": {"p4"},
        "1": {"p4"},
        "2": {"p4"},
        "3": {"p4"},
        "4": {"p4"},
        "5": {"p4"},
        "6": {"p4"},
        "7": {"p4"},
        "8": {"p4"},
        "9": {"p4"},
        ".": {"p5"},
        "e": {"p7"},
        "E": {"p7"},
    },
    "p5": {
        "0": {"p6"},
        "1": {"p6"},
        "2": {"p6"},
        "3": {"p6"},
        "4": {"p6"},
        "5": {"p6"},
        "6": {"p6"},
        "7": {"p6"},
        "8": {"p6"},
        "9": {"p6"},
    },
    "p6": {
        "ε": {"p0", "p11"},
        "0": {"p6"},
        "1": {"p6"},
        "2": {"p6"},
        "3": {"p6"},
        "4": {"p6"},
        "5": {"p6"},
        "6": {"p6"},
        "7": {"p6"},
        "8": {"p6"},
        "9": {"p6"},
        "e": {"p7"},
        "E": {"p7"},
    },
    "p7": {
        "ε": {"p9"},
        "+": {"p9"},
        "-": {"p9"},
        "0": {"p9"},
        "1": {"p9"},
        "2": {"p9"},
        "3": {"p9"},
        "4": {"p9"},
        "5": {"p9"},
        "6": {"p9"},
        "7": {"p9"},
        "8": {"p9"},
        "9": {"p9"},
    },
    "p8": {".": {"p5"}},
    "p9": {
        "0": {"p10"},
        "1": {"p10"},
        "2": {"p10"},
        "3": {"p10"},
        "4": {"p10"},
        "5": {"p10"},
        "6": {"p10"},
        "7": {"p10"},
        "8": {"p10"},
        "9": {"p10"},
    },
    "p10": {
        "0": {"p10"},
        "1": {"p10"},
        "2": {"p10"},
        "3": {"p10"},
        "4": {"p10"},
        "5": {"p10"},
        "6": {"p10"},
        "7": {"p10"},
        "8": {"p10"},
        "9": {"p10"},
    },
    "p11": {},
}

q0 = "p0"
F = {"p0", "p6", "p10"}


def is_float(string):
    """ """
    current_state = q0
    for char in string:
        next_state = tt.get(current_state, {}).get(char, None)
        if next_state is None:
            return False
        if isinstance(next_state, set):
            current_state = next(iter(next_state))
        else:
            current_state = next_state
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

dot = Digraph("Automato Finito Deterministico")

dot.format = "png"
dot.attr("graph", dpi="100")
dot.attr("graph", height="50", width="10")

# Add states
for state in tt.keys():
    shape = "circle"
    dot.node(state, state, shape=shape)

# Add transitions
for state, transitions in tt.items():
    for symbol, next_state in transitions.items():
        if isinstance(next_state, set):
            for ns in next_state:
                dot.edge(state, ns, label=symbol)
        else:
            dot.edge(state, next_state, label=symbol)

# Visualize and save the graph
dot.view()
