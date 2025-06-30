# apps/documentation/urls.py

from django.urls import path
from .views import SearchAPIView

urlpatterns = [
    # Mapeia a URL 'search/' para a nossa SearchAPIView
    path('search/', SearchAPIView.as_view(), name='search_api'),
]