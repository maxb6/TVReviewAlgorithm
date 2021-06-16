# COMP472 - Assignment 2 - Summer 2021
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


class Review:
    def __init__(self, title, review, reviewRating, isPositive):
        self.title = title
        self.review = review
        self.reviewRating = reviewRating
        self.isPositive = isPositive

    def printReview(self):
        print(self.title, " ", self.review, " ", self.reviewRating, " ", self.isPositive)


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

positiveWords = []
negativeWords = []
FreqPositiveWords = []
FreqNegativeWords = []

titleReview = []
ratingReview = []

def extractReviewData(reviewURL):
    # Extract the review data given a review URL of an episode
    response1 = requests.get(reviewURL)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    # lister-item-content can be used to find review ratings
    reviewData = soup1.findAll('div', attrs={'class': 'lister-item-content'})

    # before entering the loop, create empty wordLists and wordFrequencies for positive and negative reviews
    posWordList = []
    posWordFreq = []
    posWordCount = 0
    negWordList = []
    negWordFreq = []
    negWordCount = 0

    # iterate through all reviews of the season, clean the string and count the word frequency for each word
    for j in reviewData:
        r = Review(None, None, None, None)
        # Find review rating, only consider reviews that have a rating
        if j.find('div', class_='ipl-ratings-bar') is not None:
            reviewRating = j.find('div', class_='ipl-ratings-bar').text.replace('\n', '')
            if len(reviewRating) == 5:
                r.reviewRating = int(reviewRating[0:2])
            else:
                r.reviewRating = int(reviewRating[0:1])

            print("rating scale: " + str(r.reviewRating))

            # Assign positive or negative review status
            if r.reviewRating >= 8:
                r.isPositive = True
                ratingReview.append(r.isPositive)
            else:
                r.isPositive = False
                ratingReview.append(r.isPositive)
            print("Is the review Positive? " + str(r.isPositive))

            # get the review Title
            r.title = j.find('a', class_='title').text.replace('\n', '')
            titleReview.append(r.title)
            print("Review Title: ", r.title)

            # get the actual review
            r.review = j.find('div', class_='content').div.text.lower()
            print("Review text: ", r.review)

            # find word count
            wordCount = len(r.review.split())
            # print(wordCount)
            # clean review by inserting <s>
            r.review.replace(".", " <s> ")
            r.review.replace("(", " ")
            r.review.replace(")", " ")
            r.review = "<s> " + r.review
            r.review = removeStopwords(r.review, stopWordList)

            # check if review is positive or negative and place in corresponding list
            if r.isPositive:
                posWordList.append(r.review.split())
                positiveWords.append(r.review.split())
                for w in posWordList:
                    posWordFreq.append(posWordList.count(w))
                    FreqPositiveWords.append(posWordList.count(w))
                # print("Review:\n" + r.review)
                # print("Positive Word List:\n" + str(posWordList) + "\n")
                posWordCount += wordCount

            else:
                negWordList.append(r.review.split())
                negativeWords.append(r.review.split())
                for w in negWordList:
                    negWordFreq.append(negWordList.count(w))
                    FreqNegativeWords.append(negWordList.count(w))
                # print("Review:\n" + r.review)
                # print("Negative Word List:\n" + str(negWordList) + "\n")
                negWordCount += wordCount

    # we have obtained a list of all negative words and all positive words plus their respective counts
    print("Positive Word Count:\n" + str(posWordCount))
    print("Positive Word List:\n" + str(posWordList) + "\n")
    print("Negative Word Count:\n" + str(negWordCount))
    print("Negative Word List:\n" + str(negWordList) + "\n")

def wordFrequForPos(str):
    counter = 1
    for i in positiveWords:
        if str == i:
            counter += 1
    return counter

def wordFrequForNeg(str):
    counter = 1
    for j in negativeWords:
        if str == j:
            counter += 1
    return counter

def condProbabilityPos(str):
    proability = wordFrequForPos(str) / len(positiveWords)
    return proability

def condProbabilityNeg(str):
    proability = wordFrequForNeg(str) / len(negativeWords)
    return proability

seasonEpisodeNum = []
episodeName = []
episodeRating = []
episodeDate = []
episodeLink = []
reviewLink = []


