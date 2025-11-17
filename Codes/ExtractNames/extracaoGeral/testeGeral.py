import os
import pdfplumber
import spacy
import re
from fpdf import FPDF
from datetime import datetime
import json
import requests


# ======================================================================
#  1. CONFIGURAÇÕES DE PASTAS
# ======================================================================

PASTA_PDFS = r"E:\ProjetosEstagio\extrairNomes\pdfs_teste\pdfsEntrada"
PASTA_RESULTADOS = r"E:\ProjetosEstagio\extrairNomes\pdfs_teste\pdfsSaida"
CAMINHO_IBGE = r"E:\ProjetosEstagio\extrairNomes\baseDados\ibge_nomes.json"

os.makedirs(PASTA_RESULTADOS, exist_ok=True)


# ======================================================================
#  2. NPL DO SPACY
# ======================================================================

nlp = spacy.load("pt_core_news_sm") # Carrega o modelo de NPL do spaCy para português.


STOP_FINAIS = {
    "Além", "Depois", "Entretanto", "Portanto",
    "Empresa", "Endereço", "CPF", "RG", "CNPJ",
    "Objeto", "Assinatura", "Rua", "Avenida",
    "Telefone", "Email", "Documento", "Data",
    "Local", "Cidade", "Estado", "Brasil",
    "Contrato", "Relatório", "Processo"
}

CONECTORES = {"de", "da", "do", "dos", "das", "e"}


# ======================================================================
#   3. SISTEMA DE GÊNERO: IBGE + API
# ======================================================================

with open(CAMINHO_IBGE, "r", encoding="utf-8") as f:
    IBGE_DATA = json.load(f)


def genero_ibge(nome_completo):
    primeiro = nome_completo.split()[0].capitalize()

    if primeiro not in IBGE_DATA:
        return None, None

    dados = IBGE_DATA[primeiro]
    M = dados["M"]
    F = dados["F"]

    if M > F:
        return "Masculino", "IBGE"
    elif F > M:
        return "Feminino", "IBGE"
    else:
        return "Indefinido", "IBGE"


def genero_api(nome):
    try:
        primeiro = nome.split()[0]
        url = f"https://api.genderize.io/?name={primeiro}"
        r = requests.get(url, timeout=5).json()

        genero = r.get("gender")
        prob = r.get("probability", 0)

        if genero == "male":
            return "Masculino", f"API ({prob})"
        elif genero == "female":
            return "Feminino", f"API ({prob})"
        else:
            return "Indefinido", "API"
    except:
        return "Indefinido", "API (erro)"


def detectar_genero(nome):
    genero, fonte = genero_ibge(nome)
    if genero is not None:
        return genero, fonte
    return genero_api(nome)


# ======================================================================
#   4. EXTRAÇÃO DE TEXTO DO PDF
# ======================================================================

def extrair_texto_pdf(caminho_pdf: str) -> str:
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += (pagina.extract_text() or "") + "\n"
    texto = texto.replace("\r", " ").replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# Tornar o texto limpo para NPL e Regex


# ======================================================================
#   5. EXTRAÇÃO DE NOMES (NPL + REGEX)
# ======================================================================

def limpar_nome_final(nome: str) -> str | None:
    if not nome:
        return None

    nome = nome.strip(".,;:() ").strip() #strip retirar espaços, pontos etc
    partes = nome.split() #split separar

    while partes and partes[-1] in STOP_FINAIS:
        partes.pop()

    return " ".join(partes) or None


def extrair_nomes_por_nlp(texto: str) -> list[str]:
    doc = nlp(texto)
    nomes = []

    for ent in doc.ents:
        if ent.label_ != "PER": # PER = Pessoa
            continue

        tokens = []

        for token in ent:
            t = token.text.strip(".,;:()")

            if t in CONECTORES:
                tokens.append(t)
                continue

            if token.pos_ == "PROPN":
                tokens.append(t)
                continue

            break

        nome_final = limpar_nome_final(" ".join(tokens))

        if nome_final and nome_final not in nomes:
            nomes.append(nome_final)

    return nomes


