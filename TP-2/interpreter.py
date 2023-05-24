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
        try:
            root = self.parser.build_ast(s)
            if root is not None:
                root.traverse()
                self.eval(root)
                root.build_graph()
        except Exception as e:
            print(e)

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
        try:
            return self.parser.vars[node.value]
        except KeyError:
            raise NameError(f"Variable '{node.value}' is not defined")

    def eval_binop(self, node):
        left = self.eval(node.children[0])
        right = self.eval(node.children[1])

        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise ValueError("Both operands must be numbers")

        if node.value == "+":
            return left + right
        elif node.value == "-":
            return left - right
        elif node.value == "*":
            return left * right
        elif node.value == "/":
            if right == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return left / right

    def eval_uminus(self, node):
        return -self.eval(node.children[0])

    def eval_assign(self, node):
        self.parser.vars[node.value] = self.eval(node.children[0])
        return self.parser.vars[node.value]

    def eval_statement(self, node):
        return self.eval(node.children[0])

    def eval_expression(self, node):
        return [self.eval(child) for child in node.children]

    def eval_group(self, node):
        return self.eval(node.children[0])

    def eval_print(self, node):
        if node.children is not None:
            for child in node.children:
                try:
                    values = self.eval(child)
                    for value in values:
                        print(value, end=" ")
                    print()
                except Exception as e:
                    print(f"Exception when evaluating print argument: {e}")
        else:
            print(node.value)

    def eval_var(self, node):
        self.parser.vars[node.value] = self.eval(node.children[0])
        return self.parser.vars[node.value]

    def eval_string(self, node):
        return node.value


def main():
    interpreter = Interpreter()
    interpreter.run()


if __name__ == "__main__":
    main()
