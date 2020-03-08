from requests.compat import quote_plus 
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests

from . import models



BASE_CRAIGSLIST_URL = 'https://montreal.craigslist.org/search/sss?query={}&sort=rel&lang=en&cc=us'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    # puling data out of search bar
    search = request.POST.get('search')
    # Creating a search object from user's entry and storing in the admin's DB. SEXY!!!
    models.Search.objects.create(search=search)
    # Combining BASE_CRAIGSLIST_URL with input from user
    # quote_plus -> Combines the user input into one string
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get('https://montreal.craigslist.org/search/bbb?query=tutor&sort=rel&lang=en&cc=us')
    data = response.text
    soup = BeautifulSoup(data)
    result_listings = soup.findAll('li', class_='result-row')
    post_titles = result_listings.findAll('a', class_='result-title hdrlnk')
    post_date = result_listings.findAll('time',class_='result-date')
    post_hood = result_listings.findAll('span', class_='result-hood')
    print(post_titles[0].text)
    print(post_date[0].text)
    print(post_hood[0].text.strip())
    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
