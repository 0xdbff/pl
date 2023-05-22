import subprocess


class CCodeGenerator:
    def __init__(self, interpreter):
        self.c_code = "#include <stdio.h>\nint main() {\n"
        self.interpreter = interpreter

    def generate(self, tree):
        if tree.type == "statement":
            if tree.children[0].type == "arguments":
                for arg in tree.children[0].children:
                    value = self.interpreter.eval_expr(arg)
                    if isinstance(value, float):
                        self.c_code += f'printf("%.2lf\\n", {value});\n'
                    elif isinstance(value, int):
                        self.c_code += f'printf("%d\\n", {value});\n'

    def compile(self):
        self.c_code += "\nreturn 0;\n}"
        with open("output.c", "w") as f:
            f.write(self.c_code)
        subprocess.run(["gcc", "output.c", "-o", "output"], check=True)
