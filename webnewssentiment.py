#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup

# Specify the URL of the website you want to scrape
url = 'https://www.nytimes.com'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Extract relevant text data, e.g., article headlines and content
headlines = [headline.text for headline in soup.find_all('h2')]
contents = [content.text for content in soup.find_all('p')]


# In[9]:


from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect('sentiment_analysis')

# Create a table to store the scraped data
session.execute("""
    CREATE TABLE IF NOT EXISTS news_articles (
        id UUID PRIMARY KEY,
        headline TEXT,
        content TEXT
    )
""")

# Insert the scraped data into Cassandra
for headline, content in zip(headlines, contents):
    session.execute("INSERT INTO news_articles (id, headline, content) VALUES (uuid(), %s, %s)", (headline, content))


# In[10]:


from textblob import TextBlob

# Assuming you have a list of scraped articles in the 'contents' variable
for content in contents:
    # Create a TextBlob object for the article content
    blob = TextBlob(content)

    # Get the sentiment polarity (positive, negative, or neutral) and subjectivity score
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity

    # You can print or store these values as needed
    print(f"Sentiment Polarity: {sentiment_polarity}")
    print(f"Subjectivity: {sentiment_subjectivity}")


# In[ ]:




