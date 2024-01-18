#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template
from cassandra.cluster import Cluster
from textblob import TextBlob

app = Flask(__name__)

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using TextBlob.
    Returns a sentiment score in the range of -1 to 1.
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

@app.route('/')
def index():
    # Connect to Cassandra and retrieve the sentiment analysis results
    cluster = Cluster(['localhost'])
    session = cluster.connect('sentiment_analysis')
    rows = session.execute("SELECT * FROM news_articles;")

    # Process the sentiment analysis results
    sentiment_results = []

    for row in rows:
        content = row.content
        # Implement sentiment analysis here with TextBlob as shown in Step 5
        sentiment = analyze_sentiment(content)
        sentiment_results.append({'content': content, 'sentiment': sentiment})

    return render_template('dashboard.html', sentiment_results=sentiment_results)

if __name__ == '__main__':
    app.run(port=8080)

