#!/usr/bin/env python3
#import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import sqlite3

# Returns an array of dictionaries. Each Dict is a {link, verb, definition})
def scrapeVerbs():
    verbs = []
    # user-agent definition
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"}
    pageRequest = Request("https://www.lawlessfrench.com/verb-conjugations/", headers = headers)
    page = urlopen(pageRequest)
    
    # parse with beautiful soup
    htmlContent = BeautifulSoup(page, 'html.parser')
    content = htmlContent.find_all('div', attrs={'class':'azindex'})[0]
    aList = content.find_all("a")

    for element in aList:
        if element['href'] != "#azindex-1":
            # Text in format: Zoner - to zone, divide into zones; (familiar) to wander, bum around  within the <span> within the <a> 
            contents = element.contents[0].contents[0]
            index = contents.find("-")
            word = contents[:index - 1]
            definition = contents[index + 2:]
            verbs.append({'link': element['href'], 'word': word, 'definition': definition})
    #print(verbs)
    return verbs

def scrapeConjugations():
    verbConjugations = {}
    verbList = scrapeVerbs()
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"}
    pageRequest = Request(verbList[0]["link"], headers = headers)
    page = urlopen(pageRequest)

    # parse with beautiful soup
    htmlContent = BeautifulSoup(page, 'html.parser')
    content = htmlContent.find_all('tr')
    #print(content)
    # Just using the first word in the list for now
    word = verbList[0]["word"]
    verbConjugations[word] = {} # add the word as a key
    for i in range(len(content)):
        # first and seventh row are headers
        if i == 0 or i == 7:
            # gets the header, type of conjugation
            headerRow = content[i].find_all('a') 
            for j in range(len(headerRow)):
                verbTense = headerRow[j].contents[0]
                # add the header as a key and an empty array as the value to hold conjugations later
                # {"Abaisser": {"Present": [ abaisse, abaisses, abaisse, abaissons, abaissent, abaisse], "Imperfect": [] }}
                verbConjugations[word][verbTense] = []
    print(verbConjugations)

    #for dictionary in verbs:
        # go to the link and scrape conjugations

scrapeConjugations()
