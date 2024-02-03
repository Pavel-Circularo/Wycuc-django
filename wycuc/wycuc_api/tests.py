from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import wikipedia


class WikipediaSearchViewTests(APITestCase):

    @patch('wycuc_api.views.wikipedia.summary')
    @patch('wycuc_api.views.wikipedia.search')
    def test_search_summary_in_czech_languag(self, mock_search, mock_summary):
        mock_search.return_value = ['Rum']
        mock_summary.return_value = 'Rum je alkoholický nápoj destilovaný z melasy nebo ze šťávy získané z cukrové třtiny.'

        response = self.client.get(reverse('wikipedia-search', kwargs={
                                   'search_term': 'rum'}), HTTP_ACCEPT_LANGUAGE='cs')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Rum je alkoholický nápoj destilovaný z melasy nebo ze šťávy získané z cukrové třtiny.',
                      response.data['result'])

    @patch('wycuc_api.views.wikipedia.search')
    def test_search_suggestions_in_czech_language(self, mock_search):
        mock_search.side_effect = [['Rum'], wikipedia.exceptions.DisambiguationError(
            'Rumbellion', ['Rum', 'Rumbellion'])]

        response = self.client.get(reverse('wikipedia-search', kwargs={
                                   'search_term': 'rumbellion'}), HTTP_ACCEPT_LANGUAGE='cs')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertIn({'name': 'Rum'}, response.data['articles'])

    @patch('wycuc_api.views.wikipedia.search')
    def test_search_not_found_in_czech_language(self, mock_search):
        mock_search.return_value = []

        response = self.client.get(reverse('wikipedia-search', kwargs={
                                   'search_term': 'abcefgh'}), HTTP_ACCEPT_LANGUAGE='cs')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(response.data.get('result'))


class WikipediaSearchCachingTest(APITestCase):

    @patch('wycuc_api.views.wikipedia.summary')
    @patch('wycuc_api.views.wikipedia.search')
    def test_wikipedia_summary_caching(self, mock_search, mock_summary):
        search_term = 'Python'
        lang = 'en'
        summary_text = 'Python is a programming language...'

        mock_search.return_value = [search_term]
        mock_summary.return_value = summary_text
        self.client.get(reverse(
            'wikipedia-search', kwargs={'search_term': search_term}), HTTP_ACCEPT_LANGUAGE=lang)

        mock_search.reset_mock()
        mock_summary.reset_mock()

        response = self.client.get(reverse(
            'wikipedia-search', kwargs={'search_term': search_term}), HTTP_ACCEPT_LANGUAGE=lang)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], summary_text)

        mock_search.assert_not_called()
        mock_summary.assert_not_called()

        cache_key = f"wikipedia_summary_{search_term}_{lang}"
        cached_summary = cache.get(cache_key)
        self.assertEqual(cached_summary, summary_text)
