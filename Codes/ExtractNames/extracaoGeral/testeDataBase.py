import json
caminho_arquivo = r"E:\ProjetosEstagio\extrairNomes\baseDados\ibge_nomes.json"
with open( caminho_arquivo, "r", encoding="utf-8") as f:
    ibge_nomes = json.load(f)

def genero_ibge(nome_completo):
    primeiro = nome_completo.split()[0].capitalize()

    if primeiro not in ibge_nomes:
        return "Indefinido", "IBGE"

    dados = ibge_nomes[primeiro]
    M = dados["M"]
    F = dados["F"]

    if M > F:
        return "Masculino", "IBGE"
    elif F > M:
        return "Feminino", "IBGE"
    else:
        return "Indefinido", "IBGE"



nomes = input("Digite os nomes separados por vírgula: ").split(",")
for nome in nomes:
    g, f = genero_ibge(nome)
    print(f"{nome:<10} → {g}  (Fonte: {f})")
