# Códigos em Python de Pedro / Pedro's Python Code

![GitHub repo size](https://img.shields.io/github/repo-size/iuricode/README-template?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/iuricode/README-template?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/iuricode/README-template?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/iuricode/README-template?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/iuricode/README-template?style=for-the-badge)

<p align="center">
<img src="/assets/imagens/Python.png" width="500" alt="Python">
</p>

<details>
<summary>🇧🇷 Português</summary>

> Aqui, adicionarei meus códigos em Python que estarei criando ao longo do tempo.

## 💻 Pré-requisitos

Antes de começar, verifique se você atende aos seguintes requisitos:

- Você possui a versão mais recente do `<python/pip>`;
- Você tem instaladas as bibliotecas `<os, playwright, selenium, numpy, pandas, requests, BeautifulSoup, sys, shutil, fnmatch, jinja2>`;
- Você está utilizando uma máquina com `<Windows / Linux / Mac>`;
- Antes de usar os códigos, consulte os guias disponíveis no `Readme.md` dentro de cada pasta de cada codigo.

## 🧩 Projetos <br>
> [!NOTE]
> Os códigos estão salvos em: [**Codes**](./Codes/)

> [!TIP]
> Para acessar qualquer código, basta clicar no link correspondente abaixo:

[**UploadArchive**](./Codes/UploadArchive/)
<details>
<summary>Detalhes sobre o código</summary>
<br>
Neste projeto, o código [**coletar_arquivos.py**](./Codes/UploadArchive/TheCode/coletar_arquivos.py/) acessa pastas e subpastas do local definido por você.  
Nas subpastas, o código procura por um arquivo específico (pelo nome ou extensão) que o usuário define em [**caminhos.py**](./Codes/UploadArchive/TheCode/caminhos.py/).  
Em seguida, o programa move o arquivo para uma pasta também definida em [**caminhos.py**](./Codes/UploadArchive/TheCode/caminhos.py/).

Em outras palavras:

`Pasta X -> Subpasta X -> Arquivo X -> Pasta_Final`

Para realizar o processo inverso:

`Pasta_Final -> Arquivo X -> Pasta X -> Subpasta X`

Basta usar: [**devolver_arquivos.py**](./Codes/UploadArchive/TheCode/devolver_arquivos.py/)
</details>

[**Web-Scrapper**](./Codes/Web-Scrapper/)
<details>
<summary>Detalhes sobre o código</summary>
<br>
Neste projeto, criei um sistema simples de Web Scraping utilizando 3 arquivos principais:
[**extrator_web.py**](./Codes/Web-Scrapper/TheCodes/extrator_web.py/)  
[**gerador_pdf.py**](./Codes/Web-Scrapper/TheCodes/gerador_pdf.py/)  
[**main.py**](./Codes/Web-Scrapper/TheCodes/main.py/)

O programa acessa o site [quotes.toscrape.com](https://quotes.toscrape.com/) e extrai citações sobre um autor ou uma tag especificada pelo usuário no console.  
As informações são retornadas em um PDF formatado via HTML e CSS, utilizando os arquivos:  
[**template.html**](./Codes/Web-Scrapper/TheCodes/template.html/)  
[**styles.css**](./Codes/Web-Scrapper/TheCodes/styles.css/)
</details>

## 🤝 Colaborador

> Se quiser saber mais sobre o criador desses projetos, acesse o perfil dele no GitHub:

<table align="center">
  <tr>
    <td>
      <a href="https://github.com/PedroX-dev" title="Pedro">
        <img src="/assets/imagens/pedro.jpg" width="500" alt="Pedro"><br>
        <p align="center">
          <b>Pedro Henrique dos Santos Souza Lopes</b>
        </p>
      </a>
    </td>
  </tr>
</table>

## 😄 Torne-se um dos contribuidores

Quer fazer parte deste projeto?  
Clique [AQUI](CONTRIBUTING.md) e veja como contribuir.

## 📝 Licença

Este projeto possui licença.  
Consulte o arquivo [LICENSE](LICENSE.md) para mais detalhes.

</details>

<details>
<summary>🇺🇸 English</summary>

> Here, I will add my Python code that I'm creating over time.

## 💻 Prerequisites

Before you start, please check that you meet the following requirements:

- You have the most recent version of `<python/pip>`;
- You have the libraries installed `<os, playwright, selenium, numpy, pandas, requests, BeautifulSoup, sys, shutil, fnmatch, jinja2>`;
- You have a machine with `<Windows / Linux / Mac>`;
- Before using the codes, see the guides to help you `<guide / link / project_related_documentation>`.

## 🧩 Projects

> [!NOTE]
> The codes are saved in: [**Codes**](./Codes/)

> [!TIP]
> To access any code, simply click on the corresponding link below:

[**UploadArchive**](./Codes/UploadArchive/)
<details>
<summary>Details about the code</summary>
<br>
In this project, the code [**coletar_arquivos.py**](./Codes/UploadArchive/TheCode/coletar_arquivos.py/) accesses folders and subfolders from the location you defined.  
In the subfolders, the code will search for a specific file (by name or extension) that the user needs to define in [**caminhos.py**](./Codes/UploadArchive/TheCode/caminhos.py/).  
Then, the program will move the file to a folder also defined in [**caminhos.py**](./Codes/UploadArchive/TheCode/caminhos.py/).

In other words:

`Folder X -> SubFolder X -> Archive X -> Final_Folder`

To do the reverse process:

`Final_Folder -> Archive X -> Folder X -> SubFolder X`

You just need to use: [**devolver_arquivos.py**](./Codes/UploadArchive/TheCode/devolver_arquivos.py/)
</details>

[**Web-Scrapper**](./Codes/Web-Scrapper/)
<details>
<summary>Details about the code</summary>
<br>
In this project, I created a simple Web Scraping system using 3 main files:
[**extrator_web.py**](./Codes/Web-Scrapper/TheCodes/extrator_web.py/)  
[**gerador_pdf.py**](./Codes/Web-Scrapper/TheCodes/gerador_pdf.py/)  
[**main.py**](./Codes/Web-Scrapper/TheCodes/main.py/)

The program accesses [quotes.toscrape.com](https://quotes.toscrape.com/) and extracts quotes about an author or tag specified by the user in the console.  
The information is returned in a PDF formatted via HTML and CSS using the files:  
[**template.html**](./Codes/Web-Scrapper/TheCodes/template.html/)  
[**styles.css**](./Codes/Web-Scrapper/TheCodes/styles.css/)
</details>

## 🤝 Collaborator

> If you'd like to learn more about the creator of these projects, here's a link to their GitHub profile:

<table align="center">
  <tr>
    <td>
      <a href="https://github.com/PedroX-dev" title="Pedro">
        <img src="/assets/imagens/pedro.jpg" width="500" alt="Pedro"><br>
        <p align="center">
          <b>Pedro Henrique dos Santos Souza Lopes</b>
        </p>
      </a>
    </td>
  </tr>
</table>

## 😄 Become a contributor

Want to be a part of this project? Click [HERE](CONTRIBUTING.md) and read how to contribute.

## 📝 License

This project is licensed. See the [LICENSE](LICENSE.md) file for more details.

</details>
