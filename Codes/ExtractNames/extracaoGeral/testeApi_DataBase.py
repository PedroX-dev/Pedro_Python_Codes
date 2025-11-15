import json
import requests

# -------------------------------
# 1. CARREGA DATASET IBGE
# -------------------------------

caminho_arquivo = r"E:\ProjetosEstagio\extrairNomes\baseDados\ibge_nomes.json"
with open( caminho_arquivo, "r", encoding="utf-8") as f:
    IBGE_DATA = json.load(f)


# -------------------------------
# 2. DETECTA GÊNERO VIA IBGE
# -------------------------------
def genero_ibge(nome_completo):
    primeiro = nome_completo.split()[0].capitalize()

    # Se não existir no dataset → retornamos None
    if primeiro not in IBGE_DATA:
        return None, None  # gênero, fonte

    dados = IBGE_DATA[primeiro]
    M = dados["M"]
    F = dados["F"]

    if M > F:
        return "Masculino", "IBGE"
    elif F > M:
        return "Feminino", "IBGE"
    else:
        return "Indefinido", "IBGE"


# -------------------------------
# 3. DETECTA GÊNERO VIA API
# -------------------------------
def genero_api(nome):
    try:
        primeiro = nome.split()[0]
        url = f"https://api.genderize.io/?name={primeiro}"

        r = requests.get(url, timeout=5).json()
        genero = r.get("gender")
        prob = r.get("probability", 0)

        if genero == "male":
            return ("Masculino", f"API ({prob})")
        elif genero == "female":
            return ("Feminino", f"API ({prob})")
        else:
            return ("Indefinido", "API")

    except Exception:
        return ("Indefinido", "API (erro)")


# -------------------------------
# 4. FUNÇÃO FINAL (IBGE + API)
# -------------------------------
def detectar_genero(nome):
    # 1° Tenta IBGE
    genero, fonte = genero_ibge(nome)
    if genero is not None:
        return genero, fonte

    # 2° Fallback → API
    return genero_api(nome)


# -------------------------------
# 5. TESTE
# -------------------------------
nomes_teste = input("Digite os nomes separados por vírgula: ").split(",")

for nome in nomes_teste:
    g, f = detectar_genero(nome)
    print(f"{nome:<10} → {g}  (Fonte: {f})")
