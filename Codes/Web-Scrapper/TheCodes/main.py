import os 
from extrator_web import extrair_citacoes
from gerador_pdf import criar_pdf_de_html 


URL_ALVO = "http://quotes.toscrape.com/"

PASTA_RELATORIOS = "relatorios_pdf"

def obter_configuracoes():
    
    print("--- Configurando a Busca ---")
    
    filtro_autor = input("Digite o nome do autor (deixe em branco para nenhum): ").strip()
    if not filtro_autor: filtro_autor = None

    tags_input = input("Digite as tags separadas por vírgula (ex: life,love) (em branco para nenhuma): ").strip()
    if tags_input:
        filtro_tags = [tag.strip().lower() for tag in tags_input.split(',')]
    else:
        filtro_tags = None

    while True:
        try:
            max_paginas = int(input("Número MÁXIMO de páginas para buscar (MAX: 10): "))
            if max_paginas > 0: break
            print("Por favor, digite um número maior que 0.")
        except ValueError:
            print("Entrada inválida. Digite apenas um número.")

    while True:
        try:
            max_citacoes = int(input(f"Número MÁXIMO de citações para salvar (ex: 10): "))
            if max_citacoes > 0: break
            print("Por favor, digite um número maior que 0.")
        except ValueError:
            print("Entrada inválida. Digite apenas um número.")
            
    print("--------------------------------\n")
    return filtro_autor, filtro_tags, max_paginas, max_citacoes

def rodar_automacao():
    print("--- INICIANDO PROCESSO DE AUTOMAÇÃO ---")
    
    filtro_autor, filtro_tags, max_paginas, max_citacoes = obter_configuracoes()

    # --- 2. FASE DE EXTRAÇÃO ---
    try:
        dados_extraidos = extrair_citacoes(
            url_base=URL_ALVO,
            filtro_autor=filtro_autor,
            filtro_tags=filtro_tags,
            max_paginas=max_paginas,
            max_citacoes=max_citacoes
        )
    except Exception as e:
        print(f"Erro crítico durante a extração: {e}")
        return

    # --- 3. FASE DE ANÁLISE ---
    if not dados_extraidos:
        print("Nenhum dado foi extraído (ou nenhum correspondeu aos filtros). Encerrando.")
        return
        
    total_citacoes = len(dados_extraidos)
    print(f"\n--- Análise Concluída: {total_citacoes} citações salvas. ---\n")

    # --- 4. FASE DE EXECUÇÃO (GERAR PDF) ---
    try:
        
        nome_base_pdf = "relatorio_citacoes.pdf"
        if filtro_autor:
            nome_base_pdf = f"relatorio_autor_{filtro_autor.replace(' ', '_').lower()}.pdf"
        elif filtro_tags:
            nome_base_pdf = f"relatorio_tags_{'_'.join(filtro_tags)}.pdf"
            
        
        os.makedirs(PASTA_RELATORIOS, exist_ok=True) 
        caminho_completo_pdf = os.path.join(PASTA_RELATORIOS, nome_base_pdf)
            
        criar_pdf_de_html(dados_extraidos, caminho_completo_pdf)
        
    except Exception as e:
        print(f"Erro crítico durante a geração do PDF: {e}")
        return
        
    print("--- PROCESSO DE AUTOMAÇÃO FINALIZADO ---")

if __name__ == "__main__":
    rodar_automacao()