url1 = 'https://www.imdb.com/title/tt0098904/episodes?season=1&ref_=ttep_ep_sn_pv'
response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.content, 'html.parser')
episodeData1 = soup1.findAll('div', attrs={'class': 'list_item'})

print("Program Start: \n\n")

# Webscraping for Season 1
for i in episodeData1:
    # Webscraping the episode number and season number
    season_episode = i.div.a.text.replace('\n', '')
    seasonEpisodeNum.append(season_episode)
    print("Season and Episode Number:" + str(season_episode))
    # Webscraping the episode title
    episodeTitle = soup1.strong.extract()
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
    reviewLink.append(urlOfReview)
    print("Review Link: " + str(urlOfReview))
    extractReviewData(urlOfReview)
    print("\n")

url2 = 'https://www.imdb.com/title/tt0098904/episodes?season=2'
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.content, 'html.parser')
episodeData2 = soup2.findAll('div', attrs={'class': 'list_item'})

# Webscraping for Season 2
for i in episodeData2:
    # Webscraping the episode number and season number
    season_episode = i.div.a.text.replace('\n', '')
    seasonEpisodeNum.append(season_episode)
    print("Season and Episode Number:" + str(season_episode))
    # Webscraping the episode title
    episodeTitle = soup2.strong.extract()
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
    reviewLink.append(urlOfReview)
    print("Review Link: " + str(urlOfReview))
    extractReviewData(urlOfReview)
    print("\n")

url3 = 'https://www.imdb.com/title/tt0098904/episodes?season=3'
response3 = requests.get(url3)
soup3 = BeautifulSoup(response3.content, 'html.parser')
episodeData3 = soup3.findAll('div', attrs={'class': 'list_item'})

# Webscraping for Season 3
for i in episodeData3:
    # Webscraping the episode number and season number
    season_episode = i.div.a.text.replace('\n', '')
    seasonEpisodeNum.append(season_episode)
    print("Season and Episode Number:" + str(season_episode))
    # Webscraping the episode title
    episodeTitle = soup3.strong.extract()
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
    reviewLink.append(urlOfReview)
    print("Review Link: " + str(urlOfReview))
    extractReviewData(urlOfReview)
    print("\n")


# Building DataFrame
print("\n\n")
season_DF = pd.DataFrame(
    {'Name': episodeName, 'Season': seasonEpisodeNum, 'Review Link': reviewLink, 'Year': episodeDate})
print(season_DF)
print("\n\n")

# Putting Datafram into data.csv file
season_DF.to_csv('data.csv', sep = '|', encoding='utf-8')

# Creating the Model and Calculating Probabilities
#wordList = []
#wordList = positiveWords.extend(negativeWords)

#print(FreqPositiveWords)
#print(FreqNegativeWords)

# Writing to model.txt
count1 = 1
modelFile = open("model.txt", 'w')
for i in positiveWords:
    for j in i:
        modelFile.write("No." + str(count1) +"  "+ str(j.replace('.','').replace(',','').replace('"','')) + "\n")
        modelFile.write(str(wordFrequForPos(j)) + ", " + str(condProbabilityPos(j)) + ", " + str(wordFrequForNeg(j)) + ", " + str(condProbabilityNeg(j)) + "\n\n")
        count1 += 1

for i in negativeWords:
    for j in i:
        modelFile.write("No." + str(count1) +"  "+ str(j.replace('.','').replace(',','').replace('"','')) + "\n")
        modelFile.write(str(wordFrequForPos(j)) + ", " + str(condProbabilityPos(j)) + ", " + str(wordFrequForNeg(j)) + ", " + str(condProbabilityNeg(j)) + "\n\n")
        count1 += 1


# Creating result.txt file
resultFile = open("result.txt", "w")

'''
for n, i in enumerate(ratingReview):
    if i == True:
        ratingReview[n] == "Positive"
    else:
        ratingReview[n] == "Negative"
'''
count2 = 1
for i in titleReview:
    resultFile.write("No." + str(count2) +"  "+ str(i) + "\n")
    resultFile.write(" , " + " , " + " , " + " , " + "\n\n")
    count2 += 1



print("\nProgram Terminated.\n")
