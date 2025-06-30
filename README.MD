# MCP-Docs: Meu Co-piloto Pessoal para a Documentação do Django

<<<<<<< HEAD
Este é o repositório do **MCP-Docs**, um projeto que nasceu de uma necessidade pessoal e se tornou um campo de estudos sobre busca semântica e a integração de ferramentas com Grandes Modelos de Linguagem (LLMs) como o Gemini.

O projeto está em desenvolvimento contínuo, e este documento reflete minha jornada de aprendizado, os desafios encontrados e os próximos passos que pretendo dar.

## O Problema que me Propus a Resolver

Como desenvolvedor que utiliza Django, eu passava um tempo considerável navegando pela documentação oficial. O uso do `Ctrl+F` era funcional, mas limitado: ele busca por palavras exatas, não pelo *problema* ou *conceito* que eu queria entender. Isso me levava a pular de página em página em busca de um contexto que nem sempre era fácil de encontrar.

A minha meta era criar uma ferramenta que me permitisse "conversar" com a documentação, fazendo perguntas em linguagem natural e recebendo respostas diretas, precisas e contextualizadas.

## A Solução: Busca Semântica com RAG (Retrieval-Augmented Generation)

Para resolver o problema, decidi construir um servidor intermediário que funciona como um assistente especializado para uma IA. Este servidor lê, processa e armazena o conhecimento da documentação do Django, disponibilizando-o através de uma API.

A grande virada técnica do projeto é não depender apenas do conhecimento pré-treinado da IA, mas "aumentar" sua capacidade com informações específicas e atualizadas.

### A Limitação da IA sem o MCP-Docs: Busca Literal vs. Conhecimento Estático

Uma IA como o Gemini, por si só, possui um conhecimento vasto, mas "congelado no tempo" até a data do seu último treinamento.

* **Pesquisa sem MCP-Docs (Conhecimento Geral):** Se eu perguntar sobre uma funcionalidade do Django 5.2, a IA pode fornecer uma resposta baseada no Django 4.0, se essa for a versão mais proeminente em seus dados de treino. Pior, ela pode tentar "adivinhar" uma resposta, resultando em uma "alucinação" – uma informação incorreta que pode custar horas de depuração.

### O Poder da IA com o MCP-Docs: Busca Semântica e Conhecimento Dinâmico

O MCP-Docs implementa o padrão **RAG (Retrieval-Augmented Generation)**, transformando a IA de um "sábio com memória antiga" para um "pesquisador com acesso a uma biblioteca atualizada".

* **Pesquisa com MCP-Docs (Geração Aumentada por Recuperação):**
    1.  **Recuperação (Retrieval):** Ao receber uma pergunta, a IA primeiro consulta a API do MCP-Docs.
    2.  **Busca Semântica:** O MCP-Docs transforma a pergunta em um vetor e busca em sua base de dados (ChromaDB) os trechos da documentação que são semanticamente mais similares, ou seja, que correspondem ao *significado* da pergunta.
    3.  **Geração (Generation):** A IA recebe esses trechos de texto atualizados e confiáveis e os utiliza como base para formular uma resposta coesa, precisa e em linguagem natural.

O MCP-Docs não concorre com a IA; ele a potencializa, fornecendo a matéria-prima correta para que ela possa gerar a resposta perfeita.

### Porque Vetores e Não Texto Puro?

No coração da busca semântica estão os **embeddings de vetores**. Quando o texto da documentação é processado, ele é transformado de palavras para vetores — representações matemáticas que capturam o significado e o contexto.

* **Busca por Texto Puro:** Compara `string` com `string`. `ForeignKey` só encontra `ForeignKey`.
* **Busca por Vetores:** Compara significado com significado. Uma busca por "como conectar dois modelos" pode encontrar resultados sobre `ForeignKey`, `OneToOneField` e `ManyToManyField`, pois os vetores dessas palavras estão matematicamente próximos no "espaço de significado".

## Arquitetura e Tecnologias Utilizadas

