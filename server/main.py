import csv
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

        # Store or use the extracted data
        print(f"Sentiment Score: {sentiment_score}")
        print(f"Confidence Score: {confidence_score}")
        print(f"Position: {position}")

        # Send the sentiment data to the database
        save_sentiment_data_to_db(ticker, sentiment_score, confidence_score, position)

    #     sentiment_data = {
    #         "ticker": ticker,
    #         "sentiment": sentiment_score,
    #         "confidence": confidence_score,
    #         "position": position
    #     }
    #
    #     # Read existing data
    #     rows = []
    #     file_exists = False
    #     try:
    #         with open("sentiment_data.csv", mode="r") as file:
    #             reader = csv.DictReader(file)
    #             rows = list(reader)
    #             file_exists = True
    #     except FileNotFoundError:
    #         pass
    #
    #     # Check if the ticker exists and update it, otherwise add a new row
    #     ticker_found = False
    #     for row in rows:
    #         if row["ticker"] == ticker:
    #             row.update(sentiment_data)
    #             ticker_found = True
    #             break
    #
    #     if not ticker_found:
    #         rows.append(sentiment_data)
    #
    #     # Write updated data back to the CSV
    #     with open("sentiment_data.csv", mode="w", newline="") as file:
    #         writer = csv.DictWriter(file, fieldnames=["ticker", "sentiment", "confidence", "position"])
    #         writer.writeheader()
    #         writer.writerows(rows)
    #
    #     print(f"{'Updated' if ticker_found else 'Added'} data for {ticker}: {sentiment_data}")
    # else:
    #     print(f"No match found for ticker {ticker}")


def live_update():
    print("begin loop")
    urls, tickers_list = retrieve_news_articles()
    results = process_links(urls, tickers_list)
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
# while True:
#     live_update()
#
#     time.sleep(100)
