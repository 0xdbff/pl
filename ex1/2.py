V = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
Q = {"s2", "s3"}

tt = {
    "s2": {
        "0": "s2",
        "1": "s2",
        "2": "s2",
        "3": "s2",
        "4": "s2",
        "5": "s2",
        "6": "s2",
        "7": "s2",
        "8": "s2",
        "9": "s2",
        "ε": "s3",
    },
    "s3": {},
}
q0 = "s2"
F = {"s3"}


from graphviz import Digraph

dot = Digraph("NFA 2")

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
