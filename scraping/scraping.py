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


def searching(words):
    articles = []
    for art in get_articles():
        for word in words:
            item = []   # время - название - ссылка
            if word in art.text:
                name = art.find("a", class_="post__title_link").text
                link = art.find("a", class_="post__title_link")['href']
                time = art.find("span", class_="post__time").text
                item.append(time)
                item.append(name)
                item.append(link)
                articles.append(item)
    if articles:
        return articles
    else:
        return 'Статей по данным тегам не найдено'


if __name__ == '__main__':
    KEYWORDS = ['Дизайн', 'Фото', 'Web', 'Python', 'Информационная безопасность']  # теги должны быть с большой буквы
    print(searching(KEYWORDS))
