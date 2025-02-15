import base64
import csv
import datetime
import os
from scraper import scrape_yahoo_finance_article
from stock import get_stock_price_at_time
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
    doc_ref = db.collection('metadata').document('processed_urls')
    doc = doc_ref.get()

    if not doc.exists:
        return set()  # Return empty set if no data exists

    # Extract processed URLs from Firestore
    processed_articles = doc.to_dict().get("processed_articles", [])
    return {article["url"] for article in processed_articles}  # Return a set of URLs


# Function to clean articles older than a day
def clean_old_articles(existing_data):
    now = datetime.datetime.utcnow()  # Get current time in UTC

    cleaned_data = []
    for article in existing_data:
        try:
            article_time = datetime.datetime.strptime(article["timestamp"], "%Y-%m-%d %H:%M:%S")
            if (now - article_time).total_seconds() <= 86400:  # 86400 seconds = 1 day
                cleaned_data.append(article)  # Keep only recent articles
        except ValueError:
            continue  # Skip articles with invalid timestamps

    return cleaned_data


# Function to save urls being processed to the database. input is a list of tuples
def save_processed_urls_to_db(news_articles):
    doc_ref = db.collection('metadata').document('processed_urls')
    doc = doc_ref.get()

    # Retrieve existing data from Firestore
    existing_data = doc.to_dict().get("processed_articles", []) if doc.exists else []

    # Clean up old articles before adding new ones
    existing_data = clean_old_articles(existing_data)

    # Create a set of existing URLs for quick lookup (avoid duplicates)
    existing_urls = {article["url"] for article in existing_data}

    # Append new articles if not already processed
    for title, url, ticker, timestamp, category, prices_at_date in news_articles:
        if url not in existing_urls:
            existing_data.append({
                "title": title,
                "url": url,
                "ticker": ticker,
                "timestamp": timestamp,
                "category": category,
                "prices_at_date": prices_at_date
            })

    # Save back to Firestore
    doc_ref.set({"processed_articles": existing_data})  # Overwrite document


# Function to process only new article URLs and save to Firestore
def process_links(titles, urls, tickers, dates, categories):
    if not (len(titles) == len(urls) == len(tickers) == len(dates) == len(categories)):
        raise ValueError("The length of Titles, URLs, Tickers, Dates, and Categories must be the same.")

    # Get set of previously processed URLs to avoid re-processing
    processed_urls = get_processed_urls_from_db()
    new_articles = []
    article_contents = []

    # Process only new articles
    for title, url, ticker, date, category in zip(titles, urls, tickers, dates, categories):
        if url not in processed_urls:  # Now this is a fast lookup in the set
            try:
                # Scrape Yahoo Finance article
                is_mobile = '/m/' in url
                content = scrape_yahoo_finance_article(url, is_mobile)
                price_at_date = get_stock_price_at_time(ticker, date)  # Get price at the article's timestamp

                # Handle multiple tickers
                ticker_list = ticker.split(",")  # Split string into individual tickers
                prices_at_date = {t: get_stock_price_at_time(t, date) for t in ticker_list}

                # Store new articles in the list
                article_contents.append((url, ticker, content))
                new_articles.append(
                    (title, url, ticker, date, category, prices_at_date))  # Store new articles in the list
            except Exception as e:
                article_contents.append((url, ticker, str(e)))

    # Save only new articles to Firestore
    if new_articles:
        save_processed_urls_to_db(new_articles)

    return article_contents


# Function to retrieve the sentiment data from Firestore database
def get_sentiment_data_from_db():
    doc_ref = db.collection('metadata').document('sentiment_data')
    doc = doc_ref.get()

    return doc.to_dict().get("sentiment_data", []) if doc.exists else []


# Function to save sentiment data gathered to our Firestore database
def save_sentiment_data_to_db(ticker, sentiment_score, confidence_score, position):
    doc_ref = db.collection('metadata').document('sentiment_data')
    doc = doc_ref.get()

    existing_data = doc.to_dict().get("sentiment_data", []) if doc.exists else []

    # Check if ticker already exists, and update it
    updated = False
    for entry in existing_data:
        if entry["ticker"] == ticker:
            entry.update({
                "sentiment": sentiment_score,
                "confidence": confidence_score,
                "position": position
            })
            updated = True
            break

    # If ticker doesn't exist, add a new entry
    if not updated:
        existing_data.append({
            "ticker": ticker,
            "sentiment": sentiment_score,
            "confidence": confidence_score,
            "position": position
        })

    doc_ref.set({"sentiment_data": existing_data})


# Function to fetch the two most recent news articles for a ticker from the database
def get_recent_news_articles(ticker, limit=2):
    doc_ref = db.collection('metadata').document('processed_urls')
    doc = doc_ref.get()

    if not doc.exists:
        return []

    # Extract articles and filter by the given ticker
    processed_articles = doc.to_dict().get("processed_articles", [])

    filtered_articles = []
    for article in processed_articles:
        article_tickers = article.get("ticker", "")

        # Convert the ticker field to a list
        if isinstance(article_tickers, str):
            ticker_list = article_tickers.split(",")  # Split if it's a CSV string
        else:
            ticker_list = [article_tickers]  # Handle unexpected non-string cases

        # Check if the requested ticker is in the list
        if ticker in ticker_list:
            filtered_articles.append(article)

    if not filtered_articles:
        return []

    # Sort by timestamp (most recent first)
    filtered_articles.sort(key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), reverse=True)

    # Return the most recent articles up to the specified limit
    return filtered_articles[:limit]
