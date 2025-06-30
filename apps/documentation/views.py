# apps/documentation/views.py

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DocumentChunk
from .serializers import DocumentChunkSerializer

class SearchAPIView(APIView):
    """
    View da API para buscar nos fragmentos da documentação.
    Aceita uma query via parâmetro GET 'q'.
    Ex: /api/search/?q=sua_busca
    """
    def get(self, request, *args, **kwargs):
        
        # 1. Pega o termo de busca dos parâmetros da URL
        query = request.query_params.get('q', None)

        if not query:
            # Se nenhuma busca for fornecida, retorna um erro amigável.
            return Response(
                {"error": "O parâmetro de busca 'q' é obrigatório. Exemplo de URL: ...search/?q=model"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Faz a busca no banco de dados (case-insensitive)
        # Busca no título OU no conteúdo.
        search_results = DocumentChunk.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        # 3. Usa o Serializer para "traduzir" os resultados
        serializer = DocumentChunkSerializer(search_results, many=True)

        # 4. Retorna a resposta em JSON
        return Response(serializer.data, status=status.HTTP_200_OK)