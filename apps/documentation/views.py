# apps/documentation/views.py

import chromadb
from sentence_transformers import SentenceTransformer

from django.conf import settings
from rest_framework import generics

from .models import DocumentChunk
from .serializers import DocumentChunkSerializer

# --- Inicialização dos Modelos e do Cliente ChromaDB ---
# Em um cenário de produção real, carregar estes modelos a cada requisição não é o ideal.
# Para este projeto, é uma abordagem simples e funcional. Em projetos maiores,
# estes objetos seriam carregados uma única vez na inicialização do servidor.

# Carregando o modelo
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Conecta-se ao mesmo banco de dados vetorial persistente
client = chromadb.PersistentClient(path=str(settings.BASE_DIR / "chroma_db"))
collection = client.get_or_create_collection(name="django_docs")


class SearchAPIView(generics.ListAPIView):
    """
    View da API que realiza a BUSCA SEMÂNTICA nos fragmentos da documentação.
    """
    serializer_class = DocumentChunkSerializer

    def get_queryset(self):
        """
        Este método agora executa a busca semântica.
        """
        query = self.request.query_params.get('q', None)

        if not query:
            # Se não houver query, retorna uma lista vazia.
            return DocumentChunk.objects.none()

        # 1. Transforma a query do usuário em um vetor de embedding.
        print(f"Gerando embedding para a query: '{query}'")
        query_embedding = embedding_model.encode(query).tolist()

        # 2. Faz a busca por similaridade no ChromaDB.
        # Estamos pedindo os 10 resultados mais próximos.
        print("Buscando por similaridade no ChromaDB...")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10
        )

        # 3. Extrai os IDs dos resultados.
        chunk_ids = results.get('ids', [[]])[0]
        
        if not chunk_ids:
            return DocumentChunk.objects.none()
        
        print(f"IDs encontrados no ChromaDB: {chunk_ids}")

        # 4. Busca os objetos completos no banco de dados Django usando os IDs.
        # É importante manter a ordem de relevância retornada pelo ChromaDB.
        chunks_from_db = DocumentChunk.objects.filter(id__in=chunk_ids)
        
        # Mapeia os chunks por ID para poder reordenar
        chunks_map = {str(chunk.id): chunk for chunk in chunks_from_db}
        
        # Reordena os objetos
        ordered_chunks = [chunks_map[id_str] for id_str in chunk_ids if id_str in chunks_map]

        return ordered_chunks