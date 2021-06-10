# COMP472 - Assignment 2
# Programmed By:
# Constantine Karellas - 40109253
# Max Burah - 40077075

from matplotlib.pyplot import cla
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

url = 'https://www.imdb.com/title/tt0098904/episodes?season=1&ref_=ttep_ep_sn_pv'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

episodeName = []
episodeSeason = []
rating = []
reviewLink = []
year = []

episodeData = soup.findAll('div', attrs= {'class': 'list_item'})

for i in episodeData:
    episode = i.div.a.text.replace('\n','')
    episodeSeason.append(episode)

    episodeTitle = soup.strong.extract()
    name = episodeTitle.text
    episodeName.append(name)

    date = i.div.find('div', class_ = 'airdate').text
    year.append(date)

print(episodeName)
print(episodeSeason)
print(year)

print("\nProgram Terminated.\n")
