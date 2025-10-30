from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

def extrair_citacoes(url_base, filtro_autor=None, filtro_tags=None, max_paginas=1, max_citacoes=10):
    """
    Abre uma URL, navega pelas páginas e extrai citações com base em filtros.
    """
    print("Configurando o driver do navegador...")
    service = Service(ChromeDriverManager().install())
    
    # Adiciona opção para rodar "headless" (sem abrir a janela do navegador)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    dados_extraidos = []
    pagina_atual = 1
    url_atual = url_base

    while pagina_atual <= max_paginas:
        
        print(f"\n--- Buscando na Página {pagina_atual} ---")
        print(f"URL: {url_atual}")
        driver.get(url_atual)
        time.sleep(0.5) 
        
        elementos_quote = driver.find_elements(By.CLASS_NAME, "quote")
        
        if not elementos_quote:
            print("Nenhuma citação encontrada nesta página.")
            break 

        print(f"Encontradas {len(elementos_quote)} citações. Aplicando filtros...")
        
        for quote in elementos_quote:
            texto = quote.find_element(By.CLASS_NAME, "text").text
            autor = quote.find_element(By.CLASS_NAME, "author").text
            elementos_tag = quote.find_elements(By.CLASS_NAME, "tag")
            tags_da_citacao = [tag.text.lower() for tag in elementos_tag]

            # --- LÓGICA DOS FILTROS ---
            
            autor_ok = (not filtro_autor) or (filtro_autor.lower() in autor.lower())
            
            tags_ok = (not filtro_tags) or any(user_tag in tags_da_citacao for user_tag in filtro_tags)
            
            if autor_ok and tags_ok:
                dados_extraidos.append({
                    "texto": texto,
                    "autor": autor,
                    "tags": tags_da_citacao 
                })
                print(f"Citação salva! (Autor: {autor}). Total salvo: {len(dados_extraidos)}")
                
                if len(dados_extraidos) >= max_citacoes:
                    print(f"--- ATINGIU O LIMITE DE {max_citacoes} CITAÇÕES ---")
                    break 
        
        if len(dados_extraidos) >= max_citacoes:
            break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
            url_atual = next_button.get_attribute('href')
            pagina_atual += 1
            
        except NoSuchElementException:
            print("\n--- Não há mais páginas. Fim da busca. ---")
            break 

    driver.quit()
    print("\nNavegador fechado.")
    return dados_extraidos
