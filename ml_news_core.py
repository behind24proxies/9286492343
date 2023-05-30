import warnings
import re
from newspaper import Article
import random
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from duckduckgo_search import DDGS
# lp
from datetime import datetime, timedelta
import joblib
import re
from googlesearch import search
from urllib.parse import urlparse
import operator
from itertools import islice
import pandas as pd

warnings.filterwarnings("ignore")

df = pd.read_excel("output.xls", header=None)

match = df[0].to_list()
proxies = {
    "all://": "http://um3r_it_gmail_com:378042b6a3@85.209.199.227:30017",
    "all://": "http://um3r_it_gmail_com:378042b6a3@85.209.198.123:30017"
}
ddgs = DDGS(proxies=proxies)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
    
def remove_symbols(text):
    # Remove symbols that are not ASCII letters or numbers
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

def extractor(url):
    """
    Extractor function that gets the article body from the URL
    Args:
        url: URL of the News Article/Source
    Returns:
        article: Raw Article Body
        article_title: Title of the Article that has been extracted
    """
    print(url)
    article = Article(url)
    article_title = ""
    try:
        article.download()
        article.parse()


        #Get the article title and convert them to lower-case
        article_title = article.title
        print("extractor")
#         print(article_title)
#         print(article)
        article = article.text.lower()
        article = [article]
    except:
        pass
    return (article, article_title)


