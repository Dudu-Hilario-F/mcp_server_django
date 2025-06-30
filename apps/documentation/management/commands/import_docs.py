import requests
import chromadb
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from sentence_transformers import SentenceTransformer

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings

# Importe nosso modelo
from documentation.models import DocumentChunk

# Configuração do Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("import_docs.log"),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = 'Importa, processa e gera embeddings para uma página da documentação do Django.'

    def add_arguments(self, parser):
        parser.add_argument('version', type=str, help='A versão do Django a ser importada (ex: 5.2).')
        parser.add_argument('page_path', type=str, help='O caminho da página na documentação (ex: topics/db/models/).')

    def handle(self, *args, **options):
        
        # --- 1. INICIALIZAÇÃO DOS MODELOS E DO VETOR DB ---
        logger.info("Inicializando o banco de dados vetorial ChromaDB...")

        # Cria um cliente ChromaDB que salva os dados em disco na pasta 'chroma_db'
        client = chromadb.PersistentClient(path=str(settings.BASE_DIR / "chroma_db"))
        
        # Pega ou cria uma "coleção" (como se fosse uma tabela) para nossos documentos
        collection = client.get_or_create_collection(name="django_docs")
        
        logger.info("Carregando o modelo de embeddings (isso pode levar um momento)...")
        # Carrega um modelo pré-treinado. 'all-MiniLM-L6-v2' é um ótimo modelo, rápido e de alta qualidade.
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Modelo e DB prontos.")

        # --- 2. LÓGICA DE SCRAPING (como antes) ---
        version = options['version']
        page_path = options['page_path'].strip('/')
        
        base_url = f'https://docs.djangoproject.com/en/{version}/'
        scrape_url = urljoin(base_url, page_path)

        logger.info(f'Buscando conteúdo de: {scrape_url}')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(scrape_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f'Erro ao buscar a página: {e}')
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('article', id='docs-content')

        if not main_content:
            logger.error('Não foi possível encontrar o container do conteúdo (article#docs-content).')
            return

        page_title = main_content.find('h1').text.strip() if main_content.find('h1') else 'Título não encontrado'
        logger.info(f"Título da página: {page_title}")

        sections = main_content.find_all('h2')
        
        # --- 3. PROCESSAMENTO, SALVAMENTO E GERAÇÃO DE EMBEDDING ---
        for header in sections:
            section_title = header.text.strip()
            content_pieces = []

            for sibling in header.find_next_siblings():
                if sibling.name == 'h2':
                    break
                content_pieces.append(sibling.get_text(separator=' ', strip=True))
            
            chunk_content = ' '.join(content_pieces)
            
            # Pula seções vazias que não têm conteúdo útil para a busca
            if not chunk_content.strip():
                logger.warning(f'  -> Pulando seção vazia: "{section_title}"')
                continue

            section_id = header.get('id', slugify(section_title))
            chunk_url = f"{scrape_url}#{section_id}"

            # Salva no banco de dados relacional (SQLite/PostgreSQL)
            chunk, created = DocumentChunk.objects.update_or_create(
                source_url=chunk_url,
                defaults={
                    'title': f"{page_title} - {section_title}",
                    'content': chunk_content,
                    'django_version': version,
                }
            )

            # --- 4. A NOVA ETAPA: GERAR E SALVAR O EMBEDDING NO CHROMADB ---
            logger.info(f'  -> Gerando embedding para a seção: "{section_title}"...')
            
            # Gera o vetor a partir do conteúdo do chunk
            embedding = embedding_model.encode(chunk.content).tolist()
            
            # Adiciona (ou atualiza) o vetor no ChromaDB.
            # Usamos o ID do chunk do nosso banco Django como o ID no ChromaDB
            # para manter os dois sincronizados.
            collection.upsert(
                ids=[str(chunk.id)],
                embeddings=[embedding],
                metadatas=[{'title': chunk.title, 'source_url': chunk.source_url}]
            )
            logger.info(f'  -> Embedding salvo para o chunk ID: {chunk.id}')

        logger.info(f'\nImportação e processamento de embeddings concluídos!')