"My complete webscraper"
"Example webpage https://forums.unrealengine.com/tags/c/community/marketplace/51/launcher"
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import requests, os, time
import pandas as pd
import numpy as np
import regex as re

"""
Class structure
init
main -> runScraper
runScraper -> getLinks
getLinks -> scroll -> then returns links
links -> get data (title, replies, tags, views, leading post)
"""

class webScrape:

    browser= None
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

    def driverReset(self):
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--incognito')
        driver= webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=opts)

    #Scrolls through the webpage
    def scroll(self, driver, timeout):
        scroll_pause_time= timeout

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # Load the entire webage by scrolling to the bottom
        lastHeight = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        while (True):
            # Scroll to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for new page segment to load
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break

            lastHeight = newHeight

    #Getting the title of the post
    def getTitle(Topicsoup):
        soup= Topicsoup
        Title= soup.find('title').text

        if Title is None:
            Title= 'No Title'

        return Title 

    def getTags(Topicsoup):
        soup= Topicsoup
        Tags= PostSoup.find_all(class_='discourse-tag bullet').text

        if len(Tags)==0:
            Tags='No Tags'

        return Tags


    #Getting the Leading post of the post
    def getLeadingPost(Topicsoup):
        cooked= PostSoup.find(class_='cooked').find_all('p')
        for Lpost in cooked:
            LeadingPost= Lpost.text

        if LeadingPost is None:
            LeadingPost = str(0)

        return LeadingPost

    #Getting the dates created
    def getDateCreated(Topicsoup):
        DateCreated= Topicsoup.find(class_='relative-date').text

        if DateCreated is None:
            DateCreated = str(0)

        return DateCreated

    def getNum_Views(Topicsoup):
        Views= Topicsoup.find(class_='secondary views').find(class_='number').text
        if Views is None:
            Views= 0

        return Views

    def getNum_Replies(Topicsoup):
        Replies= Topicsoup.find(class_='replies').find(class_='number').text
        if Replies is None:
            Replies= 0

        return Replies


    # Getting the links
    def getLinks(self, url):
        driver= self.driver
        #waiting for page to load
        driver.implicitly_wait(30)
        #getting driver to open link
        driver.get(url)
        #using scroll function to scroll to the bottom
        self.scroll(driver, 2)
        #Getting html from entire webpage
        Bsoup= BeautifulSoup(driver.page_source, 'lxml')
        #closing driver
        driver.close()

        #List to store the links we will get
        Links=[]

        #Getting all the links in the webpage
        for link in Bsoup.find_all('a', class_='title raw-link raw-topic-link'):
            Links.append(link['href'])
            print(link.text)

        return Links

    def runScraper(self, SiteName, Links):
        
        
        for link in Links:

            self.driverReset()
            #Opens the links as they come as parts on the webpage
            # Some links come in as complete so this if statement determines which come in complete and which comes in as part
            linkSplit= str(link['href']).split
            if 'https:' in str(linkSplit):
                url= link
            else:
                url='https://forums.unrealengine.com'+link
            self.driver.get(url)
            #Page HTML stored in PHTML
            PHTML= self.driver.page_source
            #Page Soup stored in PSoup
            PSoup= BeautifulSoup(PHTML, 'html.parser')

            #Getting data from the pages
            Post_Title= self.getTitle(PSoup)
            Leading_Post= self.getLeadingPost(PSoup)
            Date_Created= self.getDateCreated(PSoup)
            numViews= self.getNum_Views(PSoup)
            numReplies= self.getNum_Replies(PSoup)
            Tags= self.getTags(PSoup)
            

            #Attribute dictionary where we'll temporarily store the data we collect
            attributeDict= {
                'Post_Title': Post_Title,
                'Leading_Comment': Leading_Post,
                'Date_Created': Date_Created,
                'num_of_Views': numViews,
                'num_of_Replies': numReplies,
                'Tags': Tags,
                'Link': link
            }
            self.PostDict[Post_Title]= attributeDict
            self.PostDf= self.PostDf.append(attributeDict, ignore_index= True)

            #Testing
            print('Title: ', Post_Title)
            print('Leading Post', Leading_Post)
            print('Date of Creation', Date_Created)

        #Getting timestamp
        timeStamp = datetime.now().strftime('%Y%m%d')

        #Setting up csv file
        "Please put your name here"
        csvFilename = SiteName + '_SCRAPED_DATA' + timeStamp + '.csv'
        csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csvFilename)
        # Save dataframe into csv file
        self.PostDf.to_csv(csvFileFullPath)

if __name__ =='__main__':
    #Local path to the webdriver
    #webdriverPath = r'C:\Users\savan\Desktop\Coding and Software\Stemaway Coding Stuff\chromedriver.exe'
    
    # Forum to scrape URL    
    BaseURL = 'https://forums.unrealengine.com/tags/c/community/marketplace/51/launcher'
    
    # Name of the forum
    SiteName = 'UnrealEngineMarketplace'
        
    # WebScraping object
    webScrape = webScrape()

    Links= webScrape.getLinks(BaseURL)
    
    # Run the webscraper and save scraped data
    webScrape.runScraper(SiteName, Links)
        
