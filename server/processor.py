import base64
import csv
import os
from scraper import scrape_yahoo_finance_article
import firebase_admin
from firebase_admin import credentials, firestore

# Set up database
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def encode_url(url):
    """Encodes a URL using Base64 for Firestore document ID storage."""
    return base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")  # Remove padding


def decode_url(encoded_url):
    # Add padding if necessary
    padding = '=' * (4 - len(encoded_url) % 4)  # Correct padding
    padded_encoded_url = encoded_url + padding
    return base64.urlsafe_b64decode(padded_encoded_url.encode()).decode('utf-8')


# Function to get processed urls from a csv file
def get_processed_urls(file_path="processed_urls.csv"):
    # Read the file containing processed URLs and return as a set of URLs
    if os.path.exists(file_path):
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            return set(row[0] for row in reader)  # Extract only the first column (URLs)
    else:
        return set()


# Function to save urls to a csv file
def save_processed_urls(new_urls_with_tickers, file_path="processed_urls.csv"):
    # Append new URLs and tickers to the CSV file
    file_exists = os.path.exists(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header only if the file doesn't exist
        if not file_exists:
            writer.writerow(["URL", "Ticker"])
        # Write the new rows
        writer.writerows(new_urls_with_tickers)


# Function to return the list of processed links from the database
def get_processed_urls_from_db():
    docs = db.collection('processed_urls').stream()

    return [doc.to_dict().get("url") for doc in docs if "url" in doc.to_dict()]


# Function to save urls being processed to the database. input is a list of tuples
def save_processed_urls_to_db(news_articles_with_tickers):
    # Reference the collection
    # print(news_articles_with_tickers)
    collection_ref = db.collection('processed_urls')

    # Add new URLs and tickers
    for url, ticker in news_articles_with_tickers:
        encoded_url = encode_url(url)
        doc_ref = collection_ref.add({"tickers": ticker, "url": url})

        #doc_ref.set({"tickers": ticker, "url": url})


# Function to process only new article urls
def process_links(urls, tickers):
    if len(urls) != len(tickers):
        raise ValueError("The length of URLs and Tickers must be the same.")

    # Combine URLs and tickers into a list of tuples
    urls_with_tickers = list(zip(urls, tickers))

    # Get previously processed URLs and tickers
    processed_urls = get_processed_urls_from_db()
    new_urls_with_tickers = []
    article_contents = []

    for url, ticker in urls_with_tickers:
        if url not in processed_urls:
            try:
                # Extract content for new URLs only
                is_mobile = '/m/' in url
                content = scrape_yahoo_finance_article(url, is_mobile)
                article_contents.append((url, ticker, content))
                new_urls_with_tickers.append((url, ticker))
            except Exception as e:
                article_contents.append((url, ticker, str(e)))

    # Save new URLs and tickers to the CSV file after processing
    if new_urls_with_tickers:
        save_processed_urls_to_db(new_urls_with_tickers)

    return article_contents


# Function to retrieve the sentiment data from Firestore database
def get_sentiment_data_from_db():
    collection_ref = db.collection('sentiment_data')
    docs = collection_ref.stream()

    data = []
    for doc in docs:
        sentiment = doc.to_dict()
        data.append(sentiment)
    return data


# Function to save sentiment data gathered to our Firestore database
def save_sentiment_data_to_db(ticker, sentiment_score, confidence_score, position):
    # Define the sentiment data
    sentiment_data = {
        "ticker": ticker,
        "sentiment": sentiment_score,
        "confidence": confidence_score,
        "position": position
    }

    # Reference to the collection in Firestore
    collection_ref = db.collection('sentiment_data')

    # Check if the ticker already exists in Firestore
    doc_ref = collection_ref.document(ticker)
    doc = doc_ref.get()

    if doc.exists:
        # Update the existing document if the ticker is found
        doc_ref.update(sentiment_data)
        print(f"Updated data for {ticker}: {sentiment_data}")
    else:
        # Add a new document if the ticker does not exist
        doc_ref.set(sentiment_data)
        print(f"Added data for {ticker}: {sentiment_data}")
