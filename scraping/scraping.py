import requests
from bs4 import BeautifulSoup


def get_articles():
    response = requests.get('https://habr.com/ru/all/')
    if response.status_code != 200:
        raise Exception
    text = response.text
    soup = BeautifulSoup(text, features="html.parser")
    all_article = soup.find_all('article', class_="post post_preview")
    return all_article


def searching(article, words):
    for word in words:
        item = []   # время - название - ссылка
        if word in article.text:
            name = article.find("a", class_="post__title_link").text
            link = article.find("a", class_="post__title_link")['href']
            time = article.find("span", class_="post__time").text
            item.append(time)
            item.append(name)
            item.append(link)
            print(item)
            return item


if __name__ == '__main__':
    KEYWORDS = ['Дизайн', 'Фото', 'Web', 'Python', 'Программирование']  # теги должны быть с большой буквы
    for art in get_articles():
        searching(art, KEYWORDS)
