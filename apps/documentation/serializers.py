# apps/documentation/serializers.py

from rest_framework import serializers
from .models import DocumentChunk

class DocumentChunkSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo DocumentChunk.
    E convertendo todos os campos para JSON.
    """
    class Meta:
        model = DocumentChunk
        fields = [
            'id',
            'title',
            'content',
            'source_url',
            'django_version',
        ]