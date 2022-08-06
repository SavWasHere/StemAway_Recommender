import time, os, requests, bs4
import regex as re
import numpy as np
import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
"My complete webscraper"
"Example webpage https://forums.unrealengine.com/tags/c/community/marketplace/51/launcher"

PostDict= {}
PostDf= pd.DataFrame(columns= [
    'Post_Title',
    'Num_Views',
    'Num_Replies',
    'Leading_Post',
    'Tags',
    'Date_Created'
])

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--incognito')
driver= webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=opts)

#Link goes here
driver.get('https://forums.unrealengine.com/c/community/marketplace/51')

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

        print(f'New Height= {new_height}')

scroll(driver, 3)

soup_2 = BeautifulSoup(driver.page_source, 'lxml')

#Getting the title of the post
def getTitle(Topicsoup):
    soup= Topicsoup
    Title = soup.find('title')
    if Title is None:
        Title= 'No Title'
    else:
        Title= soup.find('title').text
    return Title

def getTags(Topicsoup):
    soup= Topicsoup
    Tags=[]
    TagsRes= PostSoup.find_all(class_='discourse-tag bullet')
    if len(TagsRes)==0:
        Tags='No Tags'
    else:
        for tag in TagsRes:
            Tags.append(tag.text)
    return Tags

#Getting the Leading post of the post
"""
cooked= everything in the html of the class 'cooked'. This typically host the post data
If the webpage doesn't load, cooked will be empty so I check if it is None. If it is then no post.
If it is not None, there is a post and I extract the text by taking all the p (paragraphs)
"""
def getLeadingPost(Topicsoup):
    LeadPost=[]
    cooked= PostSoup.find_all(class_='cooked')
    if cooked is None:
        LeadPost.append('0')
    else:
        for post in cooked:
            if isinstance(post, bs4.element.Tag):
                LeadText= post.find_all('p')
                for Lpost in LeadText:
                    LeadPost.append(Lpost.text)
    return LeadPost

#Getting the dates created
def getDateCreated(Topicsoup):
    DateCreated= Topicsoup.find(class_='relative-date')
    if DateCreated is None:
        DateCreated = str(0)
    else:
        DateCreated= Topicsoup.find(class_='relative-date').text
    return DateCreated

def getNum_Views(Topicsoup):
    SecViews= Topicsoup.find(class_='secondary views')
    if SecViews is None:
        Views= 0
    else:
        Views= SecViews.find(class_='number').text
    return Views

def getNum_Replies(Topicsoup):
    ClReplies= Topicsoup.find(class_='replies')
    if ClReplies is None:
        Replies= 0
    else:
        Replies= ClReplies.find(class_='number').text
    return Replies


Links= soup_2.find_all('a', class_='title raw-link raw-topic-link')

i=1
for index, link in enumerate(Links):
    linkTest= str(link['href']).split('/')
    if 'https:' in linkTest:
        url= link['href']
    else:
        url= 'https://forums.unrealengine.com'+link['href']
    print(i, ":", url)
    i +=1
    driver.get(url)
    PostHtml= driver.page_source
    PostSoup= BeautifulSoup(PostHtml, 'html.parser')
    
    #Getting the Data
    Title= getTitle(PostSoup)
    Leading_Post= getLeadingPost(PostSoup)
    Tags= getTags(PostSoup)
    DateCreated= getDateCreated(PostSoup)
    numViews= getNum_Views(PostSoup)
    numReplies= getNum_Replies(PostSoup)

    attributeDict= {
        'Post_Title': Title,
        'Leading_Post': Leading_Post,
        'Date_Created': DateCreated,
        'Num_Views': numViews,
        'Num_Replies': numReplies,
        'Tags': Tags,
        'Link': link
    }
    print(Title)

    PostDict[Title]= attributeDict
    PostDf= PostDf.append(attributeDict, ignore_index= True)    

timeStamp = datetime.now().strftime('%Y%m%d')

author= 'SavP'

SiteName= 'UEMarkeplace'

#Setting up csv file
"Please put your name here"
csvFilename = author + SiteName + '_SCRAPED_DATA' + timeStamp + '.csv'
csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath('C:\\Users\\savan\\Desktop\\Coding and Software\\Stemaway Coding Stuff\\ClasslessWebScraper.py')), csvFilename)
# Save dataframe into csv file
PostDf.to_csv(csvFileFullPath)
