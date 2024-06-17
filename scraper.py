from bs4 import BeautifulSoup, ResultSet, Tag
import requests
import re
import json


# TODO: what to do about duplicates


def get_news_tags(host: str, path: str) -> list[dict]:
    with requests.get(f"{host}{path}") as response:
        html = BeautifulSoup(response.text, "html.parser")
        a_tags: ResultSet[Tag] = html.find_all("a", href=True)

        res: list[dict] = []
        for tag in a_tags:
            path = str(tag.get("href"))
            if re.search(r"/news/articles/.+", path) != None:
                res.append(
                    {
                        "title": str(tag.text),
                        "path": path,
                        "url": f"{host}{path}",
                    }
                )

        return res


news_tags: list[dict] = []
host = "https://www.bbc.co.uk"
path = "/news"

index = 0
while len(news_tags) < 1000:
    news_tags += get_news_tags(host, path)
    path = news_tags[index].get("path")
    index += 1


# TODO: use db
with open("links.json", "w") as f:
    json.dump(news_tags, f, indent=2)
