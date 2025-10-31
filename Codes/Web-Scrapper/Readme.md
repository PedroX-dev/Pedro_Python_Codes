<p align= "center">
  Aqui, busco explicar como os codigos referentes ao <a href="TheCodes">Sistema de Web-Scrapper</a> funciona! <br>
</p>

<p align= "center">
  <img src="../assets/imagens/img1.png" width="500" alt="Interface do sistema"> </br>
</p>

<p align= "center">
  O codigo consiste em extrair citações sobre autores de uma página web, e devolver essas citações formatadas para o usuário<br>
</p>

## 1. Formatação do PDF, Parte 1
- Os aquivos <a href= "TheCodes/template.html">template.html</a> e <a href= "TheCodes/styles.css">styles.css</a>, são responsáveis pela formatação do PDF de saída dos seus dados extraídos; portanto, peronalize-os da forma que quiser.
## 1. Formatação do PDF, Parte 2
- O codigo <a href= "TheCodes/gerador_pdf.py">gerador_pdf.py</a> é responsável pela geração do PDF após o processo de extração de dados.
- Utilizamos as bibliotecas `jinja2` para criar páginas HTML e `xhtml2pdf` para passar o html para pdf.
- Caso mude algo nos aquivos <a href= "TheCodes/template.html">template.html</a> e <a href= "TheCodes/styles.css">styles.css</a>, atente-se para mudar também em <a href= "TheCodes/gerador_pdf.py">gerador_pdf.py</a>; caso não tenha mudado nada, apenas deixe os códigos juntos.
## 3. Extraindo os dados da Web
- Para retornar os arquivos a pasta original, deve-se agora rodar o código `devolver_arquivos.py`.
- Após a conclusão do processo, o número de arquivos movidos irá aparecer no console, e os códigos serão movidos da página final, para a pasta original.
## 4. Conclusão
<p align = "center">
  O objetivo desse código, é automatizar a separação e movimentação de arquivos, um processo o qual, em altos números de arquivos, pode ser demorado e complexo.
  Dessa forma, adapte o código da forma que achar melhor, para atender suas demandas.
</p>
