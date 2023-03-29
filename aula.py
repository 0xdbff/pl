# V = {"a", "b"}
# Q = {"q0", "q1", "q2", "q3"}
# tt = {
#     "q0": {"a": "q1", "b": "q3"},
#     "q1": {"a": "q3", "b": "q2"},
#     "q2": {"a": "q2", "b": "q2"},
#     "q3": {"a": "q3", "b": "q3"},
# }
# q0 = "q0"
# F = {"q2"}
#
#
# def reconhece(palavra):
#     alpha = q0
#     while len(palavra) and alpha != "ERRO":
#         simbolo_atual = palavra[0]
#         alpha = tt[alpha][simbolo_atual] if simbolo_atual in V else "ERRO"
#         palavra = palavra[1:]
#     return (len(palavra) == 0) and (alpha in F)
#
#
# def test_reconhece():
#     palavra = ["aba", "ba", "baaa"]
#     for p in palavra:
#         print(f"{reconhece(p)}")
#
#
# test_reconhece()

# print(f"q0 => {tt[q0]}")
# print(f'{reconhece("aba")}')
# print(f'{reconhece("ba")}')
# print(f'{reconhece("abac")}')
# print(f'{reconhece("abaa")}')
# print(f'{reconhece("baaa")}')
# print(f'{reconhece("abaca")}')

# from graphviz import Digraph
#
#
# def create_nfa_graph():
#     dot = Digraph()
#
#     # Add states
#     for i in range(10):
#         dot.node(f"q{i}", f"q{i}")
#
#     # Add transitions
#     dot.edges([("q0", "q1"), ("q0", "q2")])  # Sign transitions
#     dot.edge("q1", "q3", label="0-9")  # Digit transitions
#     dot.edge("q2", "q3", label="0-9")
#     dot.edge("q3", "q3", label="0-9")
#
#     dot.edge("q3", "q4", label=".")  # Decimal transitions
#     dot.edge("q4", "q5", label="0-9")
#     dot.edge("q5", "q5", label="0-9")
#
#     dot.edges([("q3", "q6"), ("q5", "q6")])  # Exponent transitions
#     dot.edge("q6", "q7", label="e,E")
#     dot.edges([("q7", "q8"), ("q7", "q9")])  # Sign transitions
#     dot.edge("q8", "q10", label="0-9")  # Digit transitions
#     dot.edge("q9", "q10", label="0-9")
#     dot.edge("q10", "q10", label="0-9")
#
#     return dot
#
#
# nfa_graph = create_nfa_graph()
# nfa_graph.view()

V = {"d", "+", "-", ".", "e", "E"}
Q = {
    "q00",
    "q01",
    "q02",
    "q03",
    "q04",
    "q05",
    "q06",
    "q07",
    "q08",
    "q09",
    "q10",
    "q11",
    "q12",
    "q13",
    "q14",
    "q15",
    "q16",
    "q17",
    "q18",
    "q19",
    "q20",
    "q21",
}
tt = {
    "q01": {"": "q02"},
    "q02": {
        "": "q03",
        "-": "q04",
        "d": "q05",
        "+": "q06",
    },
    "q03": {
        "": "q07",
        ".": "q08",
    },
    "q04": {
        "": "q03",
        "d": "q05",
    },
    "q05": {
        "": "q03",
        "d": "q05",
    },
    "q06": {
        "": "q09",
    },
    "q07": {
        "": "q10",
        "e": "q11",
    },
    "q08": {
        "d": "q12",
    },
    "q09": {
        "": "q03",
        "d": "q05",
    },
    "q10": {
        "E": "q13",
    },
    "q11": {
        "": "q14",
    },
    "q12": {
        "": "q07",
        "d": "q15",
    },
    "q13": {
        "": "q16",
    },
    "q14": {
        "": "q16",
    },
    "q15": {
        "": "q07",
        "d": "q15",
    },
    "q16": {
        "-": "q17",
        "d": "q18",
        "+": "q19",
    },
    "q17": {
        "d": "q18",
    },
    "q18": {
        "d": "q20",
    },
    "q19": {
        "": "q21",
    },
    "q20": {
        "d": "q20",
    },
    "q21": {
        "d": "q6",
    },
}

q0 = "q01"
F = {"q07", "q18", "q20"}


def is_float(string):
    """ """
    current_state = q0
    for char in string:
        current_state = tt.get(current_state, {}).get(char, None)
        if current_state is None:
            return False
    return current_state in F


test_cases = [
    ("ddd", True),
    ("-ddd", True),
    ("+ddd", True),
    ("ddd.dd", True),
    (".dd", True),
    ("-ddd.dd", True),
    ("+ddd.dd", True),
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

# from graphviz import Digraph
#
# dot = Digraph("test")
#
# dot.format = "png"
# dot.attr("graph", dpi="100")
# dot.attr("graph", height="50", width="10")
#
# # Adicionar estados
# for state in tt.keys():
#     shape = "circle"
#     dot.node(state, state, shape=shape)
#
# # Adicionar transições
# for state, transitions in tt.items():
#     for symbol, next_state in transitions.items():
#         dot.edge(state, next_state, label=symbol)
#
# # Visualizar e guardar o grafo
# dot.view()
