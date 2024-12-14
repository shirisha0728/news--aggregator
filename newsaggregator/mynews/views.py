from django.shortcuts import render
from mynews.models import Article,Feed


import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from mynews.models import Headline

# Create your views here.
#view for scraping new
def scrape(request, name):
    Headline.objects.all().delete() #remove all existing records from table
    session = requests.Session()
    #useragent helps server to identify origin of request
    #we are imitating request as google bot
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    #google bot is crawler program
    #session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    url = f"https://www.theonion.com/{name}"
    content = session.get(url).content
    #print(content)#raw content
    soup = BSoup(content, "html.parser")
    #print(soup)
    # finding all new div using common class
    News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})
    print(News)
    for article in News:
    #extracting news link,img url,title for each news
        main = article.find_all("a", href=True)
        linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        link = linkx["href"]
        titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
        title = titlex.text
        imgx = article.find("img")["data-src"]
        #storing extracted data to model
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.save()
        #saving details to table
    return redirect("/news")


def news_list(request):
    #fetching records stored in Headline model
    headlines = Headline.objects.all()[::-1]#store records in reverse order
    #to generate current url
    current_url = request.build_absolute_uri()
    #pass current url to template through context
    context = {
        "object_list": headlines,"currenturl":current_url
    }
    return render(request, "index.html", context )

def articles_list(request):

    articles = Article.objects.all()

    rows = [articles[x:x+1] for x in range(0, len(articles), 1)]

    return render(request, 'articles_list.html', {'rows': rows})

