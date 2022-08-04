import time
import os
import requests
import regex as re
import numpy as np
import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

"""
My complete webscraper
Example webpage https://forums.unrealengine.com/tags/c/community/marketplace/51/launcher
"""

#Setting up storage for the csv and showing the data we want to collect
PostDict= {}
#Q- Why use pandas DataFrame?
#A- It stores the data in the csv in columns designated by the columns here, making it easy to read
# Check csv file provided to see how it looks
PostDf= pd.DataFrame(columns= [
    'Post_Title',
    'Num_Views',
    'Num_Replies',
    'Leading_Post',
    'Tags',
    'Date_Created'
])

#Setting up driver DO NOT CHANGE UNLESS YOU HAVE TO ADD AN ARGUMENT
#Ensure your driver is in the same file as your webscraper
opts = Options()
opts.add_argument('--headless')
opts.add_argument('--incognito')
driver= webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=opts)

#Link goes here
"""
When putting your link, I recommend going into the category and pasting the link here since this webscraper gathers
data on all the posts. To make it easy and save time and processing, I ask that you go to forums.unrealengine.com 
and go to your desired category to scrape and get that link rather than just using forums.unrealengine.com
"""
BaseLink='https://forums.unrealengine.com/tags/c/community/marketplace/51/launcher'
driver.get(BaseLink)

#Scrolls to the bottom of the webpage

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

#Gets the BeautifulSoup object of the webpage's HTML
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

#Gets the tag in the post
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

#Getting the Leading post of the Topic
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

#Gets the number of views
def getNum_Views(Topicsoup):
    SecViews= Topicsoup.find(class_='secondary views')
    if SecViews is None:
        Views= 0
    else:
        Views= SecViews.find(class_='number').text
    return Views

#Gets the number of replies
def getNum_Replies(Topicsoup):
    ClReplies= Topicsoup.find(class_='replies')
    if ClReplies is None:
        Replies= 0
    else:
        Replies= ClReplies.find(class_='number').text
    return Replies

#Gets all the links
Links= soup_2.find_all('a', class_='title raw-link raw-topic-link')

i=1
#Running the webscraper and Saving
"""
This for loop here is central to running the webscraper.
This block looks at the links found in the page, then 'clicks' into them.
When in the link it gets the HTML of the link and gathers the data we want (title, post, views, replies, tags, date)
It then adds all that data to a dictionary and adds it to the one we set up before.
That dictionary we had before will then be used to create a new csv with all the date we got
"""
for index, link in enumerate(Links):
    #Tests the link to see if it is whole or partial. Some posts come with 'https:' and some only come with '/t/topic'
    linkTest= str(link['href']).split('/')
    if 'https:' in linkTest:
        url= link['href']
    else:
        url= 'https://forums.unrealengine.com'+link['href']
    print(i, ":", url)
    i +=1
    #Getting page data from post link
    driver.get(url)
    PostHtml= driver.page_source
    PostSoup= BeautifulSoup(PostHtml, 'html.parser')
    
    #Getting the Data from the post link
    Title= getTitle(PostSoup)
    Leading_Post= getLeadingPost(PostSoup)
    Tags= getTags(PostSoup)
    DateCreated= getDateCreated(PostSoup)
    numViews= getNum_Views(PostSoup)
    numReplies= getNum_Replies(PostSoup)

    attributeDict= {
        'Post_Title': Title,
        'Leading_Comment': Leading_Post,
        'Date_Created': DateCreated,
        'Num_Views': numViews,
        'Num_Replies': numReplies,
        'Tags': Tags,
        'Link': link['href']
    }
    print(Title)

    PostDict[Titsle]= attributeDict
    PostDf= PostDf.append(attributeDict, ignore_index= True)    

#Gets the current date and time the program was run
timeStamp = datetime.now().strftime('%Y%m%d')

#Please put your name in any format here. Ensure it is recognisable as yours
Author= 'SavP'

#Put the site and category here: such as UECommunity or UEMarketplace
SiteName= 'UEMarkeplace'

#Setting up csv file's name.
csvFilename = SiteName + '_SCRAPED_DATA' + timeStamp + '.csv'

#Change the path to the path on your computer. If you do not know how, feel free to ask in the discord
myPath= 'C:\\Users\\savan\\Desktop\\Coding and Software\\Stemaway Coding Stuff\\ClasslessWebScraper.py'
csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(myPath)), csvFilename)
# Save dataframe into csv file
PostDf.to_csv(csvFileFullPath)
