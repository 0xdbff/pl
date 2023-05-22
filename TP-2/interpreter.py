from lexer import Lexer
from grammar import Grammar


class Interpreter:
    def __init__(self, **kwargs):
        self.lexer = Lexer(**kwargs)
        self.parser = Grammar(self.lexer, **kwargs)

    def run(self):
        while True:
            try:
                s = input("> ")
            except EOFError:
                break
            if not s:
                continue
            self._build_ast(s)

    def _build_ast(self, s):
        tree = self.parser.build_ast(s)
        if tree is not None:
            self.process_tree(tree)
            tree.build_graph()

    def process_tree(self, tree):
        if tree.type == "statement":
            if tree.children[0].type == "arguments":
                for arg in tree.children[0].children:
                    self.process_argument(arg)

    def process_argument(self, arg):
        if arg.type == "term":
            self.process_term(arg)
        elif arg.type == "expression":
            self.process_expression(arg)

    def process_term(self, term):
        print(term.children[0])

    def process_expression(self, expr):
        op = expr.children[2]
        left = expr.children[0]
        right = expr.children[1]

        left_val = None
        right_val = None

        if left.type == "term":
            left_val = left.children[0]
        elif left.type == "expression":
            left_val = self.process_expression(left)

        if right.type == "term":
            right_val = right.children[0]
        elif right.type == "expression":
            right_val = self.process_expression(right)
        if left_val is not None and right_val is not None:
            if op == "+":
                print(left_val + right_val)
            elif op == "*":
                print(left_val * right_val)


def main():
    interpreter = Interpreter()
    interpreter.run()


if __name__ == "__main__":
    main()
