import ply.yacc as yacc
import ply.lex as lex
from graphviz import Digraph
import copy


class Interpreter:
    reserved = {"ESCREVER": "ESCREVER"}

    tokens = [
        "STRING",
        "NUMBER",
        "COMMA",
        "SEMICOLON",
        "TIMES",
        "PLUS",
    ] + list(reserved.values())

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.reserved.get(t.value, "ESCREVER")
        return t

    t_ignore = " \t"

    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    t_COMMA = r","
    t_SEMICOLON = r";"
    t_TIMES = r"\*"
    t_PLUS = r"\+"

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
        "statement : ESCREVER arguments SEMICOLON"
        p[0] = Node("statement", [p[2]])

    def p_arguments(self, p):
        """arguments : arguments COMMA expression
        | expression"""
        if len(p) == 2:
            p[0] = Node("arguments", [p[1]])
        else:
            p[0] = Node("arguments", p[1].children + [p[3]])

    def p_expression(self, p):
        """expression : expression PLUS term
        | expression TIMES term
        | term"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[2] == "+":
                p[0] = Node("expression", [copy.deepcopy(p[1]), p[3]])
            elif p[2] == "*":
                p[0] = Node("expression", [copy.deepcopy(p[1]), p[3]])

    def p_term(self, p):
        """term : NUMBER
        | STRING"""
        p[0] = Node("term", [p[1]])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

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
                g = tree.to_graphviz()
                g.render(filename="syntax_tree", format="png")


class Node:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children if children is not None else []

    def to_graphviz(self, g=None):
        if g is None:
            g = Digraph("G")

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
