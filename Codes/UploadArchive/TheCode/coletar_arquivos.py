import os
import shutil
import fnmatch
from caminhos import pasta_raiz, padrao_arquivo, pasta_temp

def coletar_arquivos(pasta_raiz, padrao_arquivo, pasta_temp="temp_coletados"):
    #Cria a pasta temporária se não existir
    os.makedirs(pasta_temp, exist_ok=True)
    arquivos_encontrados = 0

    #Caminha por todas subpastas da pasta raiz
    for root, dirs, files in os.walk(pasta_raiz):
        for arquivo in files:
            if fnmatch.fnmatch(arquivo,padrao_arquivo):
                caminho_original = os.path.join(root,arquivo)
                caminho_relativo = os.path.relpath(root,pasta_raiz)
                destino_pasta = os.path.join(pasta_temp,caminho_relativo)
                os.makedirs(destino_pasta,exist_ok=True)
                shutil.move(caminho_original,destino_pasta)
                arquivos_encontrados += 1
                print(f"Arquivos movidos: {caminho_original} -> {destino_pasta}")

        if arquivos_encontrados == 0:
            print("Nenhum arquivo encontrado")
        else:
            print(f"\n Concluído! {arquivos_encontrados} arquivos movidos.")


#Executar
coletar_arquivos(pasta_raiz,padrao_arquivo, pasta_temp)
            
