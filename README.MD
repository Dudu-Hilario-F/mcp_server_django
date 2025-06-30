# Projeto MCP-Docs: Meu Co-piloto Pessoal para a Documentação do Django

Repositório do MCP-Docs.

A ideia nasceu de uma necessidade minha. Eu sempre acabava perdendo um tempão com `Ctrl+F` na documentação do Django, pulando de página em página. 
Pensei: "e se eu pudesse ter uma busca mais inteligente, que entendesse o *problema* que eu quero resolver, em vez de só as palavras exatas que eu digito? e trazer uma solução profissional baseado no manual do problema".

Foi assim que decidi criar o **MCP-Docs**, um servidor que estuda a documentação do Django e a deixa prontinha para ser consultada por qualquer IA que esta utilizando no momento. 
A meta é ter um co-piloto que me dê respostas diretas e contextuais sobre a documentação que me ajude a resolver um determinado problema e testar o novo produto do google `Gemeni CLI`.

## 🤔 A Ideia: Por que esse projeto existe?

O objetivo que tracei foi simples: criar um sistema que:
1.  Lesse a documentação oficial do Django por conta própria.
2.  Guardasse esse conhecimento de uma forma "inteligente", com contexto.
3.  Disponibilizasse uma API para que um cliente de IA pudesse fazer perguntas e me dar as respostas.

A missão: aposentar o `Ctrl+F` e buscar por **significado** na internet e foruns e me dar uma resposta mais precisa para melhorar minha produtividade na linguagem em que o projeto esta sendo desenvolvido.

### 🧐 Mas... a IA não podia fazer tudo isso sozinha?

Uma dúvida gigante que você pode esta pensando agora: 
`"Se o Gemini é tão inteligente, por que eu preciso construir todo esse sistema? Ele não poderia simplesmente ir ao site do Django e encontrar as respostas sozinho?".`

A resposta é **não**, e entender o porquê é entender o motivo pelo qual o MCP-Docs é tão útil.

Pensei nisso da seguinte forma: a IA é como um professor universitário genial, que leu uma biblioteca inteira de livros até o dia em que se formou. Ele sabe MUITO, mas sobre o que ele estudou **até aquela data**.

* **Conhecimento Geral (O Professor Genial):** A "memória" da IA é baseada no seu treinamento. Ela pode me dar ótimas respostas sobre o Django 4.0, por exemplo. Mas se eu perguntar sobre uma nova funcionalidade do Django 5.2, ou uma que mudou recentemente, a memória dele pode estar desatualizada. Pior, ele pode tentar "adivinhar" a resposta e me passar uma informação incorreta (o que o pessoal chama de "alucinação"), e em programação, um detalhe errado pode custar horas de dor de cabeça.

* **Ferramenta Específica (Meu Servidor MCP-Docs):** O meu servidor é como um **assistente de laboratório especializado**. O professor genial (a IA) não vai até a biblioteca procurar os artigos mais recentes. Ele vira para o assistente e diz: "Vá até a prateleira da 'Documentação do Django 5.2' e me traga o texto exato sobre `OneToOneField`".

O meu servidor MCP-Docs é esse assistente. Ele não tem a inteligência do professor para conversar, mas ele tem uma única tarefa que faz perfeitamente: ir até a **minha base de dados, que eu mantenho atualizada**, e trazer a informação crua, factual e correta.

#### A Parceria Perfeita: RAG (Retrieval-Augmented Generation) Geração Aumentada por Recuperação.

1.  **Recuperação (Retrieval):** A IA, ao invés de adivinhar, usa minha ferramenta (o MCP-Docs) para **recuperar** a informação precisa e atualizada.
2.  **Geração Aumentada (Augmented Generation):** Com essa informação confiável em mãos, a IA usa sua genialidade para **aumentar** a qualidade da sua resposta. Ela não apenas me joga o texto da documentação, mas o interpreta, resume e me explica no contexto da minha pergunta original.

Então, o MCP-Docs não é um concorrente da IA; ele é o melhor amigo dela. Ele entrega a informação fresca e confiável, e a IA usa seu poder de raciocínio para transformar essa informação em uma resposta perfeita. É a melhor colaboração possível!


## 🌱 Mantendo o Conhecimento Fresco: Como Atualizar a Base de Dados

Beleza, o MCP-Docs está funcionando e a busca semântica é incrível. Mas aí bateu outra dúvida: o Django lança uma nova versão, ou uma página da documentação é corrigida. Como eu garanto que o meu co-piloto não fique "congelado no tempo" com informação velha?

A resposta é que eu preciso de um processo para **re-popular** e **atualizar** o banco de dados. Existem duas abordagens pra isso: a manual (que já funciona) e a automática (o plano pro futuro).

### Como a "Mágica" da Atualização Funciona

Antes de mais nada, uma coisa que eu já tinha preparado no código é que o script de importação é **inteligente para lidar com atualizações**.