def extrair_nomes_por_regex(texto: str) -> list[str]:
    padrao = r"\b[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+(?:\s(?:[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+|de|da|do|dos|das|e)){1,4}\b"
    matches = re.findall(padrao, texto)
    nomes = []

    for m in matches:
        nome_final = limpar_nome_final(m)
        if nome_final and nome_final not in nomes:
            nomes.append(nome_final)

    return nomes


def filtrar_lista_nomes(nomes):
    final = []
    for nome in nomes:
        partes = nome.split()
        if partes[-1] in STOP_FINAIS:
            continue
        if nome not in final:
            final.append(nome)
    return final


# ======================================================================
#   6. GERAR RELATÓRIO PDF
# ======================================================================

def gerar_pdf_relatorio(nome_arquivo_pdf: str, nomes_encontrados: list[str]):
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_saida = os.path.splitext(nome_arquivo_pdf)[0]
    caminho_saida = os.path.join(PASTA_RESULTADOS, f"resultado_{nome_saida}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Análise de PDF", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Arquivo: {nome_arquivo_pdf}", ln=True)
    pdf.cell(0, 10, f"Data: {data}", ln=True)
    pdf.ln(8)

    if nomes_encontrados:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Nomes identificados:", ln=True)
        pdf.ln(4)

        for nome in nomes_encontrados:
            genero, fonte = detectar_genero(nome)
            linha = f"- {nome}  |  Gênero: {genero}  |  Fonte: {fonte}"
            pdf.multi_cell(0, 8, linha)

    else:
        pdf.set_text_color(200, 0, 0)
        pdf.multi_cell(0, 10, "Nenhum nome foi identificado.")
        pdf.set_text_color(0, 0, 0)

    pdf.output(caminho_saida)
    print(f"Relatório salvo em: {caminho_saida}")


# ======================================================================
#   7. PROCESSAMENTO PRINCIPAL
# ======================================================================

def identificar_nome_pdf(nome_arquivo):
    caminho_pdf = os.path.join(PASTA_PDFS, nome_arquivo)

    if not os.path.exists(caminho_pdf):
        print(f"Arquivo não encontrado: {caminho_pdf}")
        return

    print(f"\nProcessando: {nome_arquivo} ...")

    texto = extrair_texto_pdf(caminho_pdf)

    nomes_nlp = extrair_nomes_por_nlp(texto)
    nomes_regex = extrair_nomes_por_regex(texto)

    nomes = filtrar_lista_nomes(nomes_nlp + nomes_regex)

    if nomes:
        print("\nNomes encontrados:")
        for n in nomes:
            genero, fonte = detectar_genero(n)
            print(f" - {n:<30} → {genero}  ({fonte})")
    else:
        print("Nenhum nome identificado.")

    gerar_pdf_relatorio(nome_arquivo, nomes)


def processar_todos_os_pdfs():
    arquivos = sorted(f for f in os.listdir(PASTA_PDFS) if f.lower().endswith(".pdf"))

    if not arquivos:
        print("Nenhum PDF encontrado.")
        return

    print(f"\nProcessando todos os PDFs da pasta: {PASTA_PDFS}")
    for nome_arquivo in arquivos:
        identificar_nome_pdf(nome_arquivo)
    print("\nConcluído!")


# ======================================================================
#   8. MENU PRINCIPAL
# ======================================================================

if __name__ == "__main__":
    print(f"Pasta dos PDFs: {PASTA_PDFS}\n")
    print("Escolha uma opção:")
    print("1 - Processar um PDF específico")
    print("2 - Processar todos os PDFs")

    op = input("\nDigite 1 ou 2: ")

    if op == "1":
        nome = input("Nome do arquivo PDF: ").strip()
        identificar_nome_pdf(nome)

    elif op == "2":
        processar_todos_os_pdfs()

    else:
        print("Opção inválida.")
