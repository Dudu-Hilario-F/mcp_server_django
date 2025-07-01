# MCP-Docs: Meu Co-piloto Pessoal para a Documentação do Django

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
    ```

2.  **Crie e ative um ambiente virtual:**
```bash

  # Cria o ambiente
  python -m venv mcp-env

  # Ativa o ambiente
  # Windows
  mcp-env\Scripts\activate
  # macOS/Linux
  source mcp-env/bin/activate
```

3.  **Instale as dependências** (é uma boa prática criar um `requirements.txt`):
    ```bash
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
    ```bash
    python manage.py migrate
    ```

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