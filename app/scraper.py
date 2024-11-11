import asyncio, re, aiohttp
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from lxml import html
from functions import *
from classes import *
import threading, pprint

class Scraper(threading.Thread, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self):
        pass
    
    async def fetch_page(self, session, url):
        while True:
            async with session.get(url) as response:
                if response.status == 429:
                    await asyncio.sleep(2)
                else:
                    html_content = await response.text()
                    try:
                        html_content = re.sub(r'^<\?xml.*?\?>', '', html_content)
                    except Exception as e:
                        pass
                    soup = BeautifulSoup(html_content, 'html.parser')

                    return html.fromstring(soup.prettify())
    
    @abstractmethod
    async def getPage(self, url):
        async with aiohttp.ClientSession() as session:
            task = self.fetch_page(session, url)
            html = await asyncio.gather(task)
        return html[0]
    
    @abstractmethod
    async def getPosts(self, posts, xpath, model, logger):
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            tasks = []
            for key in posts:
                if posts[key]['link'] != "https://bahianoar.com/gilberto-gil-reage-apos-xingamentos-em-jogo-da-copa-do-mundo-veja-video/":
                    tasks.append(self.fetch_page(session, posts[key]['link']))
            htmls = await asyncio.gather(*tasks)

            try:
                for slug, tree in zip([posts[key]['slug'] for key in posts], htmls):
                    await self.posting(tree, posts[slug], xpath, model)
            except Exception as e:
                print(e)

    async def posting(self, tree, post, xpath, model):
        headers = {'Content-Type': 'application/json'}
        self.csv = CSVManager(model)
        self.json = JsonManager(model)

        for xph in xpath:
            temp = tree.xpath(xpath[xph])
            match xph:
                case "text":
                    post[xph] = temp[0].text_content().strip()
                case "tag":
                    post[xph] = list()
                    for tag in temp:
                        tag = get_slug(tag.get("href"))
                        result_set = self.csv.search("tag", "tag", tag)
                        if result_set is None:
                            if len(self.csv.read("category")) == 0:
                                data = list()
                                data.append({"id": 0, "tag": tag})
                                self.csv.write("tag", data)
                                post[xph] = [0]
                            else:
                                result = self.csv.getLatestPosition("tag")
                                data = [{
                                    "id": int(result["id"].iloc[0]+1),
                                    "tag": tag
                                }]
                                self.csv.insert("tag", data)
                                if data[0]["id"] not in post[xph]:
                                    post[xph].append(int(data[0]["id"]))
                        else:
                            if int(result_set["id"].iloc[0]) not in post[xph]:
                                post[xph].append(int(result_set["id"].iloc[0]))
                case "category":
                    post[xph] = list()
                    match int(post["model"]):
                        case 4:
                            for category in temp:
                                categories = category.text_content().strip().split("|")
                                for key, value in enumerate(categories):
                                    data = list()
                                    categories[key] = value.replace("\n", "").replace(" ", "")
                                    category = categories[key]

                                    result_set = self.csv.search("category", "category", category)
                                    if result_set is None:
                                        if len(self.csv.read("category")) == 0:
                                            data.append({ "id": 0, "category": category })
                                            self.csv.write("category", data)
                                            post[xph].append(0)
                                        else:
                                            result = self.csv.getLatestPosition("category")
                                            data = [{
                                                "id": int(result["id"].iloc[0]+1),
                                                "category": category
                                            }]
                                            self.csv.insert("category", data)
                                            if int(data[0]["id"]) not in post[xph]:
                                                post[xph].append(int(data[0]["id"]))
                                    else:
                                        result_set = int(result_set["id"].iloc[0])
                                        if result_set not in post[xph]:
                                            post[xph].append(result_set)
                        case _:
                            for category in temp:
                                url_categ = tuple(category.get("href").split('/'))
                                for key, param in enumerate(url_categ):
                                    if 'categ' in str(param):
                                        url_categ = url_categ[key+1:-1]
                                i = 0
                                while i < sum(1 for _ in url_categ):
                                    if url_categ[i]:
                                        result_set = self.csv.search("category", "category", url_categ[i])
                                        if result_set is None:
                                            if len(self.csv.read("category")) == 0:
                                                data = list()
                                                data.append({"id": 0, "category": url_categ[i]})
                                                self.csv.write("category", data)
                                                post[xph].append(data[0]["id"])
                                            else:
                                                result = self.csv.getLatestPosition("category")
                                                data = [{
                                                    "id": int(result["id"].iloc[0]+1),
                                                    "category": url_categ[i]
                                                }]
                                                self.csv.insert("category", data)
                                                if data[0]["id"] not in post[xph]:
                                                    post[xph].append(data[0]["id"])
                                        else:
                                            post[xph].append(int(result_set["id"].iloc[0]))
                                    i += 1
        slug = post["slug"]
        del post["slug"]
        del post["model"]
        if self.json.read("post") is None:
            self.json.write("text", {slug: post["text"]})
            del post["text"]
            self.json.write("post", {slug: post})
        else:
            file_exist = self.json.search_key("text", slug)
            if file_exist == False:
                self.json.insert("text", {slug: post["text"]})
            del post["text"]
            if self.json.search_key("post", slug) == False:
                self.json.insert("post", {slug: post})
            
