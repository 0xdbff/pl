from graphviz import Digraph
import os


class Node:
    """Representation of a node in an abstract syntax tree (AST).

    Attributes:
        type (str): The type of the node.
        value: The value of the node. The type of this attribute can be
               anything, and depends on the specific node.
        children (list[Node]): The child nodes of this node.
    """

    def __init__(self, type, value=None, children=None):
        """Initializes a Node.

        Args:
            type (str): The type of the node.
            value: The value of the node. Default is None.
            children (list[Node], optional): The child nodes of this node.
                                             Default is an empty list.
        """
        self.type = type
        self.value = value if value is not None else ""
        self.children = children if children is not None else []

    def _to_graphviz(self, g=None):
        """Recursively adds nodes to a Graphviz object to represent the subtree
        rooted at this node.

        Args:
            g (graphviz.Digraph, optional): The Graphviz object to which nodes
                                            will be added. If None, a new object
                                            is created. Default is None.

        Returns:
            graphviz.Digraph: The Graphviz object representing the subtree
                              rooted at this node.
        """
        if g is None:
            g = Digraph("g")

        name = f"{id(self)}"
        g.node(
            name,
            label=f"{self.type}: {self.value if self.value is not None else ''}",
        )

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
        """Generates a Graphviz representation of the AST rooted at this node,
        and saves it to a file named 'syntax_tree.png'."""
        g = self._to_graphviz()
        g.render(filename="syntax_tree", format="png")
        os.remove("syntax_tree")

    def __repr__(self):
        """Returns a string representation of this node and its children.

        Returns:
            str: A string representation of this node and its children.
        """
        return (
            f"<Node type={self.type}, value={self.value}, "
            + f"children=[{', '.join(repr(child) for child in self.children)}]>"
        )

    def traverse(self):
        """Perform a depth-first traversal of the tree rooted at this node."""
        print(self)
        for child in self.children:
            child.traverse()
