from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import wikipedia
import logging

logger = logging.getLogger(__name__)


class WikipediaSearchView(APIView):
    """
    View for searching Wikipedia articles.

    This view handles GET requests and searches for articles on Wikipedia based on the provided search term.
    It returns a response with the search results, including a summary of the article if an exact match is found.
    """

    def get(self, request, search_term):
        """
        Handle GET requests for searching Wikipedia articles.

        Args:
            request (HttpRequest): The HTTP request object.
            search_term (str): The search term for the Wikipedia article.

        Returns:
            Response: The HTTP response object containing the search results.

        Raises:
            wikipedia.exceptions.DisambiguationError: If the search term is ambiguous and multiple articles are found.
            Exception: If any other error occurs during the search process.
        """

        lang = request.headers.get(
            'Accept-Language', 'en').split(',')[0].split('-')[0]
        wikipedia.set_lang(lang)

        cache_key = f"wikipedia_summary_{search_term}_{lang}"
        cached_summary = cache.get(cache_key)

        if cached_summary:
            return Response({'result': cached_summary}, status=status.HTTP_200_OK)

        try:
            search_results = wikipedia.search(search_term)
            if not search_results:
                return Response({'result': None}, status=status.HTTP_404_NOT_FOUND)

            if search_term.lower() == search_results[0].lower():
                summary = wikipedia.summary(search_term)
                cache.set(cache_key, summary, 3600)
                return Response({'result': summary}, status=status.HTTP_200_OK)
            else:
                articles = [{'name': item} for item in search_results]
                return Response({'result': None, 'articles': articles}, status=status.HTTP_303_SEE_OTHER)

        except wikipedia.exceptions.DisambiguationError as e:
            articles = [{'name': item} for item in e.options]
            return Response({'result': None, 'articles': articles}, status=status.HTTP_303_SEE_OTHER)
        except wikipedia.exceptions.PageError as e:
            logger.error(
                f'Page not found for search term "{search_term}": {str(e)}')
            return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(
                f'Unexpected error while searching for "{search_term}": {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
