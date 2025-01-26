# Live Stock News Sentiment Analysis App

## Overview
This project is a live program designed to perform sentiment analysis on stock-related news articles using ChatGPT and then displaying the results in a dashboard user interface. 
By analyzing the tone and content of news articles, the program determines the sentiment score associated with a specific stock. 
The insights can help investors make informed decisions regarding their positions in the stock market.

## Features
- **Sentiment Classification:** Identifies whether a news article's sentiment is Positive, Negative, or Neutral.
- **Confidence Scoring:** Provides a confidence score for the sentiment classification.
- **Trend Visualization:** Highlights sentiment trends from the text, such as mentions of risks, opportunities, or market dynamics.
- **Actionable Recommendations:** Offers recommendations for Long, Short, or No Position based on sentiment insights.

## Technologies Used
- **Typescript:** Core programming language for the project's frontend development.
- **Python:** Core programming language for the project's backend development and sentiment analysis.
- **Next.js:** Frontend framework.
- **OpenAI GPT Model:** For natural language processing and sentiment classification.
- **FinViz API:** To gather news article information such as headline, date published, article URL, and involved tickers.
- **BeautifulSoup:** To parse HTML pages to acquire full news article content.
  
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mooresamw/sentiment-analysis-app.git
   ```
2. Install the node_modules directory:
    ```bash
   npm install
   ```
3. Navigate to the server directory:
   ```bash
   cd server
   ```
4. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```
5. Install the required Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
6. Create .env file and paste your OpenAI API key in the following format:
   ```bash
   OPENAI_API_KEY=your-api-key
   ```

## Usage
1. Run the frontend program:
   ```bash
   npm run dev
   ```
2. Navigate to the server directory:
   ```bash
   cd server
   ```
3. Run the server program:
   ```bash
   python3 core.py
   ```
4. Navigate to your web browser of choice and go to the following link:
   ```bash
   http://localhost:3000/
   ```
