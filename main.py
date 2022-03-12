import requests
from bs4 import BeautifulSoup

DESIRED_HUBS = ['HTML', 'Java', 'Git', 'Python']
URL = 'https://habr.com/ru/all/'

def getDataFromSite(URL):
    HEADERS = {
    'Sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    ret = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(ret.text, 'html.parser')

    return soup

def getListOfArticles ():
    URL_ = 'https://habr.com'
    filtered_articles = []
    soup = getDataFromSite(URL)
    main_block = soup.find('main')
    articles = main_block.find_all("article")
    for article in articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = set(hub.find("span").text.strip() for hub in hubs)
        preview = article.find(class_="article-formatted-body")
        title = article.find(class_ = 'tm-article-snippet__title-link')
        href = title.get_attribute_list('href')[0]
        for keyword in DESIRED_HUBS:
            if (keyword in hubs) or (preview.get_text().find(keyword) >= 0) or (title.get_text().find(keyword) >= 0):   
                filtered_articles.append({'title': title.get_text(), 'href': URL_ + href, 'time' : article.time.get_attribute_list('title')[0]})
                       
    return filtered_articles

def showTextWithMatchedWords(objs):
    for obj in objs:
        soup = getDataFromSite(obj['href']) 
        article_text_all = soup.find_all('p')
        print()
        for paragraph in article_text_all:
            count = 0
            for keyword in DESIRED_HUBS:
                if paragraph.text.find(keyword) >= 0:
                    count = count + 1
            if count > 0:
                print(paragraph.text)
                    


if __name__ == '__main__':

    articles = getListOfArticles()
    for article in articles:
        print(f'{article["time"]} - "{article["title"]}" - URL={article["href"]}\r\n')    
    showTextWithMatchedWords(articles)