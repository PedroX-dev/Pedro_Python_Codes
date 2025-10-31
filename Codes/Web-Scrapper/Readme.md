<p align= "center">
  Aqui, busco explicar como os codigos referentes ao <a href="TheCodes">Sistema de Web-Scrapper</a> funciona! <br>
</p>

<p align= "center">
  <img src="../assets/imagens/img1.png" width="500" alt="Interface do sistema"> </br>
</p>

<p align= "center">
  O codigo consiste em processar <b>UM ÚNICO</b> contrato de cada vez, executando as seguintes etapas para esse contrato:<br>
</p>

## 1. Definindo Valores
- Deve-se utilizar o codigo `caminhos.py`, para definir os locais da sua pasta raiz, pasta temporaria, e o tipo de arquivo que deseja buscar na sua máquina.
## 2. Rodando o Código, Parte 1
- Rode o código `coletar_arquivos.py` em sua IDE de preferência.
- Após o processo ser concluido, irá aparecer no console o local o qual foram extraidos os arquivos; o local de destino dos arquivos; e o número de arquivos movidos.
## 3. Rodando o Código, Parte 2
- Para retornar os arquivos a pasta original, deve-se agora rodar o código `devolver_arquivos.py`.
- Após a conclusão do processo, o número de arquivos movidos irá aparecer no console, e os códigos serão movidos da página final, para a pasta original.
## 4. Conclusão
<p align = "center">
  O objetivo desse código, é automatizar a separação e movimentação de arquivos, um processo o qual, em altos números de arquivos, pode ser demorado e complexo.
  Dessa forma, adapte o código da forma que achar melhor, para atender suas demandas.
</p>
