# arith.py
from arith_grammar import ArithGrammar

ag = ArithGrammar()
ag.build()
res = ag.parse("2+3*4")

print(f"Result: {res}")
