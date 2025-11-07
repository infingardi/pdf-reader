# 📄 PDF Data Extractor — Enter AI Fellowship

Solução desenvolvida para o **Take Home Project** da **Enter AI Fellowship**, com o objetivo de **extrair informações estruturadas de PDFs** de forma rápida, precisa e com baixo custo.

---

## Objetivo

Criar um sistema que:
- Receba como entrada:  
  `label`, `extraction_schema` (em JSON) e um arquivo PDF.
- Retorne:  
  As informações extraídas no formato JSON.
- Atenda os requisitos:  
   Tempo de resposta < **10s**  
   Acurácia ≥ **80%**  
   Custo mínimo de execução  

---

## Estratégia da Solução

### Pipeline:
1. **Leitura do PDF**: extrai texto via `PyPDF`.
2. **Detecção de campos faltantes**.
3. **Chamada ao modelo `gpt-5-mini`** 
4. **Cache local (diskcache)** para evitar reprocessamento e reduzir custo.
5. **Resposta estruturada em JSON**.

---

## Configuração do Ambiente

### 1. Pré-requisitos
- Python 3.9+
- Git instalado
- Conta na OpenAI (com API key fornecida pelo desafio)

---

### 2. Clone o repositório

```bash
git clone git@github.com:infingardi/pdf-reader.git
cd pdf-reader
```

--- 

### 3. Rodando o projeto

1. Crie o arquivo `.env` na raiz do projeto e adicione sua chave da OpenAI:
   ```bash
   OPENAI_API_KEY=sk-sua-chave-aqui
   ```

2. Ative o ambiente virtual (Windows)
  ```bash
  ./setup_env.bat
```


## Configuração do Ambiente

1. Após iniciar o servidor, acesse o endereço:
  ```bash
  http://127.0.0.1:8000
```

2. Selecione a pasta que contém:
 - O arquivo dataset.json
 - Os arquivos .pdf correspondentes

3. O sistema irá:
  - Processar cada PDF conforme o schema definido no dataset.json
  - Exibir os resultados em tempo real com o progresso e tempo de execução por arquivo
  - Retornar as informações extraídas no formato JSON estruturado
