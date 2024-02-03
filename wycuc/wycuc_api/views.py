from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import wikipedia


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

        try:
            search_results = wikipedia.search(search_term)
            if not search_results:
                return Response({'result': None}, status=status.HTTP_404_NOT_FOUND)

            if search_term.lower() == search_results[0].lower():
                summary = wikipedia.summary(search_term)
                return Response({'result': summary}, status=status.HTTP_200_OK)
            else:
                articles = [{'name': item} for item in search_results]
                return Response({'result': None, 'articles': articles}, status=status.HTTP_303_SEE_OTHER)

        except wikipedia.exceptions.DisambiguationError as e:
            articles = [{'name': item} for item in e.options]
            return Response({'result': None, 'articles': articles}, status=status.HTTP_303_SEE_OTHER)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
