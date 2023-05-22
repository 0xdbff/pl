import ply.yacc as yacc
import ply.lex as lex
from graphviz import Digraph
import os
import copy
from reserved import reserved as py_c_keywords


class Interpreter:
    reserved = py_c_keywords

    keywords = {
        "stdout": "stdout",
        "var": "var",
        "const": "const",
        "stdin": "stdin",
        "fn": "fn",
        "return": "return",
        "while": "while",
        "for": "for",
        "in": "in",
        "not": "not",
        "and": "and",
        "or": "or",
        "break": "break",
        "continue": "continue",
    }

    arith_operators = {  # not listed in literals
        "equals": "equals",
        "less_or_equal": "less_or_equal",
        "greater_or_equal": "greater_or_equal",
    }

    tokens = (
        [
            "string",
            "number",
            "identifier",
            "keyword",
            "comment",
        ]
        + list(keywords.values())
        + list(arith_operators.values())
    )

    literals = ["{", "}", "+", "-", "*", "/", ">", "<", "&", "|", "(", ")", "!", ";"]
    t_ignore = " \t\0"

    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "="),
        # ("right", "**"),
        ("nonassoc", ">", "<", "==", "!=", "<=", ">="),
    )

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)

    @lex.TOKEN(r"[a-zA-Z_][a-zA-Z_0-9]*")
    def t_identifier(self, t):
        try:
            if self.keywords.get(t.value) is not None:
                t.type = "keyword"
            elif self.reserved.get(t.value) is None:
                t.type = "identifier"
            else:
                raise ValueError(
                    "The token is not a valid identifier or keyword, "
                    "check the list of reserved keywords!"
                )
            return t
        except ValueError as e:
            print(e)

    @lex.TOKEN(r'"[^"]*"')
    def t_string(self, t):
        try:
            t.value = t.value[1:-1]
            return t
        except ValueError as e:
            print(e)

    @lex.TOKEN(
        r"-?0[bB][01]+|-?0[oO][0-7]+|-?0[xX][0-9a-fA-F]+|-?\d+(\.\d+)?(e[-+]?\d+)?"
    )
    def t_number(self, t):
        try:
            if "e" in t.value or "." in t.value:
                t.value = float(t.value)
                t.type = "float_n"
            elif t.value.lower().startswith("0b"):
                t.value = int(t.value, 2)
                t.type = "bin_n"
            elif t.value.lower().startswith("0o"):
                t.value = int(t.value, 8)
                t.type = "octal_n"
            elif t.value.lower().startswith("0x"):
                t.value = int(t.value, 16)
                t.type = "hex_n"
            else:
                t.value = int(t.value)
                t.type = "int_n"
        except ValueError:
            print(f"Could not parse number: {t.value}")
        return t

    @lex.TOKEN(r"//.*")
    def t_comment(self, t):
        t.lexer.lineno += len(t.value)

    @lex.TOKEN(r"/\*(.|\n)*?\*/")
    @staticmethod
    def t_multiline_comment():
        pass

    @lex.TOKEN(r"\n+")
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def run(self):
        while True:
            try:
                s = input("> ")
            except EOFError:
                break
            if not s:
                continue
            tree = self.parser.parse(s, lexer=self.lexer)
            if tree is not None:
                self.process_tree(tree)
                g = tree.to_graphviz()
                g.render(filename="syntax_tree", format="png")
                os.remove("syntax_tree")

    def process_tree(self, tree):
        pass


class Node:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children if children is not None else []

    def to_graphviz(self, g=None):
        if g is None:
            g = Digraph("g")

        name = f"{id(self)}"
        g.node(name, label=self.type)

        for child in self.children:
            if isinstance(child, Node):
                child.to_graphviz(g)
                g.edge(name, f"{id(child)}")
            else:
                child_name = f"{id(child)}"
                g.node(child_name, label=str(child), shape="box")
                g.edge(name, child_name)

        return g
