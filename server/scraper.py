import os
import csv
import requests
from bs4 import BeautifulSoup


def fetch_url_content(url, user_agent=None):
    headers = {
        "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch URL {url}: {response.status_code}")


# Function to scrape Yahoo Finance article and return the article full content
def scrape_yahoo_finance_article(url, is_mobile=False):
    # Using different user agents for gathering articles
    mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148"
    desktop_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Fetch the content using appropriate User-Agent
    html_content = fetch_url_content(url, mobile_user_agent if is_mobile else desktop_user_agent)
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the title
    title = None
    div_title = soup.find('div', class_='cover-title')
    if div_title:
        title = div_title.text.strip()
    else:
        # If not found, try finding an h1 tag
        h1_title = soup.find('h1', id='caas-lead-header-undefined')
        if h1_title:
            title = h1_title.text.strip()

    # Extract the publication date
    pub_date = soup.find('time')['datetime'] if soup.find('time') else "Publication date not found"

    # Find the div with class 'body' (main article content)
    if is_mobile:
        body_div = soup.find('div', class_='caas-body')  # Mobile links
    else:
        body_div = soup.find('div', class_='body')  # Non-mobile links
    article_content = ""

    # Extract and join <p> tags within the div with class 'body'
    if body_div:
        paragraphs = body_div.find_all('p')
        article_content = " ".join([p.text for p in paragraphs])
    else:
        print("No div with class 'body' found.")

    # Print the extracted information
    article = {
        "Title": title,
        "Publication Date": pub_date,
        "Content": article_content,
    }
    #return article["Title"] + ": " + article["Content"]
    return article["Content"]


def get_processed_urls(file_path="processed_urls.csv"):
    # Read the file containing processed URLs and return as a set of URLs
    if os.path.exists(file_path):
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            return set(row[0] for row in reader)  # Extract only the first column (URLs)
    else:
        return set()


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


def process_links(urls, tickers):
    if len(urls) != len(tickers):
        raise ValueError("The length of URLs and Tickers must be the same.")

    # Combine URLs and tickers into a list of tuples
    urls_with_tickers = list(zip(urls, tickers))

    # Get previously processed URLs and tickers
    processed_urls = get_processed_urls()
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
        save_processed_urls(new_urls_with_tickers)

    return article_contents

#url = "https://finance.yahoo.com/m/4401a006-a041-3a2c-afbd-4dabb50a693f/donald-trump-launches-trump.html"
# url = "https://finance.yahoo.com/news/agoda-shares-five-destinations-slither-032500429.html"
# try:
#     article_content = scrape_yahoo_finance_article(url)
#     print(article_content)
# except Exception as e:
#     print(e)
