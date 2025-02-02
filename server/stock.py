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
    return [{'date': timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'price': "{:.2f}".format(price.item())} for timestamp, price in
            zip(data.index, data['Open'].values)]


# Function to get the stock company name. We can also return other stock information
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    company_name = stock.info['longName']
    current_price = stock.info['currentPrice']
    return company_name, current_price