def text_area_extractor(text):
    """
    Textbox extractor function to preprocess and extract text
    Args:
        text: Raw Extracted Text from the News Article
    Returns:
        text: Preprocessed and clean text ready for analysis
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub("(\\r|\r|\n)\\n$", " ", text)
    text = [text]
    return text

def duckduckgo_search(title):
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
        print('fetching articles')
        if "articles" in data:
            print('got articles')
            articles = data["articles"]
            print('1')
            if len(articles) < 1:
                print("Articles not found")
            if len(articles) > 3:
                articles = articles[:3]
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
                search_urls.append(article_url)
                source_sites.append(source_name)

        # search_urls = ['https://www.al-monitor.com/originals/2023/05/gulf-space-sector-attracts-private-companies-including-bezos-blue-origin']
        # source_sites = ['Al-Monitor']
        # print(title)
        
        # LP     
        # for result in results:
        # set up the date filter
        # now = datetime.now()
        # timeframe = now - timedelta(days=7)
        # timeframe_str = timeframe.strftime("%Y-%m-%d")
        # end_date = datetime.today()
        # start_date = end_date - timedelta(days=7)

        # # search for articles published in the last week using DuckDuckGo
        # keywords = title
        # results = ddgs.news(keywords, region='wt-wt', safesearch='Moderate', timelimit='w')
        # # set up the date filter for the last 7 days
        # end_date = datetime.today()
        # start_date = end_date - timedelta(days=7)
        # # filter the results by date
        # filtered_results = []
        # print("results", results)
        # for result in results:
        #     try:
        #         # extract the publication date from the URL using a regular expression
        #         # date_str = re.search(r'\d{4}/\d{2}/\d{2}', result.url).group()
        #         date_str = result['date']
        #         result_date = datetime.strptime(date_str, '%Y/%m/%d')

        #         # add the result to the filtered list if its date is within the date range
        #         if start_date <= result_date <= end_date:
        #             filtered_results.append(result)
        #     except (AttributeError, ValueError):
        #         filtered_results.append(result)
        #         pass  

        # print("filtered_results", filtered_results)
        # for result in filtered_results:
        #     if any(x in result["url"] for x in match):
        #     #if "https://balancednewssummary.com/" not in result["href"]:
        #         source_sites.append(result["source"])
        #         search_urls.append(result["url"])
        #         print("result")
        #         print(result)
        # # for i in search(title, tld = "com", num = 10, start = 1, stop = 6):
        # #     if "youtube" not in i and domain not in i:
        # #         source_sites.append(urlparse(i).hostname)
        # #         search_urls.append(i)
    # my_query = 'andrew tate'

    return search_urls, source_sites

def similarity(url_list, article):
    """
    Function to check the similarity of the News Article through Cosine Similarity
    Args:
        url_list: List of the URLs similar to the news article
        article: Preprocessed article which would be vectorized
    Returns:
        cosine_cleaned: Cosine Similarity Scores of each URL passed
        average_score: Average value of the cosine similarity scores fetched
    """
    article = article
    sim_tfv = TfidfVectorizer(stop_words ="english")
    sim_transform1 = sim_tfv.fit_transform(article)
    cosine = []
    cosine_cleaned = []
    cosine_average = 0
    count = 0
    article_titles = []
    for i in url_list:
        try: 
            test_article, test_title = extractor(i)
            print("similarity")
#             print(test_article)
#             print(test_title)
            test_article = [test_article]
            sim_transform2 = sim_tfv.transform(test_article[0])
            score = cosine_similarity(sim_transform1, sim_transform2)
            cosine.append(score*100)
            article_titles.append(test_title)
            count+=1
        except Exception as e:
            print(e) #naked except for handling failed downloads
    for i in cosine:
        x = str(i).replace('[','').replace(']','')
        cosine_cleaned.append(float(x))

    for i in cosine:
        if i !=0:
            cosine_average = cosine_average + i
        else:
            count-=1

    average_score = cosine_average/count
    average_score = str(average_score).replace('[','').replace(']','')
    average_score = float(average_score)
    # return cosine_cleaned, average_score
    return cosine_cleaned,article_titles

def handlelink(article_link):
    """
    Classification function to take the article link and predict the similar news articles
    Args:
        article_link: URL of the article
    Returns:
        pred: Predicted news sources from the machine learning model
        article_title: Title of the Article
        article: Article fetched from the URL 
        url: URL of the article
    """

    job_pac = joblib.load('models/pac.pkl')
    job_vec = joblib.load('models/tfv.pkl')
    url = (article_link)
    article, article_title = extractor(article_link)
    print("handlelink")
    print(article_link)
    print(article)
    print(article_title)
    pred = job_pac.predict(job_vec.transform(article))
    return pred, article_title, article, url


def similarNews(url):
    """
    Driver function to return a dictionary with all the similar news and their similarity score
    Args:
        url: URL of the article
    Returns:
        dictionary: Dictionary containing all the similar news articles and their similarity score
    """
    print("similarNews")
    print(url)
    sorted_d = dict()
    try:
        prediction, article_title, article, url = handlelink(article_link=url)
        url_list, article_titles = duckduckgo_search(article_title)
        # similarity_score, avgScore = similarity(url_list, article)
        similarity_score, article_titles_new = similarity(url_list, article)
        dictionary = dict(zip(url_list, similarity_score))
        url_title_dict = dict(zip(url_list, article_titles_new))

        sorted_d = dict( sorted(dictionary.items(), key=lambda item:item[1],reverse=True))
        for key in sorted_d.keys():
            for index, row in df.iterrows():
                if row[0] in key:
                    sorted_d[key] = row[1]
    except Exception as e:
        print(e)

    l=[]
    c=[]
    r=[]
    
    for key, value in sorted_d.items():
        if value in ["L", "CL"]:
            l.append({key:url_title_dict[key]})
        elif value in ["C"]:
            c.append({key:url_title_dict[key]})
        elif value in ["R", "CR"]:
            r.append({key:url_title_dict[key]})

    lun = [len(l), len(c), len(r)]
    final = []

    for i in range(max(lun)):
        try:
            final.append(l[i])
        except:
            pass
        try:
            final.append(c[i])
        except:
            pass
        try:
            final.append(r[i])
        except:
            pass


    # json_response = [{key:url_title_dict[key], "rating":value} for key, value in sorted_d.items()]

    # for item in json_response:
    #     for index, row in df.iterrows():
    #         if row[0] in item.key:
    #             print(row[0], row[1])
    # print(sorted_d)
    # # url_list = [{key:n_items[key]} for key in n_items]
    # url_list = [{key:article_titles[index]} for index,key in enumerate(sorted_d)]
    # dictionary = [{item,similarity_score[index]} for index,item in enumerate(url_list)]
    # print(dictionary)
    # print(url_title_dict)
    # print(json_response)
    return final[0:3]




if __name__ == "__main___":
    pass
    

