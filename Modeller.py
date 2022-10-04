"""
@author: Savann
Version: 1.01
Purpose: To create a model using logistic regression of the forum data collected
"""

import pandas as pd
import os, re, glob, logging, gensim
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


"""
TODO: Import all files
TODO: Find TFIDF
TODO: Create vectors
TODO: Create logistic Regression Model
"""

"Importing Files"
folders_file= os.listdir(f"..\\Stemaway Recommender\\Processed-Data")

#Importing the data (There are easier ways to do this but I was running out of time so did this way)
forum1= pd.read_csv("..\\Stemaway Recommender\\Processed-Data\\forum_data_full_1.csv")
forum1.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]


forum2= pd.read_csv("..\\Stemaway Recommender\\Processed-Data\\forum_data_full_2.csv")
forum2.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]

forum3= pd.read_csv("..\\Stemaway Coding Stuff\\Stemaway Recommender\\Processed-Data\\forum_data_full_3.csv")
forum3.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]

forum4= pd.read_csv("..\\Stemaway Recommender\\Processed-Data\\forum_data_full_4.csv")
forum4.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]

forum5= pd.read_csv("..\\Stemaway Recommender\\Processed-Data\\forum_data_full_5.csv")
forum5.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]

forum6= pd.read_csv("..\\Stemaway Coding Stuff\\Stemaway Recommender\\Processed-Data\\forum_data_full_6.csv")
forum6.columns= ["Title", "Category", "Date-Scraped", "Link", "Date-Posted", "Last-Reply", "Replies", "Views", "Users", "Likes", "Links", "Words"]

allData= forum1, forum2, forum3, forum4, forum5, forum6

FullForum= pd.concat(allData)

"Exploring the Data"

#Categories
Categories= FullForum["Category"].unique()

wordcloud= WordCloud(width= 800, height= 800, background_color= 'white', stopwords= None, min_font_size= 10).generate(str(Categories))

#plotting the wordcloud image
plt.figure(figsize=(4,8), facecolor= None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad= 0)
plt.show()

#Words
Words= FullForum["Words"]

#Setting up wordcloud
wordcloud2= WordCloud(width= 800, height=800, background_color='white', stopwords=None, min_font_size= 5).generate(str(Words))

#Plotting the wordcloud by defining the features
plt.figure(figsize=(4, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()                  #Showing the wordcloud

#Time to model
X= FullForum.Words    #Setting the x axis of our model
Y= FullForum.Category #Setting the y axis of our model
#Setting the split for training and testing
X_train, X_test, Y_train, Y_test= train_test_split(X, Y, test_size=0.3, random_state= 42)

#Setting up the pipeline that we will use to model the data
# Vectorizer -> Transformer -> Logistic regression
logreg= Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LogisticRegression(n_jobs=1, C=1e5, max_iter= 15000)),])
logreg.fit(X_train, Y_train)

#Using the prediction split to test the model
Y_pred= logreg.predict(X_test)

#Getting accuracy (42%... not good Will test out different models)
print(f'accuracy {accuracy_score(Y_pred, Y_test)}')
res1331= accuracy_score(Y_pred, Y_test)
print(classification_report(Y_test, Y_pred, target_names=Categories))