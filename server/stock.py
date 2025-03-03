import datetime
from datetime import timedelta
import yfinance as yf
import pytz


# Function to get the current price of a ticker
def get_ticker_current_price(ticker):
    # Fetch the historical market data for ytd
    stock = yf.Ticker(ticker)
    history = stock.history(period="ytd", auto_adjust=False, actions=False)
    current_price = history['Close'].iloc[-1]  # Price at the end of the period

    return current_price


# Function to get closing price data for different periods
def get_period_data(ticker, period):
    data = yf.download(tickers=ticker, period=period, interval='5m', prepost=True)
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
    # Convert timestamp string to datetime object (assume input is in EST)
    est = pytz.timezone("US/Eastern")
    target_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    target_time = est.localize(target_time)

    #target_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Download historical data with pre/post-market included
    stock_data = yf.download(
        ticker,
        start=target_time.date() - datetime.timedelta(days=3),  # Include previous day for pre-market
        end=target_time.date() + datetime.timedelta(days=1),  # Include next day for after-hours
        interval="5m",
        prepost=True,  # Include pre-market & after-hours data
        progress=False,
        auto_adjust=True,
    )

    if stock_data.empty:
        return None  # No data available

    # Convert the index (which is in UTC) to Eastern Time (ET)
    stock_data.index = stock_data.index.tz_convert("US/Eastern")

    # Convert target_time to ET (assuming input is in EST)
    target_time = target_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))  # EST offset

    # Find the closest available time
    closest_time = min(stock_data.index, key=lambda x: abs(x - target_time))

    # Return just the stock price at that timestamp
    return stock_data.loc[closest_time, "Close"].iloc[0]


# Function to get stock price change % from when news broke out to current time
def get_stock_price_change(ticker, timestamp):
    # Get the current price of the stock
    current_price = get_ticker_current_price(ticker)
    # Get the price of the stock at the given timestamp
    price_at_timestamp = get_stock_price_at_time(ticker, timestamp)
    # Calculate the price change percentage
    price_change = round(((current_price - price_at_timestamp) / price_at_timestamp) * 100, 2)

    return price_change
