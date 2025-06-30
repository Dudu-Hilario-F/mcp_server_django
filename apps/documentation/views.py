from django.db.models import Q
from rest_framework import generics 

from .models import DocumentChunk
from .serializers import DocumentChunkSerializer

# A nossa view agora herda de generics.ListAPIView
class SearchAPIView(generics.ListAPIView):
    """
    View da API para buscar nos fragmentos da documentação.
    Usa o padrão de ListAPIView do DRF para uma implementação mais limpa.
    Aceita uma query via parâmetro GET 'q'.
    Ex: /api/v1/search/?q=sua_busca
    """
    # Definimos o serializer como um atributo da classe.
    serializer_class = DocumentChunkSerializer

    def get_queryset(self):
        """
        Este método é sobrescrito para controlar o conjunto de dados (queryset)
        que a view irá retornar. A lógica de busca fica toda aqui.
        """
        # 1. Pega o termo de busca dos parâmetros da URL
        query = self.request.query_params.get('q', None)

        # 2. Se uma query foi fornecida, filtra o banco de dados.
        if query:
            # Verifica se a busca não retornou none
            return DocumentChunk.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        # 3. Aqui a listview trata a query vazia caso nenhuma query foi fornecida, retorna um queryset vazio.
        # A ListAPIView vai lidar com isso e retornar uma lista vazia `[]` 
        return DocumentChunk.objects.none()