* No banco de dados do Django, eu usei o comando `update_or_create()`. Isso significa: "Se o `source_url` deste chunk de documento já existe, **atualize** o conteúdo. Se não existe, **crie** um novo."
* No ChromaDB, eu usei o comando `upsert()`. Ele faz exatamente a mesma coisa: se o ID do chunk já existe, o vetor de embedding é atualizado; senão, um novo é inserido.

Esses dois comandos são os heróis silenciosos aqui, pois eles garantem que eu não crie conteúdo duplicado e que as informações sejam sempre substituídas pelas mais recentes.

### Abordagem 1: A Atualização Manual (O Jeito Simples e Direto)

Este é o método que eu posso usar agora mesmo, sempre que eu notar uma mudança importante ou quiser adicionar mais conhecimento.

1.  **Encontre a Página:** Primeiro, eu encontro a URL da página da documentação do Django que foi atualizada ou que eu quero adicionar.
2.  **Rode o Comando:** Eu simplesmente executo o comando `import_docs`, apontando para essa página.

    ```bash
    # Exemplo: A documentação sobre "Formsets" foi atualizada na versão 5.2
    python manage.py import_docs 5.2 topics/forms/formsets/
    ```

O script vai fazer todo o trabalho pesado. Ele vai ler a página, e o `update_or_create` / `upsert` vão garantir que os chunks sejam atualizados ou criados no banco de dados, sem bagunça.

> **Dica de Mestre:** Para uma atualização massiva (como o lançamento do Django 6.0), a abordagem mais segura seria apagar o banco de dados antigo (`db.sqlite3`) e a pasta `chroma_db/`, rodar o `migrate` de novo, e então re-popular tudo do zero com a nova versão. Isso garante uma base de conhecimento 100% limpa e consistente.

### Abordagem 2: A Atualização Automática (O Próximo Nível)

Ainda estudando.

...

## 🛠️ Ferramentas: O que eu usei no projeto

Para tirar essa ideia do papel, precisei aprender e usar algumas ferramentas. Cada uma foi uma peça chave no quebra-cabeça:

* **Django**: Foi a base de tudo, o "chassi" do meu projeto. Usei pra criar o servidor, o banco de dados principal e organizar a estrutura.
* **Django REST Framework (DRF)**: O kit de ferramentas que me ajudou a construir a "ponte" (a API) entre meu servidor e o mundo. Sem ele, criar a API teria sido bem mais complicado.
* **Requests**: A ferramenta que meu "robô" usou pra ir até o site do Django e baixar o conteúdo das páginas. Simples e eficaz.
* **BeautifulSoup4**: Depois que o `requests` trazia o HTML, o BeautifulSoup foi meu detetive particular, analisando a "sopa" de tags e me ajudando a extrair só o texto que importava.
* **Sentence-Transformers**: A "varinha mágica" do projeto. Essa biblioteca pegou o texto puro que extraí e o transformou em "embeddings" – basicamente, matemática que representa o significado do texto. É aqui que a IA do projeto começou a tomar forma.
* **ChromaDB**: Se os embeddings são o conhecimento, o ChromaDB foi a "estante de livros mágica". Ele organiza os textos por similaridade de significado, o que permite buscas por contexto de forma super rápida.

## 🚀 Como Colocar pra Rodar: Guia de Instalação

Quer testar o projeto aí? É só seguir esses passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative seu ambiente virtual:**
    ```bash
    python -m venv mcp-env
    # No Windows: mcp-env\Scripts\activate
    # No macOS/Linux: source mcp-env/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    # (Seria necessário criar um requirements.txt com as libs acima)
    pip install django djangorestframework requests beautifulsoup4 sentence-transformers chromadb
    ```

4.  **Prepare o banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Alimente a base de conhecimento:** Rode o scraper para ler a documentação e criar os embeddings.
    ```bash
    # Rode para quantas páginas da documentação você quiser!
    python manage.py import_docs 5.2 topics/db/models/
    ```

6.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

## 🗺️ Minha Jornada: O Diário de Bordo do Projeto

O projeto foi uma escada, degrau por degrau.

#### Etapa 1: O Esqueleto (Setup do Django)
Aqui foi onde tudo começou. A parte de planejamento, definindo a estrutura de pastas e o primeiro modelo no `models.py`, o `DocumentChunk`. Foi o molde para cada pedaço de conhecimento que eu ia guardar.

#### Etapa 2: O Caçador de Conhecimento (Web Scraper)
Essa foi a hora de botar a mão na massa. Criei um comando Django (`import_docs`) que usava `requests` e `BeautifulSoup` para caçar o conteúdo na documentação. O desafio foi ensinar o script a se comportar como um detetive: achar o conteúdo principal, quebrá-lo em seções lógicas e salvar no banco de dados.

#### Etapa 3: A Ponte para o Mundo (API com Busca Simples)
Com os dados guardados, eu precisava de um jeito de acessá-los. Usando o DRF, construí a primeira versão da API. Criei um `Serializer` pra "traduzir" os dados pra JSON e uma `View` que fazia uma busca simples por texto. O primeiro teste no navegador, vendo o JSON aparecer, foi um momento de vitória.

