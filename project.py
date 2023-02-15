#Importing Libraries
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import cmudict
import re

#############################################################################################

#Converting Excel Sheet to Pandas DataFrame
df = pd.read_csv('Input.xlsx - Sheet1.csv')


URL = df.loc[:,"URL"]
#print(URL)
URL_ID = df.loc[:,"URL_ID"]
#print(URL_ID)

################################################################################################

# Create new columns in DataFrame
columns=[
    "POSITIVE SCORE",
    "NEGATIVE SCORE",
    "POLARITY SCORE",
    "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH",
    "PERCENTAGE OF COMPLEX WORDS",
    "FOG INDEX",
    "AVG NUMBER OF WORDS PER SENTENCE",
    "COMPLEX WORD COUNT",
    "WORD COUNT",
    "SYLLABLE PER WORD",
    "AVG SYLLABLE COUNT PER WORD",
    "PERSONAL PRONOUNS",
    "AVG WORD LENGTH"
]
for c in columns:
    df.insert(columns.index(c)+2 ,c, value=None)

# Print the DataFrame
#print(df)

################################################################################################

#Imported stopWords
import os

directory = "D:\project\StopWords"
text_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

stop_words = []
for filename in text_files:
    with open(os.path.join(directory, filename), "r", encoding="ISO-8859-1") as file:
        contents = file.read().replace("\n", " ")
    stop_words.append(contents)

#print(stop_words[0])
#print(type(stop_words))

#Tokenize stopwords
swords = word_tokenize(str(stop_words))
swords = text_without_symbols = [word for word in swords if word.isalpha()]
#print(swords)
#print(type(swords))

#####################################################################################################

#Imported positive-words.txt
filename = "positive-words.txt"
directory = "D:\project\MasterDictionary"

with open(os.path.join(directory, filename), "r", encoding="ISO-8859-1") as file:
    contents = file.read().replace("\n", " ")
positive_words = contents

#print(positive_words)
#print(type(positive_words))

#Tokenize positivewords
pwords = word_tokenize(str(positive_words))
#print(pwords)
#print(type(pwords))

#####################################################################################################

#Imported negative-words.txt
filename = "negative-words.txt"
directory = "D:\Internshala\MasterDictionary"
with open(os.path.join(directory, filename), "r", encoding="ISO-8859-1") as file:
    contents = file.read().replace("\n", " ")
negative_words = contents

#print(negative_words)
#print(type(negative_words))

#Tokenize negativewords
nwords = word_tokenize(str(negative_words))
#print(nwords)
#print(type(nwords))

######################################################################################################

