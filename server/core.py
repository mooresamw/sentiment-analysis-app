from flask import Flask, jsonify, request
from flask_cors import CORS
from processor import get_sentiment_data_from_db
from main import live_update
from stock import get_ticker_current_price, get_period_data, get_stock_info

# Create the Flask application
app = Flask(__name__)
CORS(app)


# Main API route to fetch live updates from finviz, and retrieve the stored values from CSV file
@app.route('/api/', methods=['GET'])
def get_analysis():
    live_update()
    # with open("sentiment_data.csv", mode="r") as file:
    #     reader = csv.DictReader(file)
    #     rows = list(reader)
    return jsonify(get_sentiment_data_from_db())


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


# Run the Flask server
app.run(debug=True, port=8080)
