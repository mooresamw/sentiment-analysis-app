import requests
from bs4 import BeautifulSoup


# Function to fetch the given url
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
    #if is_mobile:
    if '/m' in url:
        #body_div = soup.find('div', class_='caas-body')  # Mobile links
        body_div = soup.find('div', class_='body')  # Mobile links
    else:
        body_div = soup.find('div', class_='body')  # Non-mobile links
    article_content = ""

    # Extract and join <p> tags within the div with class 'body'
    if body_div:
        paragraphs = body_div.find_all('p')
        article_content = " ".join([p.text for p in paragraphs])
    else:
        print(url)
        print("No div with class 'body' found.")

    # Print the extracted information
    article = {
        "Title": title,
        "Publication Date": pub_date,
        "Content": article_content,
    }
    #return article["Title"] + ": " + article["Content"]
    return article["Content"]


url = "https://finance.yahoo.com/m/9d249331-fc18-3a36-8e27-1b21ae7f1db9/lpl-earnings-beat-estimates.html"
#url = "https://finance.yahoo.com/news/first-guaranty-bancshares-q4-earnings-230055117.html"
# try:
#     article_content = scrape_yahoo_finance_article(url)
#     print(article_content)
# except Exception as e:
#     print(e)
