from django.urls import path
from mynews.views import scrape, news_list,articles_list
urlpatterns = [
  path('scrape/<str:name>', scrape, name="scrape"),
  path('news/', news_list, name="news_list"),
  path('', articles_list, name="articles_list"),
]