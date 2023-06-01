import re
import random
import requests
from datetime import datetime, timedelta
import joblib
import re
from urllib.parse import urlparse
import operator
from itertools import islice
import pandas as pd
    
def remove_symbols(text):
    # Remove symbols that are not ASCII letters or numbers
    text = text.replace('https://balancednewssummary.com/', '')
    text = text.replace('-',' ')
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

print(remove_symbols('https://balancednewssummary.com/tina-turner-dies-at-83/'))
def google_news_search(title):
    """
    Function to perform a Google Search with the specified title and URL
    Args:
        title: Title of the Article
        url: URL of the specified article
    Returns:
        search_urls: Similar News Articles found over the Web
        source_sites: Hostname of the Articles founder over the Web
    """
    # target = url
    # domain = urlparse(target).hostname
    # print(title)
    search_urls = []
    source_sites = []
    api_keys = ["10a8210e085717c22dd42c1dc0a255e7"]
    print('after keys')
    if title != "":
        print('title exists')
        title = title.split(" – Balanced News Summary")[0]
        title = remove_symbols(title)

        print(title)
        
        
        url = f"https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={random.choice(api_keys)}&q={title}"
        print('sending request')
        response = requests.get(url)
        print(response.text)
        data = response.json()
        returner = []
        print('fetching articles')
        if "articles" in data:
            print('got articles')
            articles = data["articles"]
            print('1')
            if len(articles) < 1:
                print("Articles not found")
            if len(articles) > 6:
                articles = articles[:6]
            print(len(articles))
            print(articles)
            print('-----')
            for article in articles:
                print('2')

                article_url = article["url"]
                print('3')
                source_name = article["source"]["name"]
                
                print("Article URL:", article_url)
                print("Source Name:", source_name)
                print()
                news_pair = {
                    article_url: source_name
                }
                returner.append(news_pair)
                search_urls.append(article_url)
                source_sites.append(source_name)



    return returner

