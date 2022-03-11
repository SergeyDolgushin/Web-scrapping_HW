import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Cookie': '_ym_uid=1640608840610531527; _ym_d=1640608840; _ga=GA1.2.1177545873.1640608888; fl=ru; hl=ru; __gads=ID=6652a488f81f66d5:T=1640608887:S=ALNI_MYB2hNhIBEjzorkNxrjj7-Hu0jTQQ; cto_bundle=NIgIr182Vk5sV0lPbkRsREZ5clhHV1U1SlIwNjBucWNXcmJBUTY4V0lndUFIV2ttdEFXVkE1UGRpeXBZQXJjSyUyRjZZYkJ1RHc0aVJoJTJGNzZVemhDNnV6ejZKJTJCczAzZ2ZuaCUyQjlUZ0UlMkZscXAzMGZwZlkzNGZ3R255RUh0TXpGSTV1UENaOTBCdTRrWE9RclVJVExLJTJGTEpKMzIzd1ElM0QlM0Q; visited_articles=534488:342922:110731:653605:541256:269497:43955:254773:647619:554274; _ym_isad=1; _gid=GA1.2.543365982.1646935597; habr_web_home_feed=/all/; _gat=1',
    'Sec-ch-ua-platform': "Windows",
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-ch-ua-mobile': '?0',
    'Sec-ch-ua-user': '?1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'If-None-Match': 'W/"2a75-8MMP9mXkL25QhWi9LxIhHPKAtRU"',
    'Referer': 'https://habr.com/ru/all/',
    'x-app-version': '2.66.0'
}

DESIRED_HUBS = ['HTML', 'Java', 'Git', 'Python']

def getListOfArticles ():
    URL = 'https://habr.com/ru/all/'
    URL_ = 'https://habr.com'
    all_articles = []
    ret = requests.get(URL, HEADERS)
    soup = BeautifulSoup(ret.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = article.find(class_ = 'tm-article-snippet__title-link')
        href = title.get_attribute_list('href')[0]
        all_articles.append({'title': title.get_text(), 'href': URL_ + href, 'time' : article.time.get_attribute_list('title')[0]})
        
    return all_articles

def filteredArticles(objs):
    filtered_articels = []
    for obj in objs:
        ret = requests.get(obj['href'], HEADERS)
        soup = BeautifulSoup(ret.text, 'html.parser')
        tags = soup.find_all(class_='tm-article-snippet__hubs-item')
        hubs = set(hub.text.strip() for hub in tags)
        for hub in hubs:
            if hub[:-2] in DESIRED_HUBS:
                filtered_articels.append(obj)
    for article in filtered_articels:
        print(f'{article["time"]} "{article["title"]}" URL={article["href"]}\r\n')

    return filtered_articels

def showTextWithMatchedWords(objs):
    for obj in objs:
        ret = requests.get(obj['href'], HEADERS)
        soup = BeautifulSoup(ret.text, 'html.parser')    
        article_text_all = soup.find_all('p')
        for paragraph in article_text_all:
            for keyword in DESIRED_HUBS:
                if paragraph.text.find(keyword) >= 0:
                    print(paragraph.text)
                    


if __name__ == '__main__':

    articles = getListOfArticles()
    filtered_articels = filteredArticles(articles)
    showTextWithMatchedWords(filtered_articels)