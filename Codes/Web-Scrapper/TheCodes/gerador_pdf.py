import jinja2
from xhtml2pdf import pisa
import os

def criar_pdf_de_html(dados, nome_arquivo="relatorio.pdf"):
    """
    Gera um PDF a partir de um template HTML ('template.html') e CSS ('estilo.css').
    """
    print(f"Iniciando geração do PDF: {nome_arquivo}")

    # Configura o Jinja2 para carregar o template da pasta atual
    template_loader = jinja2.FileSystemLoader(searchpath=".")
    template_env = jinja2.Environment(loader=template_loader)
    
    try:
        template_html = template_env.get_template("template.html")
    except jinja2.exceptions.TemplateNotFound:
        print("ERRO: Arquivo 'template.html' não encontrado na pasta.")
        return

    # Prepara o contexto de dados para o Jinja
    contexto = {
        "dados": dados,
        "total": len(dados)
    }
    
    # Renderiza o HTML com os dados injetados
    html_renderizado = template_html.render(contexto)
    
    # Função 'link_callback' para o xhtml2pdf encontrar o arquivo CSS
    def link_callback(uri, rel):
        # Transforma a URI (ex: 'estilo.css') em um caminho de sistema
        sUrl = os.path.join(".", uri.replace("/", os.sep))
        # Garante que o caminho é absoluto
        path = os.path.abspath(sUrl)
        if not os.path.isfile(path):
            print(f"AVISO: Arquivo de recurso não encontrado: {uri}")
            return None
        return path

    # Converte o HTML para PDF
    try:
        with open(nome_arquivo, "w+b") as result_file:
            # Converte o HTML para PDF
            pisa_status = pisa.CreatePDF(
                html_renderizado,       # O HTML a ser convertido
                dest=result_file,       # O arquivo de saída
                link_callback=link_callback # A função para encontrar o CSS
            )
            
        if not pisa_status.err:
            print(f"PDF gerado com sucesso: {nome_arquivo}")
        else:
            print(f"Erro ao gerar PDF: {pisa_status.err}")
            
    except Exception as e:
        print(f"Exceção ao escrever PDF: {e}")
