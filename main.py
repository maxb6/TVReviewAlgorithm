# COMP472 - Assignment 2
# Programmed By:
# Constantine Karellas - 40109253
# Max Burah - 40077075

from matplotlib.pyplot import cla
import pandas as pd
import requests
import string
import re
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

episodes = []
episodeData = soup.findAll('div', attrs={'class': 'list_item'})

print("Program Start \n\n")

for i in episodeData:
    season = i.div.a.text.replace('\n', '')
    print(season)
    episodeTitle = soup.strong.extract()
    name = episodeTitle.text.replace('\n', '')
    print(name)
    rating = i.find('div', class_ = 'ipl-rating-star small').text.replace('\n', '')
    print(rating[:-7])
    date = i.find('div', class_ = 'airdate').text.replace(' ', '').replace('\n', '')
    print(date)
    print("\n")


######### Extract the Data and Build the Model  ###########
# Using words for tokens in this model
# Method to count word frequency for a review
def wordFrequency(paragraph):
    wordList = paragraph.split()
    wordFreq = []
    for w in wordList:
        wordFreq.append(wordList.count(w))
    print("Review:\n" + paragraph)
    print("List:\n" + str(wordList) + "\n")
    print("Frequencies:\n" + str(wordFreq) + "\n")
    print("Pairs:\n" + str(list(zip(wordList, wordFreq))))


def wordFrequency1(wordList):
    wordFreq = []
    for w in wordList:
        wordFreq.append(wordList.count(w))
    print("List:\n" + str(wordList) + "\n")
    print("Frequencies:\n" + str(wordFreq) + "\n")
    print("Pairs:\n" + str(list(zip(wordList, wordFreq))))


# method to remove stopwords from a given paragraph

def removeStopwords(paragraph, stopwords):
    wordList = paragraph.split()
    resultWords = [word for word in wordList if word not in stopwords]
    result = ' '.join(resultWords)
    return result


# Read the stopword file into a stopWordList
stopWordFile = open("Stopword_File.txt", "r")
stopWordList = stopWordFile.read()
stopWordFile.close()
print(stopWordList)
print("\n\n")

# Extract the review data given a review URL of an episode
url1 = 'https://www.imdb.com/title/tt0098286/reviews/?ref_=tt_ql_urv'
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.content, 'html.parser')
# lister-item-content can be used to find review ratings
reviewData = soup1.findAll('div', attrs={'class': 'content'})
# iterate through all reviews of the season, clean the string and count the word frequency for each word

rate =[]

for i in reviewData:
    review = i.div.text
    review = review.lower()
    # find word count
    wordCount = len(review.split())
    print(wordCount)
    # clean review by inserting <s>
    cleanReview = review.replace(".", " <s>")
    cleanReview = "<s> " + cleanReview
    finalReview = removeStopwords(cleanReview, stopWordList)
    wordFrequency(finalReview)

print("\nProgram Terminated.\n")




