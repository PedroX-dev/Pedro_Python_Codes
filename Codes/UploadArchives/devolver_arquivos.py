import os
import shutil
from caminhos import pasta_raiz, pasta_temp



def devolver_arquivos(pasta_temp, pasta_raiz):
    arquivos_encontrados = 0
    for root, dirs, files in os.walk(pasta_temp):
        for arquivo in files:
            #Caminho do arquivo temporário
            caminho_temp = os.path.join(root, arquivo)
            # Recupera o caminho relativo
            caminho_relativo = os.path.relpath(root, pasta_temp)
            #Monta o caminho original do destino na pasta raiz
            destino_original = os.path.join(pasta_raiz, caminho_relativo)
            os.makedirs(destino_original, exist_ok=True)
            shutil.move(caminho_temp, destino_original)
            arquivos_encontrados += 1
            print(f"Arquivos movidos: {caminho_temp} -> {destino_original}")

    if arquivos_encontrados == 0:
        print("Nenhum arquivo encontrado")
    else:
        print(f"\n Concluído! {arquivos_encontrados} arquivos movidos.")

#Executar
devolver_arquivos(pasta_temp, pasta_raiz)
