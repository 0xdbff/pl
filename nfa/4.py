V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "e", "E", "+", "-"}
Q = {"s7", "s8", "s9", "s10"}

tt = {
    "s7": {
        "ε": "s10",
        "e": "s8",
        "E": "s8",
    },
    "s8": {
        "ε": "s9",
        "+": "s9",
        "-": "s9",
    },
    "s9": {
        "0": "s9",
        "1": "s9",
        "2": "s9",
        "3": "s9",
        "4": "s9",
        "5": "s9",
        "6": "s9",
        "7": "s9",
        "8": "s9",
        "9": "s9",
    },
    "s10": {},
}


q0 = "s7"
F = {"s9", "s10"}


from graphviz import Digraph

dot = Digraph("NFA 4")

dot.format = "png"
dot.attr("graph", dpi="300")

# Add states
for state in tt.keys():
    if state in F:
        shape = "doublecircle"
    else:
        shape = "circle"
    dot.node(state, state, shape=shape)

# Add transitions
for state, transitions in tt.items():
    for symbol, next_state in transitions.items():
        dot.edge(state, next_state, label=symbol)

# Visualize and save the graph
dot.view()
