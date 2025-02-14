import datetime
from datetime import timedelta
import yfinance as yf


# Function to get the current price of a ticker
def get_ticker_current_price(ticker):
    # Fetch the historical market data for ytd
    stock = yf.Ticker(ticker)
    history = stock.history(period="ytd", auto_adjust=False, actions=False)
    current_price = history['Close'].iloc[-1]  # Price at the end of the period

    return current_price


# Function to get closing price data for different periods
def get_period_data(ticker, period):
    stock = yf.Ticker(ticker)
    data = yf.download(tickers=ticker, period=period, interval='5m', prepost=True)
    prices = data['Open']
    return [
        {'date': (timestamp - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'), 'price': "{:.2f}".format(price.item())}
        for timestamp, price in
        zip(data.index, data['Open'].values)]


# Function to get the stock company name. We can also return other stock information
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    company_name = stock.info['longName']
    current_price = stock.info['currentPrice']
    return company_name, current_price


# Function to get stock price for ticker at a given time
def get_stock_price_at_time(ticker, timestamp):
    # Convert timestamp string to datetime object
    target_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Download historical minute-level data for the day
    stock_data = yf.download(ticker, start=target_time.date(), end=target_time.date() + datetime.timedelta(days=1),
                             interval="1m")

    if stock_data.empty:
        return None  # No data available

    # Convert index (which is in UTC) to a pandas DatetimeIndex for comparison
    stock_data.index = stock_data.index.tz_localize(None)

    # Find the closest available time
    closest_time = min(stock_data.index, key=lambda x: abs(x - target_time))

    # Return the price at the closest timestamp
    return stock_data.loc[closest_time, "Close"], closest_time
