import os
import pdfplumber
import spacy
import re
from fpdf import FPDF
from datetime import datetime

#  Caminhos padrão (ajuste se preciso)
PASTA_PDFS = r"C:\Users\pedro.lopes\OneDrive - CAMG\Área de Trabalho\PastaPDFsEntrada"
PASTA_RESULTADOS = r"C:\Users\pedro.lopes\OneDrive - CAMG\Área de Trabalho\PastaPDFsSaida\resultados"

# Garante que a pasta de resultados existe
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

# Modelo NLP do spaCy
nlp = spacy.load("pt_core_news_sm")

# 🔹 Palavras que NUNCA podem ser o último token de um nome
STOP_FINAIS = {
    "Além", "Depois", "Entretanto", "Portanto",
    "Empresa", "Endereço", "CPF", "RG", "CNPJ",
    "Objeto", "Assinatura", "Rua", "Avenida",
    "Telefone", "Email", "Documento", "Data",
    "Local", "Cidade", "Estado", "Brasil",
    "Contrato", "Relatório", "Processo"
}

CONECTORES = {"de", "da", "do", "dos", "das", "e"}


def extrair_texto_pdf(caminho_pdf: str) -> str:
    """Extrai texto de todas as páginas do PDF e normaliza espaços/linhas."""
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            pagina_texto = pagina.extract_text() or ""
            texto += pagina_texto + "\n"
    texto = texto.replace("\r", " ").replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def limpar_nome_final(nome: str) -> str | None:
    """
    Limpa pontuação, espaços extras e remove token final se ele for proibido.
    Ex.: 'Tulio Maravilha Além' -> 'Tulio Maravilha'
    """
    if not nome:
        return None

    nome = nome.strip(".,;:() ").strip()
    if not nome:
        return None

    partes = nome.split()
    # Remove tokens finais proibidos enquanto existirem
    while partes and partes[-1] in STOP_FINAIS:
        partes.pop()

    nome_limpo = " ".join(partes).strip()
    return nome_limpo or None


def extrair_nomes_por_nlp(texto: str) -> list[str]:
    """
    Usa o spaCy para extrair nomes de pessoa (PER), analisando o contexto.
    Garante que o nome termina antes de verbos, advérbios ou substantivos comuns,
    e corta nomes incorretamente estendidos (como 'Tulio Maravilha Além').
    """
    doc = nlp(texto)
    nomes: list[str] = []

    for ent in doc.ents:
        if ent.label_ != "PER":
            continue

        tokens_limpos: list[str] = []

        for token in ent:
            t = token.text.strip(".,;:()")

            # Conectores minúsculos permitidos
            if t in CONECTORES:
                tokens_limpos.append(t)
                continue

            # Nomes próprios (PROPN)
            if token.pos_ == "PROPN":
                tokens_limpos.append(t)
                continue

            # Se chegou aqui, é algo que não parece fazer parte do nome -> para
            break

        nome_bruto = " ".join(tokens_limpos).strip()
        nome_final = limpar_nome_final(nome_bruto)

        if nome_final and nome_final not in nomes:
            nomes.append(nome_final)

    return nomes


def extrair_nomes_por_regex(texto: str) -> list[str]:
    """
    Regex como fallback — cobre casos que o NLP não detecta.
    Permite conectores ('de', 'da', etc.), mas evita palavras contextuais.
    """
    padrao_nome = r"\b[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+(?:\s(?:[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+|de|da|do|dos|das|e)){1,4}\b"
    correspondencias = re.findall(padrao_nome, texto)
    nomes: list[str] = []

    for m in correspondencias:
        nome_bruto = m.strip()
        nome_final = limpar_nome_final(nome_bruto)
        if not nome_final:
            continue
        if nome_final not in nomes:
            nomes.append(nome_final)

    return nomes


def filtrar_lista_nomes(nomes: list[str]) -> list[str]:
    """
    Filtro final de segurança:
    - remove nomes que terminem com STOP_FINAIS
    - remove duplicados preservando a ordem
    """
    resultado: list[str] = []
    for nome in nomes:
        partes = nome.split()
        if not partes:
            continue
        if partes[-1] in STOP_FINAIS:
            continue
        if nome not in resultado:
            resultado.append(nome)
    return resultado


def gerar_pdf_relatorio(nome_arquivo_pdf: str, nomes_encontrados: list[str]):
    """Cria um PDF de relatório com o resultado da análise."""
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo_saida = os.path.splitext(nome_arquivo_pdf)[0]
    caminho_saida = os.path.join(PASTA_RESULTADOS, f"resultado_{nome_arquivo_saida}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Análise de PDF", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Arquivo analisado: {nome_arquivo_pdf}", ln=True)
    pdf.cell(0, 10, f"Data da análise: {data}", ln=True)
    pdf.ln(8)

    if nomes_encontrados:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Nomes identificados:", ln=True)
        pdf.ln(4)

        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 128, 0)
        for nome in nomes_encontrados:
            pdf.multi_cell(0, 8, f"- {nome}")
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_text_color(200, 0, 0)
        pdf.multi_cell(0, 10, "Nenhum nome foi identificado com confiança.")
        pdf.set_text_color(0, 0, 0)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Análise realizada automaticamente pelo sistema de extração de nomes.", ln=True, align="C")

    pdf.output(caminho_saida)
    print(f" Relatório salvo em: {caminho_saida}")


def identificar_nome_pdf(nome_arquivo: str):
    """Identifica TODOS os nomes em um PDF e gera relatório PDF."""
    caminho_pdf = os.path.join(PASTA_PDFS, nome_arquivo)

    if not os.path.exists(caminho_pdf):
        print(f" Arquivo não encontrado: {caminho_pdf}")
        return

    print(f"\nProcessando: {nome_arquivo} ...")

    texto = extrair_texto_pdf(caminho_pdf)

    nomes_nlp = extrair_nomes_por_nlp(texto)
    nomes_regex = extrair_nomes_por_regex(texto)

    # Junta listas
    nomes_combinados = nomes_nlp + nomes_regex

    # Filtro final de segurança
    nomes_encontrados = filtrar_lista_nomes(nomes_combinados)

    if nomes_encontrados:
        print("Nomes encontrados:")
        for n in nomes_encontrados:
            print(f" - {n}")
    else:
        print("Nenhum nome identificado.")

    gerar_pdf_relatorio(nome_arquivo, nomes_encontrados)


def processar_todos_os_pdfs():
    """Percorre todos os PDFs da pasta e gera relatórios para cada um."""
    arquivos = sorted(f for f in os.listdir(PASTA_PDFS) if f.lower().endswith(".pdf"))
    if not arquivos:
        print("Nenhum PDF encontrado na pasta padrão.")
        return

    print(f"\nProcessando TODOS os PDFs da pasta: {PASTA_PDFS}")
    for nome_arquivo in arquivos:
        identificar_nome_pdf(nome_arquivo)
    print("\n✅ Todos os PDFs foram processados com sucesso!")


if __name__ == "__main__":
    print(f"Pasta padrão dos PDFs: {PASTA_PDFS}\n")
    print("Escolha uma opção:")
    print("1 - Processar apenas um arquivo específico")
    print("2 - Processar todos os PDFs da pasta padrão")
    opcao = input("\nDigite 1 ou 2: ").strip()

    if opcao == "1":
        nome_arquivo = input("\nDigite o nome do arquivo PDF (ex: contrato.pdf): ").strip()
        identificar_nome_pdf(nome_arquivo)
    elif opcao == "2":
        processar_todos_os_pdfs()
    else:
        print("\n Opção inválida. Execute o programa novamente e escolha 1 ou 2.")