* **Django e Django REST Framework (DRF):** Utilizados para construir o servidor, a estrutura do banco de dados relacional e a API que expõe os dados.
* **Requests & BeautifulSoup4:** Ferramentas para realizar o web scraping da documentação oficial do Django e extrair o conteúdo textual das páginas HTML.
* **Sentence-Transformers:** Biblioteca fundamental que transforma os trechos de texto em embeddings de vetores, permitindo a busca semântica.
* **ChromaDB:** Banco de dados vetorial onde os embeddings são armazenados e indexados, permitindo buscas por similaridade de forma extremamente eficiente.

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Dudu-Hilario-F/mcp_server_django.git](https://github.com/Dudu-Hilario-F/mcp_server_django.git)
    cd mcp_server_django
=======
Bem-vindo ao repositório do **MCP-Docs**, um sistema de busca inteligente para a documentação do Django, projetado para ser consumido por assistentes de IA como o Gemini.

A ideia nasceu de uma necessidade comum: a busca por soluções na documentação oficial, que muitas vezes se torna uma caça manual e demorada com `Ctrl+F`. O MCP-Docs resolve isso implementando uma busca semântica, que entende o *problema* por trás da pergunta, em vez de apenas palavras-chave exatas.

O objetivo é transformar a maneira como interagimos com a documentação, fornecendo respostas contextuais e diretas, e servindo como um caso de teste para a integração de ferramentas de IA no fluxo de trabalho de desenvolvimento.

## 🤔 A Arquitetura: Geração Aumentada por Recuperação (RAG)

O MCP-Docs não é apenas um motor de busca; ele é uma implementação do padrão **RAG (Retrieval-Augmented Generation)**. Em vez de depender do conhecimento potencialmente desatualizado de um modelo de linguagem, nós o "aumentamos" com informações precisas e atuais.

**O Problema:** Um LLM (Modelo de Linguagem Grande) como o Gemini possui um conhecimento vasto, mas congelado no tempo do seu último treinamento. Ele pode não conhecer as funcionalidades da versão mais recente do Django ou, pior, "alucinar" uma resposta incorreta, causando erros e perda de tempo.

**A Solução RAG:**
1.  **Recuperação (Retrieval):** Quando uma pergunta sobre o Django é feita, em vez de adivinhar, a IA usa a API do MCP-Docs. Nosso sistema busca em uma base de dados vetorial (ChromaDB), que contém a documentação oficial previamente processada, e recupera os trechos mais relevantes para a pergunta.
2.  **Geração Aumentada (Augmented Generation):** Com esses trechos de informação confiável e atualizada em mãos, a IA gera uma resposta coesa, precisa e contextualizada.

O MCP-Docs atua como um assistente de pesquisa especializado, fornecendo os fatos, enquanto a IA usa sua inteligência para interpretá-los e apresentá-los de forma clara. É a colaboração perfeita entre uma base de conhecimento especializada e um raciocínio avançado.

## 🚀 Guia de Instalação e Execução

Para executar o projeto localmente, siga os passos abaixo.

### 1. Pré-requisitos
- Python 3.10+
- Git

### 2. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd mcp-project
>>>>>>> 12b5bf7 (Fazendo melhorias no projeto: (fazendo testes, criando arquivos de logs, .env e melhorando o readme))
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
<<<<<<< HEAD
    python -m venv venv
    # No Windows: venv\Scripts\activate
    # No Linux/macOS: source venv/bin/activate
=======
    # Cria o ambiente
    python -m venv mcp-env

    # Ativa o ambiente
    # Windows
    mcp-env\Scripts\activate
    # macOS/Linux
    source mcp-env/bin/activate
>>>>>>> 12b5bf7 (Fazendo melhorias no projeto: (fazendo testes, criando arquivos de logs, .env e melhorando o readme))
    ```

3.  **Instale as dependências** (é uma boa prática criar um `requirements.txt`):
    ```bash
<<<<<<< HEAD
    pip install django djangorestframework requests beautifulsoup4 sentence-transformers chromadb
    ```

4.  **Aplique as migrações do banco de dados:**
=======
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie uma cópia do arquivo `.env.example` e renomeie para `.env`. Este arquivo guardará suas configurações locais.
    ```bash
    # No Windows (usando copy) ou Linux/macOS (usando cp)
    copy .env.example .env
    ```
    *O arquivo `.env` já vem com valores padrão para desenvolvimento. A `SECRET_KEY` é gerada automaticamente se não existir.*

5.  **Prepare o banco de dados:**
>>>>>>> 12b5bf7 (Fazendo melhorias no projeto: (fazendo testes, criando arquivos de logs, .env e melhorando o readme))
    ```bash
    python manage.py migrate
    ```

<<<<<<< HEAD
5.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    A API estará acessível em `http://127.0.0.1:8000/api/v1/search/`.

## Populando a Base de Conhecimento

Para que a busca funcione, é preciso alimentar o banco de dados com a documentação do Django. Criei um comando customizado para isso.

O script é inteligente: ele utiliza `update_or_create` (no Django) e `upsert` (no ChromaDB) para evitar duplicatas e permitir a atualização de documentos já existentes.

* **Para popular com uma página específica:**
    ```bash
    # Exemplo: python manage.py import_docs <VERSÃO> <CAMINHO_DA_PÁGINA>
    python manage.py import_docs 5.2 topics/db/models/
    ```

* **Para uma atualização completa (ex: nova versão do Django):**
    A abordagem mais segura é limpar a base de dados antiga (apagar `db.sqlite3` e a pasta `chroma_db/`), rodar o `migrate` novamente e, então, re-popular tudo do zero com os novos comandos.

## Roadmap de Melhorias Futuras

Este projeto é um campo de aprendizado. As próximas melhorias que pretendo estudar e implementar são:

- [ ] **Containerização com Docker:** Criar um ambiente com `docker-compose` para encapsular a aplicação Django e o banco de dados PostgreSQL, facilitando a configuração e o deploy.
- [ ] **Aprimoramento do Parsing:** Substituir a extração de texto puro com `BeautifulSoup4` por uma conversão de **HTML para Markdown**. Isso preservará a estrutura semântica do documento (títulos, listas, tabelas, blocos de código), o que deve enriquecer a qualidade dos embeddings.
- [ ] **Mecanismo de Atualização em Massa:** Desenvolver um script que possa monitorar o sitemap da documentação do Django e disparar atualizações automáticas no banco de dados quando detectar mudanças.
- [ ] **Evolução da API:** Adicionar mais funcionalidades à API, como filtros por versão do Django, paginação e a possibilidade de retornar metadados mais ricos sobre os documentos.
- [ ] **Otimização do Banco de Dados Relacional:** Adicionar **índices** em campos-chave do modelo `DocumentChunk`, como nos títulos e URLs, para acelerar as consultas e filtros no banco de dados PostgreSQL.

## Desafios e Aprendizados

* **Instabilidade do Scraper:** O seletor de CSS que eu usava para encontrar o conteúdo principal parou de funcionar após uma mudança no site do Django. **Aprendizado:** A importância de salvar o HTML localmente para depurar o scraper e a necessidade de construir seletores mais resilientes.
* **Cache de Bytecode (`__pycache__`):** Perdi um tempo considerável depurando um erro que não existia mais no código. **Aprendizado:** O Python pode rodar versões antigas de scripts em cache. Limpar as pastas `__pycache__` e reiniciar o terminal se tornou um passo padrão na solução de problemas "fantasmas".
* **Boas Práticas de Scraping:** Meu script foi inicialmente bloqueado. **Aprendizado:** A necessidade de "ser educado" com os servidores, adicionando um `User-Agent` ao cabeçalho da requisição para simular um navegador real.
=======
### 3. Alimentando a Base de Conhecimento

Para popular o banco de dados com a documentação do Django, use o comando `import_docs`.

```bash
# Exemplo: Importar a documentação sobre Models da versão 5.2 do Django
python manage.py import_docs 5.2 topics/db/models/
```

O script irá:
- Fazer o download da página.
- Dividir o conteúdo em seções lógicas.
- Salvar o texto no banco de dados relacional (SQLite).
- Gerar embeddings (vetores de significado) para cada seção.
- Salvar os embeddings no banco de dados vetorial (ChromaDB).

O progresso e possíveis erros são registrados no arquivo `import_docs.log`.

### 4. Iniciando o Servidor

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/v1/search/`.

### 5. Executando os Testes

Para garantir que tudo está funcionando como esperado, rode a suíte de testes:
```bash
python manage.py test
```

## 🛠️ Boas Práticas e Próximos Passos

Este projeto segue boas práticas de desenvolvimento para garantir qualidade e manutenibilidade.

-   **Gerenciamento de Dependências:** O arquivo `requirements.txt` garante que todos os desenvolvedores usem as mesmas versões das bibliotecas, evitando o "funciona na minha máquina".
-   **Configuração Segura:** O uso de variáveis de ambiente (`.env`) separa as configurações sensíveis (como `SECRET_KEY`) do código, uma prática de segurança essencial.
-   **Logging:** O comando de importação (`import_docs`) gera logs detalhados no arquivo `import_docs.log`, facilitando a depuração e o monitoramento.
-   **Testes Automatizados:** Testes unitários para a API (`apps/documentation/tests.py`) garantem que o endpoint principal funcione corretamente e evitam regressões.

### Próximos Passos Sugeridos

-   **Automação de Atualização:** Criar um novo comando que utilize o `sitemap.xml` da documentação do Django para descobrir e importar páginas novas ou atualizadas automaticamente.
-   **Containerização com Docker:** Criar um `Dockerfile` e um `docker-compose.yml` para simplificar o setup do ambiente de desenvolvimento e preparar o projeto para produção.
-   **CI/CD (Integração Contínua):** Configurar um workflow com GitHub Actions para rodar testes e linters automaticamente a cada push, garantindo a qualidade do código.

## 🔌 Integração com uma IA (Ex: Gemini)

A API foi projetada para ser usada como uma **ferramenta** por um LLM. No seu cliente de IA, você deve registrar a seguinte ferramenta:

```json
{
  "name": "search_django_docs",
  "description": "Busca na documentação oficial do Django por trechos de texto que respondam a uma pergunta ou descrevam um conceito técnico.",
  "parameters": {
    "type": "object",
    "properties": {
      "q": {
        "type": "string",
        "description": "A pergunta do usuário ou o conceito a ser pesquisado. Deve ser uma frase completa para uma busca semântica eficaz."
      }
    },
    "required": ["q"]
  }
}
```

Com a ferramenta registrada, o fluxo é o seguinte:
1.  O usuário faz uma pergunta técnica sobre Django.
2.  A IA identifica que a ferramenta `search_django_docs` é a mais adequada para responder.
3.  A IA chama a API do MCP-Docs com a pergunta do usuário.
4.  O MCP-Docs retorna os trechos mais relevantes da documentação.
5.  A IA utiliza esses trechos para formular uma resposta final, precisa e baseada em fatos.
>>>>>>> 12b5bf7 (Fazendo melhorias no projeto: (fazendo testes, criando arquivos de logs, .env e melhorando o readme))