for i in range(0,114):
    #Naming filename as URL_ID
    filename = str(URL_ID[i]) + ".txt"
    url = URL[i]
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    #Saving Title as string
    for header in soup.find_all('h1'):
        title = str(header.text)
    #Saving Article text as string
    article_text = ""
    for article in soup.find_all('p'):
        info = article.text
        article_text = article_text + " " + info
    #Appending Title and Article text
    complete = title + article_text
    #Creating file and saving complete article in file
    with open(filename, "w") as file:
        file.write(str(complete))
    
    ##########################################################################################

    #Imported text file
    with open(filename, "r") as file:
        contents = file.read()
    text = contents
    #print(type(text))
    
    ###########################################################################################

    #Tokenized the text to words
    words = word_tokenize(text)
    #Removed all symbols from text
    text_without_symbols = [word for word in words if word.isalpha()]
    #Tokens without stopwords
    cleaned_text = [x for x in text_without_symbols if x not in swords]
    #print(cleaned_text)

    ############################################################################################

    #Positive Score
    posscore = 0
    for x in cleaned_text:
       if x in pwords:
            posscore += 1
    #print(posscore)

    #############################################################################################

    #Negative Score
    negscore = 0
    for x in cleaned_text:
       if x in nwords:
            negscore += 1
    #print(negscore)

    ##############################################################################################

    #Polarity Score
    polarityscore = (posscore - negscore)/((posscore + negscore) + 0.000001)
    #print(polarityscore)

    ##############################################################################################
    
    #Subjectivity Score
    subscore = (posscore + negscore)/ (len(cleaned_text) + 0.000001)
    #print(subscore)

    ##############################################################################################
    
    #Tokenized the text to sentences
    sent = sent_tokenize(text)
    #print(sent)
    #print(len(sent))

    ##############################################################################################
    
    #Average Sentence Length = the number of words / the number of sentences
    avg_sent_length = len(text_without_symbols)/len(sent)
    #print(avg_sent_length)

    ##############################################################################################
    
    #Complex Words
    #nltk.download('cmudict')
    d = cmudict.dict()

    def count_syllables(word):
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
        except KeyError:
            return 0

    complex_words = []
    for word in cleaned_text:
        if count_syllables(word) > 2:
            complex_words.append(word)
    #print(complex_words)

    ##############################################################################################
    
    #Percentage of Complex words = the number of complex words / the number of words 
    percwords = len(complex_words)/len(cleaned_text)
    #print(percwords)

    ##############################################################################################
    
    #Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
    fogindex = 0.4*(avg_sent_length + percwords)
    #print(fogindex)

    ##############################################################################################
    
    #Average Number of Words Per Sentence = the total number of words / the total number of sentences
    avg_no_of_words_sent = len(text_without_symbols)/len(sent)
    #print(avg_no_of_words_sent)

    ##############################################################################################
    
    #Complex Word Count
    cwordcount = len(complex_words)
    #print(cwordcount)

    ##############################################################################################
    
    #Word Count
    wordcount = len(cleaned_text)
    #print(wordcount)

    ##############################################################################################
    
    #Syllable Count Per Word
    def count_syllables(word):
        vowels = "aeiouy"
        word = word.lower().strip(".:;?!")
        if word[-2:] == "ed" or word[-2:] == "es":
            word = word[:-2]
        if word[-1:] == "e":
            word = word[:-1]
        if word[-3:] == "ing":
            word = word[:-3]
        count = 0
        for index, char in enumerate(word):
            if char in vowels and (index == 0 or word[index-1] not in vowels):
                count += 1
        if word[-1] in vowels:
            count += 1
        return count

    def syllable_count_per_word(cleaned_text):
        syllable_counts = [count_syllables(word) for word in cleaned_text]
        return dict(zip(cleaned_text, syllable_counts))

    syllable_per_word = syllable_count_per_word(cleaned_text)
    #print(syllable_per_word)

    ##############################################################################################
    
    #Total Syllables
    def total_syllables(cleaned_text):
        syllable_counts = [count_syllables(word) for word in cleaned_text]
        total_syllable = sum(syllable_counts)
        return total_syllable

    total_syllable = total_syllables(cleaned_text)
    #print(total_syllable)


    #Average Syllable Count Per Word
    avg_syllable_count_per_word = total_syllable/len(cleaned_text)
    #print(avg_syllable_count_per_word)

    ##############################################################################################
    
    #Personal Pronouns
    def count_personal_pronouns(cleaned_text):
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for word in cleaned_text:
            if word in personal_pronouns:
                count += 1
            elif word == "US":
                count -= 1
        return count

    personal_pronouns = count_personal_pronouns(cleaned_text)
    if personal_pronouns < 0:
        personal_pronouns = 0
    #print(personal_pronouns)

    ##############################################################################################
    
    #Average Word Length = Sum of the total number of characters in each word/Total number of words
    def sum_of_characters(cleaned_text):
        total_sum = 0
        for word in cleaned_text:
            total_sum += len(word)
        return total_sum
    total_characters = sum_of_characters(cleaned_text)
    #print(total_characters)

    avg_word_length = total_characters/len(cleaned_text)
    #print(avg_word_length)

    ##############################################################################################
    
    # Add data to the DataFrame
    df.loc[i] = [URL_ID[i], URL[i], posscore, negscore, polarityscore, subscore, avg_sent_length, percwords, fogindex, avg_no_of_words_sent, cwordcount, wordcount, syllable_per_word, avg_syllable_count_per_word, personal_pronouns, avg_word_length]

    # Print the DataFrame
    #print(df)



####################################################################################################
#First five rows
print(df.head(5))

#Saving dataframe to excel file
df.to_excel('Output Data Structure.xlsx', index=False)
