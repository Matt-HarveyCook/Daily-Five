# requires this for install: pip install newsapi-python
# from newsapi.newsapi_client import NewsApiClient

# requires this for install: pip install beautifulsoup4
from bs4 import BeautifulSoup

from json import JSONEncoder

# may require this for install: pip install requests
import requests

import random
import re
import base64
import os
from dotenv import load_dotenv
load_dotenv()

class Category():
    def __init__(self, name, articles):
        self.name = name
        self.articles = articles

class Category_Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Request:
    def __init__(self) -> None:
        pass

    def select_category(self, category, baseRequest, apiKey, everythingOrTop, domains = ""):
        finalRequest = ""
        match category:
            case "politics":
                q = "q=politics OR budget OR government"
                finalRequest = baseRequest + everythingOrTop + q + "&" + domains + "&" + apiKey
            case "environment":
                q = "q=climate OR environment OR (global AND warming)"
                finalRequest = baseRequest + everythingOrTop + q + "&" + domains + "&" + apiKey
            case "general":
                q = "q=breaking OR headline"
                finalRequest = baseRequest + everythingOrTop + q + "&" + domains + "&" + apiKey
            case "technology":
                q = "q=tech OR AI OR (artificial AND intelligence) OR iphone OR app"
                finalRequest = baseRequest + everythingOrTop + q + "&" + domains + "&" + apiKey
            case "sports":
                q = "q=football OR basketball OR sports OR sport OR athlete OR fitness OR exercise"
                finalRequest = baseRequest + everythingOrTop + q + "&" + domains + "&" + apiKey

        return finalRequest
    
    def api_request(self, request):
        response = requests.get(request)
        content = response.json()

        articles = content["articles"]

        sampled_articles = random.sample(articles, 5)
        print(len(sampled_articles))

        return sampled_articles
    
    def decode_url(self, articles):
        count = 0
        while count < 10:
            for article in articles:
                url = article["url"]
                if "news.google" in url:

                    coded = url.split("/")
                    coded = coded[-1]
                    coded = re.split('[^a-zA-Z0-9]', coded)[0]

                    while len(coded)%4 != 0:
                        coded = coded +"="

                    url = str(base64.b64decode(coded))
                    httpIndex = url.find("https")
                    htmlIndex = url.find(".html")
                    url = url[httpIndex:-1]

                    if "xd2\\\\x01\\\\x00" in url:
                        url = url.split("xd2\\\\x01\\\\x00")[0]
                    elif "\\xd2\\x01" in url:
                        url = url.split("\\xd2\\x01")[0]
                    
                    article["url"] = url
            count += 1

        del articles[5:]
        return articles
    
    def clean_article_data(self, articles):
        tempArticleList = []
        validSites = ["BBC News", "independent", "sky", "thesun", "CNN", "reuters", "espn", "usatoday", "mirror", "telegraph", "metro", "thetimes", "Wired", "dailymail"]

        for article in articles:
            if article["url"] in validSites:
                tempArticleList.append(article)
            # for i in validSites:
            #     if i in article["url"] and len(tempArticleList) < 6:
            #         tempArticleList.append(article)
                    
                    # validSites.remove(i)  
                    # USE THIS LINE TO ENSURE UNIQUE LIST OF SITES
        
        return tempArticleList
    
    def query_article_data(self, articles):
        final_articles = []

        for article in articles:
            url = article["url"]

            # Metro url is a different form so this fixes that
            if "metro" in url:
                domain = "metro"

            else:
                domain = url.split(".")[1]

            r = requests.get(url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            content=""

            match domain:
                case "bbc":
                    for para in soup.find_all("p"):
                        attrList = para.parent.attrs.get("class")
                        if(attrList!=None):
                            for i in attrList:
                                if "RichTextContainer" in i:
                                    content += para.get_text()

                case "independent":
                    for para in soup.find_all("p"):
                        if para.parent.attrs.get("id") == "main":
                            content += para.get_text()
                case "metro":
                    for para in soup.find_all("p"):                
                        if para.parent.attrs.get("class")[0] == "article-body"  and para.get_text() != "NEWS... BUT NOT AS YOU KNOW IT":
                                content += para.get_text()

                case "telegraph":
                    for para in soup.find_all("p"):
                        if "articleBodyText" in para.parent.parent.attrs.get("class")[0]:
                            content += para.get_text()

                case  "cnn" | "usatoday"| "espn" | "sky" | "reuters" | "mirror" | "thetimes" | "wired" | "dailymail" | "skysports"| "time"|"businessinsider"|"bleacherreports":
                    for para in soup("p"):
                        if para.parent.attrs.get("class") != None:
                            if para.parent.attrs.get("class")[0] == "article__content"  :
                                content += para.get_text()
                            if para.parent.attrs.get("class")[0] == "article-body"  :
                                content += para.get_text()
                            if "article-body" in para.parent.attrs.get("class")[0]:
                                content += para.get_text()
                            if para.parent.attrs.get("class")[0] == "story"  :
                                content += para.get_text()
                            if "responsive__BodyContainer" in para.parent.attrs.get("class")[0]:
                                content += para.get_text()
                            if "body__inner-container" in para.parent.attrs.get("class")[0]:
                                content += para.get_text()
                            if "article" in para.parent.parent.attrs.get("class")[0]:
                                content += para.get_text()
                            if "content-lock" in para.parent.attrs.get("class")[0]:
                                content += para.get_text()
                            if "ol" in para.parent.nodeName():
                                content += para.get_text()
                case _: # Default case
                    for para in soup.find_all("p"):
                        content += para.get_text()

            if content != "":
                sentences = content.split(".")
                sentences[0] = (sentences[0].strip()).replace("\n", "")
                sentences[1] = (sentences[1].strip()).replace("\n", "")
                content = sentences[0] + ". " + sentences[1] + "."
                final_articles.append([article["title"], content, article["url"]])

            else:
                print("sorry couldnt find content ",str([article["url"]]))

        return final_articles
            

class Article:
    def __init__(self, title, content, link):
        self.title = title
        self.content = content
        self.link = link

class Article_Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__



rq = Request()


# choose between: environment, politics, technology, general, sports
    
# Used to perform the request to the API
# response = requests.get(finalRequest)
# content = response.json()

# Decodes the original URL from google news links
# articles = content["articles"]

# Main function for extracting the first 2 sentences from a news article
        
# final_articles = []
# tempArticleList = []

# List of all possible sites to access from   


# Final content is stored in final_articles
# 2D array with each nested array containing 3 elements: title, content and url
# example form: final_articles = [["title", "content", "url"],[...]]
# Use the block below to display content

# for i in final_articles:
#     article = Article(i[0], i[1], i[2])
#     article_objects.append(article)
#     # print("\nthis is the title: \n",str(i[0]))
#     # print("\nthis is the content \n",str(i[1]))
#     # print("\nthis is the url \n",str(i[2]))
    

    