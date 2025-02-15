from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os
from processor import process_links, save_sentiment_data_to_db
from test import retrieve_news_articles
import time
import re

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

FINVIZ_KEY = os.getenv("FINVIZ_API_KEY")


def analyze_sentiment(ticker, text):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer",
                 "content": "You are a developer with an expertise in finance and sentiment analysis."},
                {
                    "role": "user",
                    "content": f"Perform a complete sentiment analysis on the following news article for {ticker}: {text}"
                               f"Answer exactly in the following format every time :\n"
                               f"Sentiment Score: 0-1\n"
                               f"Confidence Score: 0-1\n"
                               f"Position: (buy, sell, hold)"
                               f"DO NOT INCLUDE THE ANALYSIS PART."
                }
            ]
        )

        # Extract and return the sentiment analysis result
        return completion.choices[0].message.content
    except OpenAIError as e:
        return f"An error occurred: {e}"


def extract_sentiment_data(ticker, text):
    pattern = r"Sentiment Score:\s*(\d+\.\d+)\s*Confidence Score:\s*(\d+\.\d+)\s*Position:\s*(\w+)"
    match = re.search(pattern, text)
    if match:
        sentiment_score = float(match.group(1))
        confidence_score = float(match.group(2))
        position = match.group(3)

        # Send the sentiment data to the database
        save_sentiment_data_to_db(ticker, sentiment_score, confidence_score, position)


# live updating loop
def live_update():
    print("begin loop")
    titles, urls, tickers_list, dates, categories = retrieve_news_articles(FINVIZ_KEY)
    results = process_links(titles, urls, tickers_list, dates, categories)
    for url, tickers, content in results:
        print(f"Processing news for: {tickers}")
        print(f"{tickers}: {url} \n {content[:200]}...")
        print("-" * 80)

        # Split tickers and analyze sentiment for each
        individual_tickers = [ticker.strip() for ticker in tickers.split(",")]
        for ticker in individual_tickers:
            print(f"Analyzing sentiment for ticker: {ticker}")
            sentiment_result = analyze_sentiment(ticker, content)
            print(f"Ticker: {ticker}, Sentiment Analysis:\n{sentiment_result}")
            extract_sentiment_data(ticker, sentiment_result)
            print("=" * 100)


# live sentiment analysis
while True:
    live_update()

    time.sleep(10)
