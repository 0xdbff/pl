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

    tokens = [
        "string",
        "number",
        # "comma",
        # "semicolon",
        "times",
        "plus",
        "identifier",
        "keyword",
    ] + list(keywords.values())

    literals = ["{", "}", "+", "-", "*", "/", ">", "<", "&", "|"]
    t_ignore = " \t"

    @lex.TOKEN(r"[a-zA-Z_][a-zA-Z_0-9]*")
    def t_identifier(self, t):
        try:
            if self.keywords.get(t.value) is not None:
                t.type = "keyword"
            elif self.reserved.get(t.value) is not None:
                t.type = "identifier"
            else:
                raise ValueError(
                    "The token is not a valid identifier or keyword, "
                    "check the list of reserved keywords!"
                )
            print(t.type)
            print(t.value)
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
            elif t.value.lower().startswith("0b"):
                t.value = int(t.value, 2)
            elif t.value.lower().startswith("0o"):
                t.value = int(t.value, 8)
            elif t.value.lower().startswith("0x"):
                t.value = int(t.value, 16)
            else:
                t.value = int(t.value)
        except ValueError:
            print(f"Could not parse number: {t.value}")
        return t

    # t_comma = r","
    # t_semicolon = r";"
    t_times = r"\*"
    t_plus = r"\+"

    def t_comment(self, t):
        r"//.*"
        pass

    def t_multiline_comment(self, t):
        r"/\*(.|\n)*?\*/"
        pass

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def p_statement(self, p):
        "statement : keyword arguments ';'"
        p[0] = Node("statement", [p[2]])

    def p_arguments(self, p):
        """arguments : arguments ',' expression
        | expression"""
        if len(p) == 2:
            p[0] = Node("arguments", [p[1]])
        else:
            p[0] = Node("arguments", p[1].children + [p[3]])

    def p_expression(self, p):
        """expression : expression plus term
        | expression times term
        | term"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Node("expression", [copy.deepcopy(p[1]), p[3], p[2]])

    def p_term(self, p):
        """term : number
        | string"""
        p[0] = Node("term", [p[1]])

    def p_error(self, p):
        if p:
            print(f"syntax error at '{p.value}'")
        else:
            print("syntax error at EOF")

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)

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
        if tree.type == "statement":
            if tree.children[0].type == "arguments":
                for arg in tree.children[0].children:
                    if arg.type == "term":
                        print(arg.children[0])
                    elif arg.type == "expression":
                        op = arg.children[2]
                        if op == "+":
                            print(
                                arg.children[0].children[0]
                                + arg.children[1].children[0]
                            )
                        elif op == "*":
                            print(
                                arg.children[0].children[0]
                                * arg.children[1].children[0]
                            )


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


def main():
    interpreter = Interpreter()
    interpreter.run()


if __name__ == "__main__":
    main()
