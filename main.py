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
print("\n\n")


def extractReviewData(reviewURL):
    # Extract the review data given a review URL of an episode
    response1 = requests.get(reviewURL)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    # lister-item-content can be used to find review ratings
    reviewData = soup1.findAll('div', attrs={'class': 'content'})
    # iterate through all reviews of the season, clean the string and count the word frequency for each word

    rate = []

    for j in reviewData:
        review = j.div.text
        review = review.lower()
        # find word count
        wordCount = len(review.split())
        print(wordCount)
        # clean review by inserting <s>
        cleanReview = review.replace(".", " <s>")
        cleanReview = "<s> " + cleanReview
        finalReview = removeStopwords(cleanReview, stopWordList)
        wordFrequency(finalReview)


url = 'https://www.imdb.com/title/tt0098904/episodes?season=1&ref_=ttep_ep_sn_pv'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

episodeData = soup.findAll('div', attrs={'class': 'list_item'})

seasonEpisodeNum = []
episodeName = []
episodeRating = []
episodeDate = []
episodeLink = []
reviewLink = []

print("Program Start: \n\n")

# Webscraping 
for i in episodeData:
    # Webscraping the episode number and season number
    season_episode = i.div.a.text.replace('\n', '')
    seasonEpisodeNum.append(season_episode)
    print("Season and Episode Number:" + str(season_episode))
    # Webscraping the episode title
    episodeTitle = soup.strong.extract()
    name = episodeTitle.text.replace('\n', '')
    episodeName.append(name)
    print("Episode Title: " + str(name))
    # Webscraping the episode rating
    rating = i.find('div', class_='ipl-rating-star small').text.replace('\n', '')
    episodeRating.append(rating[:-7])
    print("Episode Rating: " + str(rating[:-7]))
    # Webscraping the episode date
    date = i.find('div', class_='airdate').text.replace(' ', '').replace('\n', '').replace('.', '')
    episodeDate.append(date[-4:])
    print("Episode Date of Release: " + str(date[-4:]))
    # pageLink = soup.strong.extract()
    # if pageLink.has_attr('href'):
    episodeLink = i.find('a').get('href')
    urlOfEpisode = 'https://www.imdb.com' + str(episodeLink)
    urlOfReview = str(urlOfEpisode) + "reviews?ref_=tt_ov_rt"
    print("Review Link: " + str(urlOfEpisode) + "reviews?ref_=tt_ov_rt")
    extractReviewData(urlOfReview)


# Building DataFrame
season_DF = pd.DataFrame(
    {'Name': episodeName, 'Season': seasonEpisodeNum, 'Rating': episodeRating, 'Year': episodeDate})
print(season_DF)
print("\n\n")

print("\nProgram Terminated.\n")
