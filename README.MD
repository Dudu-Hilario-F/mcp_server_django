# MCP Django Documentation Project

... 

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