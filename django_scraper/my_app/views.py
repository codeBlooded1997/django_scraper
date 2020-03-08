from requests.compat import quote_plus 
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests

from . import models


BASE_CRAIGSLIST_URL = 'https://montreal.craigslist.org/search/sss?query={}'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    # pulling data out of search bar
    search = request.POST.get('search')
    # Creating a search object from user's entry and storing in the admin's DB. SEXY!!!
    models.Search.objects.create(search=search)
    # Combining BASE_CRAIGSLIST_URL with input from user
    # quote_plus -> Combines the user input into one string
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    post_listings = soup.findAll('li', class_='result-row')

    final_postings = []

    for post in post_listings:
        post_title = post.find('a', class_='result-title hdrlnk').text
        post_url = post.find('a', class_='result-title hdrlnk')['href']
        post_date = post.find('time',class_='result-date').text
        if post.find('span', class_='result-price'):
            post_price = post.find('span', class_='result-price').text.strip()
        else:
            post_price = 'N/A'

        if post.find('span', class_='result-hood'):
            post_hood = post.find('span', class_='result-hood').text.strip()
        else:
            post_hood = 'N/A'

        final_postings.append((post_date, post_title, post_hood, post_price, post_url))

    quantity = len(final_postings)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
        'quantity': quantity,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
