# MCP-Docs: Meu Co-piloto Pessoal para a Documentação do Django

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
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows: venv\Scripts\activate
    # No Linux/macOS: source venv/bin/activate
    ```

3.  **Instale as dependências** (é uma boa prática criar um `requirements.txt`):
    ```bash
    pip install django djangorestframework requests beautifulsoup4 sentence-transformers chromadb
    ```

4.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

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
