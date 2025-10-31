<p align= "center">
  Aqui, busco explicar como os codigos <a href="TheCode/coletar_arquivos.py">coletar_arquivos.py</a> e <a href="TheCode/devolver_arquivos.py">devolver_arquivos.py</a> funcionam! <br>
</p>

<p align= "center">
  <img src="../assets/imagens/img1.png" width="500" alt="Interface do sistema"> </br>
</p>

<p align= "center">
  O codigo consiste em processar <b>UM ÚNICO</b> contrato de cada vez, executando as seguintes etapas para esse contrato:<br>
</p>

## 1. PREPARAÇÃO
- Recebe: núcleo e contrato
- Cria: código CADMUT (exemplo: 0011234567)

## 2. BUSCA DE DOCUMENTOS
- Vai em SGH → busca documento
- Vai em CADMUT → extrai informações
- Vai em CEDOC → busca documentos

## 3. ANÁLISE COM IA
- Usa GeminiAPI (Inteligência Artificial)
- Analisa os documentos encontrados

## 4. GERAÇÃO DE PDF
- Cria um recurso (texto automático)
- Gera um número de ofício
- Converte para PDF

## 5. VALIDAÇÃO
- Verifica se o PDF foi criado
- Anexa documentos ao PDF
- Valida se o recurso é reversível

## 6. RETORNA RESULTADOS
- True/False para cada etapa