#### Etapa 4: Dando um Cérebro ao Projeto (Embeddings e Busca Semântica)
A grande virada. Modifiquei o scraper para, além de salvar o texto, usar a `sentence-transformers` para criar um vetor de embedding para cada pedaço. Esse vetor, que é puro significado, foi salvo no `ChromaDB`. Depois, refiz a API. Agora, em vez de buscar por palavras, ela transforma a pergunta em um vetor e pede ao ChromaDB os textos com os significados mais parecidos. Foi aqui que o projeto ganhou vida.

## 🤯 Os Quebra-Cabeças: Dificuldades que Encontrei

Nem tudo foram flores! Tive cada dor de cabeça que me ensinou muito.

1.  **O Site que Muda:** Meu primeiro grande erro foi achar que a estrutura do site do Django era sempre igual. O scraper quebrou feio porque o seletor que eu usava (`div#content`) não existia mais. **Aprendizado:** Aprendi na marra que a melhor forma de debugar um scraper é salvando o HTML que ele baixa e investigando o arquivo como um detetive. Foi assim que achei o seletor correto (`article#docs-content`).

2.  **O Fantasma do Código Antigo:** Passei um tempo frustrado porque eu mudava o código, mas o erro continuava o mesmo. **Aprendizado:** Descobri duas pegadinhas clássicas do Python. A primeira era **indentação** errada (um `def` fora do lugar quebra tudo). A segunda era o **cache de bytecode (`__pycache__`)**. O Python estava rodando uma versão antiga do meu script. A solução? Deletar as pastas `__pycache__` e reiniciar o terminal. Foi como um exorcismo!

3.  **Ser Educado com o Servidor:** No começo, o site do Django bloqueava meu script. **Aprendizado:** Descobri que um script não pode chegar "chutando a porta". Adicionei um `User-Agent` para ele se apresentar como um navegador comum, e os servidores me deixaram entrar.

## 🔌 Como Usar: Integrando o MCP-Docs com um Cliente de IA (Gemini)

Beleza, o servidor está pronto, a API funciona. E agora? Como um "usuário do MCP" faz isso virar um assistente de verdade?

A ideia é que a nossa API não foi feita para um humano usar diretamente no navegador. Ela foi feita para ser uma **"ferramenta" (tool)** para um modelo de linguagem grande (LLM), como o Gemini.

É como dar um superpoder para a IA. Por padrão, ela tem o conhecimento geral dela. Ao registrar nossa API como uma ferramenta, a gente ensina pra ela:

> "Olha, Gemini, quando alguém te perguntar algo **específico e técnico sobre a documentação do Django**, não tente adivinhar. Use esta ferramenta que eu criei, que se chama `search_django_docs`, porque ela tem a informação mais atualizada."

#### Passo 1: Definir a Ferramenta (A "Declaração")

No seu cliente (seja a Gemini CLI ou um script Python que usa a API do Gemini), você precisa declarar a ferramenta. É um tipo de "contrato", geralmente em formato JSON, que descreve o que sua ferramenta faz.

**Exemplo de como seria essa declaração:**

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
`name:` O nome que a IA vai usar para chamar a ferramenta.

`description:` A explicação para a IA entender quando usar a ferramenta.

`parameters: ` Descreve os "argumentos" que a ferramenta precisa. No nosso caso, apenas o parâmetro q.

#### Passo 2: A Mágica Acontecendo (O Fluxo)
Uma vez que a ferramenta está registrada no seu cliente Gemini, o fluxo é o seguinte:

Você Pergunta: Você digita na sua CLI: "Ei, Gemini, qual a diferença entre OneToOneField e ForeignKey no Django?"

A IA Decide: O Gemini analisa sua pergunta. Por causa da descrição da nossa ferramenta, ele entende que a melhor forma de responder não é com seu conhecimento geral, mas sim consultando a documentação. Ele decide usar a ferramenta search_django_docs.

A IA Prepara a Chamada: Ele pega sua pergunta e a formata como o parâmetro q da nossa API.

O Cliente Executa: Seu cliente (a CLI) faz a chamada HTTP de verdade para o nosso servidor: GET http://127.0.0.1:8000/api/v1/search/?q=diferença entre OneToOneField e ForeignKey

Nosso Servidor Trabalha: Nosso MCP-Docs recebe a chamada, transforma a pergunta em um vetor, busca no ChromaDB os chunks mais relevantes e os retorna como JSON.

A Resposta da Ferramenta: Seu cliente recebe esse JSON e o envia de volta para a IA, dizendo: "Ok, Gemini, o resultado da ferramenta foi este aqui..."

A IA Sintetiza: Agora vem a melhor parte. O Gemini não te joga o JSON na tela. Ele lê os trechos da documentação que nosso servidor enviou, entende o conteúdo e formula uma resposta final, coesa e em linguagem natural para você.

No final, você tem uma resposta inteligente, baseada na documentação mais recente, tudo de forma automática. Esse é o poder de conectar um LLM a ferramentas personalizadas.
