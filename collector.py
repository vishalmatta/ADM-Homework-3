from bs4 import BeautifulSoup
import requests, csv, re, time, random
from collections import defaultdict
import numpy as np
import pandas as pd


def generate_html():
    movie_list = []
    # here is a list of urls we want to parse !!!
    urls = ['https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html',
            'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html',
            'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies3.html', ]
    for url in urls:
        response_page = requests.get(url)
        soup = BeautifulSoup(response_page.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            movie_list.append(link['href'])

    for movie in range(30000):  # here we want to save html pages.
        response_page = requests.get(movie_list[movie])
        if int(response_page.status_code) == 200:
            # response_page = requests.get(movie_list[movie])
            time.sleep(random.randint(1, 5))
        elif int(response_page.status_code) == 429:
            time.sleep(1200)

        soup = BeautifulSoup(response_page.text, 'html.parser')
        # here we define the movie file_name
        name = "article-{0}.html".format(movie)
        # here we get the movie link
        movie_link = movie_list[movie]
        page = str(soup)
        with open(name, 'a') as f:
            f.write(page)
            # here we add an anchor tag with our beloved group name @ the end of the file
            f.write(f'<a class="group-21" href="{movie_link}" title="{movie_link}">{movie_link}</a>')

generate_html()


