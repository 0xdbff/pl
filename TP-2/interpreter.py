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
        root = self.parser.build_ast(s)
        if root is not None:
            print(self.eval(root))
            root.build_graph()

    def eval(self, node):
        """
        Dispatch method that calls the appropriate method based on
        node type.
        """
        method_name = f"eval_{node.type}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def eval_number(self, node):
        return node.value

    def eval_name(self, node):
        return self.parser.vars[node.value]

    def eval_binop(self, node):
        left = self.eval(node.children[0])
        right = self.eval(node.children[1])
        if node.value == "+":
            return left + right
        elif node.value == "-":
            return left - right
        elif node.value == "*":
            return left * right
        elif node.value == "/":
            return left / right

    def eval_uminus(self, node):
        return -self.eval(node.children[0])

    def eval_assign(self, node):
        self.parser.vars[node.value] = self.eval(node.children[0])
        return self.parser.vars[node.value]

    def eval_statement(self, node):
        return self.eval(node.children[0])

    def eval_group(self, node):
        return self.eval(node.children[0])

    def eval_print(self, node):
        value = self.eval(node.children[0])
        print(value)
        return value

    def eval_var(self, node):
        self.parser.vars[node.value] = self.eval(node.children[0])
        return self.parser.vars[node.value]


def main():
    interpreter = Interpreter()
    interpreter.run()


if __name__ == "__main__":
    main()
