from graphviz import Digraph
import os


class Node:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children if children is not None else []

    def _to_graphviz(self, g=None):
        if g is None:
            g = Digraph("g")

        name = f"{id(self)}"
        g.node(name, label=self.type)

        for child in self.children:
            if isinstance(child, Node):
                child._to_graphviz(g)
                g.edge(name, f"{id(child)}")
            else:
                child_name = f"{id(child)}"
                g.node(child_name, label=str(child), shape="box")
                g.edge(name, child_name)

        return g

    def build_graph(self):
        g = self._to_graphviz()
        g.render(filename="syntax_tree", format="png")
        os.remove("syntax_tree")
