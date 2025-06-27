import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from django.core.management.base import BaseCommand
from django.utils.text import slugify

# Importe nosso modelo
from documentation.models import DocumentChunk

class Command(BaseCommand):
    help = 'Importa e processa uma página da documentação do Django para o banco de dados.'

    def add_arguments(self, parser):
        parser.add_argument('version', type=str, help='A versão do Django para importar (ex: 4.2).')
        parser.add_argument('page_path', type=str, help='O caminho da página na documentação (ex: topics/db/models/).')

    def handle(self, *args, **options):
        version = options['version']
        page_path = options['page_path'].strip('/')
        
        base_url = f'https://docs.djangoproject.com/en/{version}/'
        scrape_url = urljoin(base_url, page_path)

        self.stdout.write(self.style.HTTP_INFO(f'Buscando conteúdo de: {scrape_url}'))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(scrape_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Erro ao buscar a página: {e}'))
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- A CORREÇÃO FINAL ESTÁ AQUI ---
        # Usando o seletor que descobrimos na nossa investigação.
        main_content = soup.find('article', id='docs-content')

        if not main_content:
            # Mensagem de erro atualizada para o seletor correto.
            self.stderr.write(self.style.ERROR('Não foi possível encontrar o container do conteúdo (article#docs-content). O site pode ter mudado.'))
            return

        page_title = main_content.find('h1').text.strip() if main_content.find('h1') else 'Título não encontrado'
        
        self.stdout.write(f"Título da página: {page_title}")

        sections = main_content.find_all('h2')
        total_chunks = 0

        for header in sections:
            section_title = header.text.strip()
            content_pieces = []

            for sibling in header.find_next_siblings():
                if sibling.name == 'h2':
                    break
                content_pieces.append(sibling.get_text(separator=' ', strip=True))
            
            chunk_content = ' '.join(content_pieces)
            
            section_id = header.get('id', slugify(section_title))
            chunk_url = f"{scrape_url}#{section_id}"

            chunk, created = DocumentChunk.objects.update_or_create(
                source_url=chunk_url,
                defaults={
                    'title': f"{page_title} - {section_title}",
                    'content': chunk_content,
                    'django_version': version,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  -> Criado chunk para a seção: "{section_title}"'))
                total_chunks += 1
            else:
                self.stdout.write(self.style.WARNING(f'  -> Atualizado chunk para a seção: "{section_title}"'))

        self.stdout.write(self.style.SUCCESS(f'\nImportação concluída! {total_chunks} novos chunks criados.'))