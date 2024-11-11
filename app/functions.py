from django.utils.text import slugify
from datetime import datetime
import uuid, re

def date_format(date):
    date = re.sub(r'[\r\n]+', ' ', date)
    date = re.sub(r'\s+', ' ', date)
    date = date.strip()
    
    mouths = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    if "/" not in str(date):
        date = date.split(" ")
        if len(date) == 3:
            mouth = date[1].lower().replace(",", "")
            mouth = mouth[:3]
            index = mouths.index(mouth)+1
            if len(str(date[0])) == 1:
                date[0] = f'0{date[0]}'
            if len(str(index)) == 1:
                return f"{date[0]}/0{index}/{date[-1]}"
            return f"{date[0]}/{index}/{date[-1]}"
        elif len(date) == 5:
            mouth = date[2].lower()
            mouth = mouth[:3]
            index = mouths.index(mouth)+1
            if len(str(date[0])) == 1:
                date[0] = f'0{date[0]}'
            if len(str(index)) == 1:
                return f"{date[0]}/0{index}/{date[-1]}"
            return f"{date[0]}/{index}/{date[-1]}"
    elif "h" in date:
        date = date.split(" ") 
        return date[-2]
    else:
        return date

def data_page(xpath, tree, model):
    elements = dict()
    posts = dict()

    elements.update({
        xph: tree.xpath(xpath[xph])
        for xph in xpath
    })

    if len(elements["title"]) > 0:
        elements_treaties = zip(
            [slugify(f"{get_slug(element.get('href'))}_{uuid.uuid4().hex[:8]}")
             for key, element in enumerate(elements['link'])],
            [str(element.text_content()).strip() for element in elements["title"]],
            [ element.get("href") if model != 4 else f"https://relatabahia.com.br/{element.get('href')}"
            for element in elements["link"]],
            [datetime.strptime(date_format(element.text_content().strip()), "%d/%m/%Y").date() 
             for element in elements['date']]
        )

        for data_post in tuple(elements_treaties):
            posts.update({str(data_post[0]):{
                'slug': str(data_post[0]),
                'model': model,
                'title': str(data_post[1]),
                'link': str(data_post[2]),
                'date': str(data_post[3]),
            }})
        return posts
    else: return None

def get_slug(url):
    url = url.split('/')
    if url[-1] != "":
        return url[-1]
    else:
        return url[-2]
