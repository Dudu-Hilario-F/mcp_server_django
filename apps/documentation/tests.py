from django.test import TestCase
from django.urls import reverse

class APITestCase(TestCase):
    def test_search_endpoint(self):
        """Testa se o endpoint de busca responde corretamente."""
        url = reverse('search')  # Usa o nome da URL para evitar hardcoding
        response = self.client.get(url, {'q': 'test'})

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se a resposta contém a estrutura esperada (uma lista de resultados)
        self.assertIn('results', response.json())
