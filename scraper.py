from bs4 import BeautifulSoup, ResultSet, Tag
import requests
import re
import psycopg2
from dotenv import load_dotenv
import os


# TODO: what to do about duplicates


load_dotenv(".env.development.local")


def get_news_tags(host: str, path: str) -> list[dict[str, str]]:
    url = f"{host}{path}"
    print(url)
    with requests.get(url) as response:
        html = BeautifulSoup(response.text, "html.parser")
        a_tags: ResultSet[Tag] = html.find_all("a", href=True)

        res: list[dict] = []
        for tag in a_tags:
            path = str(tag.get("href"))
            if re.search(r"/news/articles/.+", path) != None:
                res.append({"title": str(tag.text), "path": path, "url": url})

        return res


connection = psycopg2.connect(
    database=os.environ["POSTGRES_DATABASE"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
)

news_tags: list[dict[str, str]] = []
host = "https://www.bbc.co.uk"
path = "/news"

index = 0
while len(news_tags) < 1000:
    news_tags += get_news_tags(host, path)
    path = news_tags[index].get("path")
    index += 1

with connection.cursor() as curs:
    curs.execute(
        """
            CREATE TABLE IF NOT EXISTS news_links (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                path TEXT NOT NULL,
                url TEXT NOT NULL
            );
        """
    )
    insert_query = "INSERT INTO news_links (title, path, url) VALUES (%(title)s, %(path)s, %(url)s);"
    curs.executemany(insert_query, news_tags)
    connection.commit()
