import requests

def genero_api(nome):
    primeiro = nome.split()[0]
    url = f"https://api.genderize.io/?name={primeiro}"

    r = requests.get(url).json()

    genero = r.get("gender")
    probabilidade = r.get("probability")

    if genero == "male":
        return ("Masculino", probabilidade)
    elif genero == "female":
        return ("Feminino", probabilidade)
    else:
        return ("Desconhecido", probabilidade)
    


nomes = input("Digite os nomes separados por vírgula: ").split(",")
for nome in nomes:
    g, f = genero_api(nome)
    print(f"{nome:<10} → {g}  (Fonte: {f})")
