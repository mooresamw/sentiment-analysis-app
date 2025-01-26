import requests
import pandas as pd
import io


def retrieve_news_articles():
    url = "https://elite.finviz.com/news_export.ashx?v=3&auth=9972c25f-e5d7-4bd5-aba9-34d475ccdc4c"
    response = requests.get(url)
    data = io.StringIO(response.text)
    df = pd.read_csv(data)
    filtered_url_list = [url for url in df['Url'].tolist() if "finance.yahoo" in url]
    filtered_urls = df[df['Url'].str.contains("finance.yahoo", na=False)]
    filtered_ticker_list = []
    for url, ticker in zip(filtered_urls['Url'], filtered_urls['Ticker']):
        filtered_ticker_list.append(ticker)

    return filtered_url_list, filtered_ticker_list
