# **Trading Strategies Setiment Project**

[![Language](https://img.shields.io/badge/Python-darkblue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Framework](https://img.shields.io/badge/sklearn-darkorange.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Framework](https://img.shields.io/badge/FastAPI-darkgreen.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Framework](https://img.shields.io/badge/Streamlit-red.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)

An end-to-end Data Science and Machine Learning Project.

## **Problem Statement**

Automated trading system also referred to as algorimith trading, allow traders to establish specific rules for both trade entries and exits that, once programmed, can be automatically executed via a computer. In this sese, there is a long list of advantages to having a computer monitor the markets for trading opportunities and execute the trades, including:

- Minimizing emotions
- Backtesting
- Peserving discipline
- Improving order entry speed
- Diversiying trading

On the other hand,  Sentiment analysis is also one of the more successful methods of including the effects of market psychology in a trading strategy. Empirical evidence suggests that investor sentiment is one of the most reliable indicators of future price movements.

Therefore, in this project, we develop a Streamlit App that utilizes an Automated Trading System as an API to get two trading strategies (MACD and MFI) and a sentiment detector based on a deep learning model(GRU). 

The App can be viewed through this [link]()

[Deep Learning Model NoteBook]()

## Trading system

### Trading Strategies implemets in this project:
 
#### Moving average convergence/divergence(MACD)
 - The MACD is a technical analysis indicator that aims to identify changes in a share price's momentum. The MACD collects data from different moving averages to help traders indetify possible oppotunities around support and resistance levels.

MACD indicator components:

- MACD line, measures the distance between two moving averages.
- Signal line, identifies changes in price momentum and acts as a trigger for buy and sell signal.
- Histogram, represents the difference between the MACD and signal line.

The MACD line was created by subtracting the 26-period moving average form the 12-period moving average. on the other hand, the signal line was created taking the 9-period moving average of the MACD.

Sell and Buy MACD signal

- The MACD is then displayed as a histogram, a graphical representation of the distance between the two lines. If the MACD cuts through the signal line from below, traders could use it as a buy signal and if it cuts the signal line from above, traders might use it as a sell signal.

#### Money Flow Index(MFI)
- The MFI is a technical oscillator that measures the inflow an outflow of money into an asset over a period of time. it looks at both price and volume to assess the buying and selling pressures in a given market.

Sell and Buy MFI signal

- The money flow index works by oscillating on a scale from zero to 100. If the MFI reading is obove 80, the market would be considered overbounght, while a reading of 20 or below is a signal for oversold conditions.

## Data

#### Financial data
- Finance data (daily trading) were extracted from [Alpha Vantage API](https://www.alphavantage.co/). 

Data preprocessing stets:
 - Transform the data from json format to a dataframe format
 - Create datetime index
 - Stored the data into a PostGres Database


#### Text data
- The tweets data were extrated from Twetter app using snscrape python library.

Keywords for searching:
 - "Stock Market"
 - "Stock Market sentiment"
 - "Stocks"

Data preprocessing stets:
 - Transform the data into a dataframe format
 - Clean tweets data 
 - Stored the data in a CSV file
 - Cleaning and feature engineering (Lemmatizer and remove Stock words)
 - Create target variable (Get sentiments)


## Sentiment Analysis

### Modelling 
Recurrent Neural Network Architectures that were tested:
 - LSTM
 - GRU
 
GRU architecture was chosen as the final model.

## REST API
The trading system was developed as a rest API/web service using FastAPI (web framework from python). In this sense, this API has three different services:

- MACD trading strategy service
- MFI trading strategy service
- Sentiment detector services

The API's code and its dependencies were packed into a container using Docker. The Docker image was stored on Docker hud.

- [API image](https://hub.docker.com/repository/docker/lfss08/stfastapi/general)
