from flask import Flask, jsonify, request
from flask_cors import CORS
import csv

from processor import get_sentiment_data_from_db
from main import live_update
import firebase_admin
from firebase_admin import credentials, firestore
import os

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


# Run the Flask server
app.run(debug=True, port=8080)
