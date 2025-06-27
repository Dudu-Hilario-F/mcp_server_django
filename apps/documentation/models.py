from django.db import models

class DocumentChunk(models.Model):
    """
    Esse Modelo de BD representa a vetorização pedaços ou fragmentos da documentação do django
    que esta descrita no README.MD do projeto.

    Onde vamos usar o ChromaDB para vetorizar os conteudos e armazenar no banco de dados para buscas semanticas

    # O ID deste modelo será usado para linkar com o vetor no ChromaDB.
    # O Django vai criar um ID automático.
    """

    
    source_url = models.URLField(
        max_length=1024, 
        unique=True, 
        help_text="URL de origem do fragmento da documentação."
    )

    title = models.CharField(
        max_length=512, 
        help_text="Título da página ou da seção de onde o fragmento foi extraído."
    )

    content = models.TextField(
        help_text="O conteúdo de texto limpo do fragmento da documentação."
    )

    django_version = models.CharField(
        max_length=20, 
        help_text="Versão do Django a que esta documentação se refere (ex: '4.2')."
    )

    # Timestamps para controle interno.
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="Data e hora em que o registro foi criado."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última atualização."
    )

    def __str__(self):
        return f"{self.title} ({self.django_version})"

    class Meta:
        verbose_name = "Fragmento da Documentação"
        verbose_name_plural = "Fragmentos da Documentação"
        ordering = ['-created_at']