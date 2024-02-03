from django.urls import path
from .views import WikipediaSearchView

urlpatterns = [
    path('<str:search_term>', WikipediaSearchView.as_view(),
         name='wikipedia-search'),
]
