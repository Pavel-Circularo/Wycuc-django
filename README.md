# Wýcuc - Wikipedia API Project

This REST API enables fetching information from Wikipedia based on search terms and specified language.  
It allows searching for articles with a given term and returns the first paragraph of the article in the requested language, a list of articles containing the term if the exact article is not found, or a 404 response if no relevant articles exist.

## Installation Instructions

Follow these steps to get the project up and running on your local machine.

### Step 1: Setting Up Virtual Environment

Before you start, make sure you have Python 3.11 installed. Then, create and activate a virtual environment to isolate project dependencies:

```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

### Step 2: Installing Dependencies

With the virtual environment activated, install the required dependencies by running:

```
pip install -r requirements.txt
```

## Running the Application

To run the server on your local machine, navigate to project folder and execute:
```
python manage.py runserver
```
## API Usage
To use the API, make a GET request to ```/wiki/<search_term>/``` where ```<search_term>``` is your query. You can specify the language of the search results using the Accept-Language header in your request.

### Example Requests
Using curl to fetch information about "rum" in Czech language:

```
curl -H "Accept-Language: cs" http://localhost:8000/wiki/rum
```

### Running Tests
To ensure everything is working as expected, you can run the provided tests with:
```
python manage.py test wycuc_api
```
