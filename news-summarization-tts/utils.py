from newspaper import Article
from bs4 import BeautifulSoup
import nltk
import requests
nltk.download('punkt')
nltk.download('punkt_tab')


def generate_related_urls1(title):
    from duckduckgo_search import DDGS
    num_results = 11
    with DDGS() as ddgs:
        results = ddgs.text(title, max_results=num_results)
        return [result["href"] for result in results]

def generate_related_urls(title):
    """
    :param title: str
    :param num_results: int
    :return: list
    """
    from googlesearch import search
    urls_list = []
    num_results = 11
    for url in search(title, num_results=num_results):
        if url.startswith("https") and "google.com/search" not in url:
            urls_list.append(url)
    return urls_list

def extract_data(title):
    """
    :param title: str
    :param max_articles:int
    :return: dict
    """
    urls_list = generate_related_urls(title)
    articles_data = []
    for url in urls_list[:11]:
        print(f"Processing URL: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"Success: {url}\n")
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                h1_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                topics_list = []
                for h1 in h1_tags:
                    topics_list.append(h1.text.strip())
                article = Article(url, language="en")
                article.download()
                article.parse()
                article.nlp()
                article_data =[ {
                    "url": url,
                    "title": article.title,
                    "text": article.text,
                    "authors": article.authors,
                    "published_date": str(article.publish_date) if article.publish_date else "Unknown",
                    "top_image": article.top_image,
                    "videos": article.movies,
                    "keywords": article.keywords,
                    "summary": article.summary,
                    "topics": topics_list
                }]
                articles_data.append(article_data)

            elif response.status_code == 404:
                print(f"Error: 404 Not Found - {url}\n")
            elif response.status_code == 403:
                print(f"Error: 403 Forbidden - {url}. Access Denied.\n")
        except Exception as e:
            print(f"Failed to process {url}: {str(e)}\n")
        finally:
            print("=" * 50 + "\n")

    return articles_data


