import os
import shutil
import fnmatch
from caminhos import pasta_raiz, padrao_arquivo, pasta_temp

def coletar_arquivos(pasta_raiz, padrao_arquivo, pasta_temp):
    #Cria a pasta temporária se não existir
    os.makedirs(pasta_temp, exist_ok=True)
    arquivos_encontrados = 0

    #Caminha por todas subpastas da pasta raiz
    for root, dirs, files in os.walk(pasta_raiz): #root é a pasta atual, dirs são as subpastas e files são os arquivos dentro dela. O os.walk percorre a pasta que eu escolher!
        for arquivo in files: #arquivos são todos os arquivos na pasta atual, files é uma lista de strings com os nomes dos arquivos
            if fnmatch.fnmatch(arquivo,padrao_arquivo): #aqui verifico se o arquivo é do padrão que eu quero: pdf.
                caminho_original = os.path.join(root,arquivo) # os.path.join junta as pastas em uma string com o separador correto para cada sistema operacional
                caminho_relativo = os.path.relpath(root,pasta_raiz) #os.path.relpath retorna o caminho relativo
                destino_pasta = os.path.join(pasta_temp,caminho_relativo)
                os.makedirs(destino_pasta,exist_ok=True) #cria a pasta temporária de destino caso ela ainda não exista
                shutil.move(caminho_original,destino_pasta) #move o arquivo para a pasta temporária de destino
                arquivos_encontrados += 1
                print(f"Arquivos movidos: {caminho_original} -> {destino_pasta}")

        if arquivos_encontrados == 0:
            print("Nenhum arquivo encontrado")
        else:
            print(f"\n Concluído! {arquivos_encontrados} arquivos movidos.")


#Executar
coletar_arquivos(pasta_raiz,padrao_arquivo, pasta_temp)
            
