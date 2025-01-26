from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os
import csv

from main import live_update
from scraper import scrape_yahoo_finance_article, process_links
from test import retrieve_news_articles
import time

app = Flask(__name__)
CORS(app)


@app.route('/api/', methods=['GET'])
def get_analysis():
    live_update()
    with open("sentiment_data.csv", mode="r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return jsonify(rows)


app.run(debug=True, port=8080)
