V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", ".", "e", "E"}
Q = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
tt = {
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

q0 = "q0"
F = {"q2", "q6", "q5"}


def is_recognized(string):
    """Verificar se a string é reconhecida pelo autómato"""
    current_state = q0
    for char in string:
        current_state = tt.get(current_state, {}).get(char, None)
        if current_state is None:
            return False
    return current_state in F


def cast_to_float(test_cases):
    """Converter para float as strings reconhecias pelo autómato"""
    print("\nConverting to float!")
    for string, expected in test_cases:
        if is_recognized(string) == expected and expected:
            float_repr = "{:,.10f}".format(float(string))
            print(f"{string.ljust(10)}: {float_repr}")


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
    """Testes unitários para testar a função de transição."""
    matched_tests = 0
    for string, expected in test_cases:
        result = is_recognized(string)
        padded_string = f"'{string}'".ljust(11)
        if result == expected:
            matched_tests += 1
        print(
            f"str: {padded_string} is a float? expected({str(expected).ljust(5)}) got -> {result}"
        )
    print(f"\nMatched {matched_tests} out of {len(test_cases)} test cases!")


test()

cast_to_float(test_cases)


from graphviz import Digraph


def graph():
    """Gerar o gráfico do autómato e guardar em png"""
    dot = Digraph("Automato Finito Deterministico")

    dot.format = "png"
    dot.attr("graph", dpi="300")

    for state in tt.keys():
        if state in F:
            shape = "doublecircle"
        else:
            shape = "circle"
        dot.node(state, state, shape=shape)

    for state, transitions in tt.items():
        for symbol, next_state in transitions.items():
            dot.edge(state, next_state, label=symbol)

    dot.view()


graph()
