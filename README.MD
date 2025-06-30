# MCP Django Documentation Project

## API de Busca por Palavra-Chave

Nesta etapa, o objetivo foi construir a primeira versão funcional da API do nosso servidor. Esta API serve como uma "ponte" entre os dados que coletamos e armazenamos no banco de dados e o mundo exterior, permitindo que um cliente faça buscas simples baseadas em texto.

**Tecnologias Utilizadas:**
* Django
* Django REST Framework (DRF)

### Componentes Criados

A implementação seguiu o padrão do Django REST Framework, dividindo a lógica em três componentes principais:

#### 1. Serializer (`serializers.py`)

* **Propósito:** Atua como um "tradutor", convertendo os objetos `DocumentChunk` do nosso banco de dados (que são objetos Python) para o formato JSON, que é um formato de texto leve e universal para a web.
* **Implementação:** Foi criado um `DocumentChunkSerializer` que herda de `serializers.ModelSerializer`, especificando os campos que devem ser incluídos na resposta da API.

    ```python
    # apps/documentation/serializers.py
    from rest_framework import serializers
    from .models import DocumentChunk

    class DocumentChunkSerializer(serializers.ModelSerializer):
        class Meta:
            model = DocumentChunk
            fields = [
                'id',
                'title',
                'content',
                'source_url',
                'django_version',
            ]
    ```

#### 2. View (`views.py`)

* **Propósito:** É o "cérebro" da API. A View é responsável por receber a requisição do cliente, entender o que ele quer, executar a lógica de busca no banco de dados e retornar uma resposta formatada.
* **Lógica Implementada:**
    1.  A view extrai o termo de busca do parâmetro `q` na URL (ex: `?q=models`).
    2.  Utiliza os `Q objects` do Django para fazer uma busca *case-insensitive* (`__icontains`) no banco de dados, procurando pelo termo no campo `title` **OU** no campo `content`.
* **Refatoração para Melhores Práticas:** Inicialmente implementada como uma `APIView` básica, a view foi refatorada para usar a classe genérica `generics.ListAPIView` do DRF. Isso tornou o código mais limpo, declarativo e alinhado com os padrões da comunidade.

    ```python
    # apps/documentation/views.py
    from django.db.models import Q
    from rest_framework import generics
    from .models import DocumentChunk
    from .serializers import DocumentChunkSerializer

    class SearchAPIView(generics.ListAPIView):
        serializer_class = DocumentChunkSerializer

        def get_queryset(self):
            query = self.request.query_params.get('q', None)
            if query:
                return DocumentChunk.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
            return DocumentChunk.objects.none()
    ```

#### 3. URLs (`urls.py`)

* **Propósito:** Define o "endereço" ou "endpoint" que os clientes usarão para acessar a nossa `SearchAPIView`.
* **Estrutura:** Foi criada uma rota `search/` dentro do app `documentation`, que por sua vez foi incluída na rota principal do projeto sob o prefixo `api/v1/`.
* **Endpoint Final:** `http://127.0.0.1:8000/api/v1/search/`

### Como Testar a API

1.  Garanta que o banco de dados foi populado com o comando `manage.py import_docs`.
2.  Inicie o servidor de desenvolvimento com `python manage.py runserver`.
3.  Abra um navegador e acesse a URL, passando um termo de busca no parâmetro `q`. Por exemplo:
    **`http://127.0.0.1:8000/api/v1/search/?q=model`**
4.  O resultado esperado é a página da API navegável do DRF, exibindo uma lista de resultados em formato JSON.

### Conclusão da Etapa

Ao final desta etapa, temos um servidor com uma API de busca por palavra-chave totalmente funcional. A base está pronta e testada, abrindo caminho para a próxima fase: a implementação da busca semântica para fornecer resultados mais inteligentes e contextuais.


## Troubleshooting e Depuração

Esta seção documenta os desafios encontrados durante o desenvolvimento do scraper de documentação (`import_docs`) e as soluções que apliquei.

### Desafio 1: O Seletor de Conteúdo Instável

Quando estava tentando fazer uma requisição no site da documentação do django estava me deparando com um erro, onde buscava o conteudo principal da pagina pela **DIV** **id="#content"** e depois mudei para o **_div[role="main"]_**, não tinha resolvido.

#### Sintoma

Ao executar o comando de importação, o script falhava com uma mensagem de erro indicando que o contêiner principal do conteúdo não foi encontrado.

```bash
# Erro inicial
(mcp-env) ...> python manage.py import_docs 5.2 topics/db/models/
Buscando conteúdo de: [https://docs.djangoproject.com/en/5.2/topics/db/models](https://docs.djangoproject.com/en/5.2/topics/db/models)
Não foi possível encontrar a div de conteúdo principal (#content).
```

# Erro após a primeira tentativa de correção
```bash
(mcp-env) ...> python manage.py import_docs 5.2 topics/db/models/
Buscando conteúdo de: [https://docs.djangoproject.com/en/5.2/topics/db/models](https://docs.djangoproject.com/en/5.2/topics/db/models)
Não foi possível encontrar a div de conteúdo principal (div[role="main"]).
```

As tentativas iniciais de usar seletores comuns como **_soup.find('div', id='content') ou soup.find('div', role='main')_** falharam. Isso indicou que a estrutura do site **docs.djangoproject.com** não seguia mais esse padrão.

Para corrigir o problema, salvei o conteúdo HTML exato que a biblioteca requests estava recebendoe em um arquivo local, para permitir analisar manualmente qual era a **_DIV_** do conteudo principal.

Então fiz um codigo que salvava a pagina em um arquivo:

```bash
soup = BeautifulSoup(response.content, 'html.parser')

try:
    with open("debug_output.html", "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))
    
    self.stdout.write(self.style.SUCCESS("\nArquivo 'debug_output.html' salvo."))
    return 
except Exception as e:
    self.stderr.write(self.style.ERROR(f"Erro ao salvar o arquivo de debug: {e}"))
```

## Solução
Ao analisar o arquivo **debug_output.html**, descobri que o contêiner correto para o conteúdo da documentação era a tag **<article> com o id="docs-content"**.

**_Poderia ter feito isso manualmente indo na documentção e inspecionando a pagina, mas optei por tentar em codigo._**

Então só alterei a linha do main_content e mudei o id:

```bash
# A solução final e funcional
main_content = soup.find('article', id='docs-content')
```

Também adicionei o **_User-Agent_**: Para evitar que o servidor bloqueie o meu script por identificá-lo como um robô, adicionei ao cabeçalho da requisição **requests**

```bash
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(scrape_url, headers=headers)
```