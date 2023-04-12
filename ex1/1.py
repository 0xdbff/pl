V = {"+", "-"}
Q = {"s0", "s1"}

tt = {
    "s0": {
        "+": "s1",
        "-": "s1",
        "ε": "s1",
    },
    "s1": {},
}
q0 = "s0"
F = {"s1"}


from graphviz import Digraph

dot = Digraph("NFA 1")

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
