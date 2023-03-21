V = {"a", "b"}
Q = {"q0", "q1", "q2", "q3"}
tt = {
    "q0": {"a": "q1", "b": "q3"},
    "q1": {"a": "q3", "b": "q2"},
    "q2": {"a": "q2", "b": "q2"},
    "q3": {"a": "q3", "b": "q3"},
}
q0 = "q0"
F = {"q2"}


def reconhece(palavra):
    alpha = q0
    while len(palavra) and alpha != "ERRO":
        simbolo_atual = palavra[0]
        alpha = tt[alpha][simbolo_atual] if simbolo_atual in V else "ERRO"
        palavra = palavra[1:]
    return (len(palavra) == 0) and (alpha in F)


def test_reconhece():
    palavra = ["aba", "ba", "baaa"]
    for p in palavra:
        print(f"{reconhece(p)}")


test_reconhece()

# print(f"q0 => {tt[q0]}")
# print(f'{reconhece("aba")}')
# print(f'{reconhece("ba")}')
# print(f'{reconhece("abac")}')
# print(f'{reconhece("abaa")}')
# print(f'{reconhece("baaa")}')
# print(f'{reconhece("abaca")}')
