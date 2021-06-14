# COMP472 - Assignment 2
# Programmed By:
# Constantine Karellas - 40109253
# Max Burah - 40077075

from matplotlib.pyplot import cla
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np


class Episode:
    def __init__(self, name, season, reviewLink, year):
        self.name = name
        self.season = season
        self.reviewLink = reviewLink
        self.year = year

    def printEpisode(self):
        print(self.name, " ", self.season, " ", self.reviewLink, " ", self.year)




url = 'https://www.imdb.com/title/tt0098904/episodes?season=1&ref_=ttep_ep_sn_pv'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

episodes=[]
episodeData = soup.findAll('div', attrs={'class': 'list_item'})

for i in episodeData:
    season = i.div.a.text
    print(season)
    episodeTitle = soup.strong.extract()
    name = episodeTitle.text
    print(name)
    date = i.div.text
    print(date)







'''
episodeName = []
episodeSeason = []
rating = []
reviews = []
years = []

episodeData = soup.findAll('div', attrs={'class': 'list_item'})

for i in episodeData:
    episode = i.div.a.text.replace('\n', '')
    episodeSeason.append(episode)

    episodeTitle = soup.strong.extract()
    epName = episodeTitle.text
    episodeName.append(epName)

    # date = i.div.find('div', class_ = 'airdate').text
    # years.append(date)

print(episodeName)
print(episodeSeason)
print(years)
'''

print("\nProgram Terminated.\n")
