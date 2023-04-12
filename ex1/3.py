V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
Q = {"s4", "s6"}

tt = {
    "s4": {
        "ε": "s6",
        ".": "s5",
    },
    "s5": {
        "0": "s5",
        "1": "s5",
        "2": "s5",
        "3": "s5",
        "4": "s5",
        "5": "s5",
        "6": "s5",
        "7": "s5",
        "8": "s5",
        "9": "s5",
    },
    "s6": {},
}
q0 = "s4"
F = {"s5","s6"}

from graphviz import Digraph

dot = Digraph("NFA 3")

dot.format = "png"
dot.attr("graph", dpi="300")
# dot.attr("graph", height="50", width="10")

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

# Visualize and save the graph
dot.view()
