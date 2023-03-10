from django.urls import path

from .views import news_list
from .views import news_detail
from .views import HomePageView
from .views import TechNewsView
from .views import WorldNewsView
from .views import SportNewsView
from .views import NewsCreateView
from .views import NewsDeleteView
from .views import NewsUpdateView
from .views import ContactPageView
from .views import admin_page_view
from .views import EconomicNewsView
from .views import SearchResultsList


urlpatterns = [
    path('news/', news_list, name='all_news_list'),
    path('', HomePageView.as_view(), name='home_page'),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('tech-news/', TechNewsView.as_view(), name='tech_news_page'),
    path('news-create/', NewsCreateView.as_view(), name='news_create'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('world-news/', WorldNewsView.as_view(), name='world_news_page'),
    path('sport-news/', SportNewsView.as_view(), name='sport_news_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('economic-news/', EconomicNewsView.as_view(), name="economics_news_page"), # noqa
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_results'),
]
