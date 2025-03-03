from flask import Flask, jsonify, request
from flask_cors import CORS
from processor import get_sentiment_data_from_db, get_recent_news_articles, get_all_price_changes, \
    calculate_average_price_changes, get_most_recent_price_change
from main import live_update
from stock import get_ticker_current_price, get_period_data, get_stock_info

# Create the Flask application
app = Flask(__name__)
CORS(app)


# Main API route to fetch live updates from finviz, and retrieve the stored values from CSV file
@app.route('/api/', methods=['GET'])
def get_analysis():
    live_update()
    response_data = get_sentiment_data_from_db()

    # Get average price changes
    # price_changes = calculate_average_price_changes(get_all_price_changes())

    # Add price change data to response
    for item in response_data:
        ticker = item.get("ticker")
        #item["price_change"] = price_changes.get(ticker, 0.0)  # Default to 0.0 if no data

        # Grab the most recent price change for the ticker which will update when new articles are processed
        item["price_change"] = get_most_recent_price_change(ticker)

    return jsonify(response_data)


# Api route to get the current price of a ticker
@app.route('/api/ticker/<ticker>/get_current_price', methods=['GET'])
def get_current_price(ticker: str):
    company_name, current_price = get_stock_info(ticker)
    return {'current_price': current_price, 'company_name': company_name}


# Api route to get the live stock prices
@app.route('/api/ticker/<ticker>/get_period_data', methods=['GET'])
def get_prices(ticker: str):
    data = get_period_data(ticker, '1d')
    return jsonify(data)


# API endpoint to fetch the two most recent news articles for a ticker from the database
@app.route('/api/ticker/<ticker>/get_recent_news', methods=['GET'])
def get_recent_news(ticker):
    recent_articles = get_recent_news_articles(ticker)

    if not recent_articles:
        return jsonify({"error": f"No news articles found for {ticker}"}), 404

    return jsonify(recent_articles), 200


# Run the Flask server
app.run(debug=True, port=8080)
