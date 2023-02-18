# **Trading Strategies Setiment Project**

[![Language](https://img.shields.io/badge/Python-darkblue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Framework](https://img.shields.io/badge/sklearn-darkorange.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Framework](https://img.shields.io/badge/FastAPI-darkgreen.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Framework](https://img.shields.io/badge/Streamlit-red.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)

An end-to-end Data Science and Machine Learning Project.

## Goal


## **Problem Statement**

Automated trading system also referred to as algorimith trading, allow traders to establish specific rules for both trade entries and exits that, once programmed, can be automatically executed via a computer. In this sese, there is a long list of advantages to having a computer monitor the markets for trading opportunities and execute the trades, including:

- Minimizing emotions
- Backtesting
- Peserving discipline
- Improving order entry speed
- Diversiying trading

 ## Trading Strategies implemets in this project:
 
 Moving average convergence/divergence(MACD)
 - The MACD is a technical analysis indicator that aims to identify changes in a share price's momentum. The MACD collects data from different moving averages to help traders indetify possible oppotunities around support and resistance levels.

MACD indicator components:

- MACD line, measures the distance between two moving averages.
- Signal line, identifies changes in price momentum and acts as a trigger for buy and sell signal.
- Histogram, represents the difference between the MACD and signal line.

The MACD line was created by subtracting the 26-period moving average form the 12-period moving average. on the other hand, the signal line was created taking the 9-period moving average of the MACD.

### Sell and Buy MACD signal

The MACD is then displayed as a histogram, a graphical representation of the distance between the two lines. If the MACD cuts through the signal line from below, traders could use it as a buy signal and if it cuts the signal line from above, traders might use it as a sell signal.







Therefore, in this project we develop a Streamlit App that utilizes a Machine Learning model(XGBoost) as an API to detect potential fraud in credit card transactions, based on the following criteria: Type of transaction, Amount(money), Old balance orig, New balance orig, Old balance dest, New balance dest.

The App can be viewed through this [link](https://luissalazarsalinas-fraud-detection-fraud-detection-app-zvrvsp.streamlitapp.com/)

[NoteBook]()

## Data Preparation

Credit card transaction is a syntetic financial dataset created using a simulator called PaySim. In this sense, PaySim uses aggregated data from the private dataset to generate a synthetic dataset that resembles the normal operation of transactions and injects malicious behaviour to later evaluate the performance of fraud detection methods.

#### Data preprocessing stets:
 - Clean the data: removed duplicate values, missing values, unnecessary and leakage variables
 - Transform no-numerical variables to numerical variables
 - Split the data into train, validation and test sets

Source dataset: [Credit card data](https://www.kaggle.com/datasets/ealaxi/paysim1)

## Modelling 
Machine Learning Algorithms that were tested:
 - Random Forest 
 - LightGBM
 - XGBoost

Xgboost was the model with better performance with the validation set:
 - Accuracy: 0.93
 - F1-Score: 0.90
 - ROC-AUC: 0.93
 
Xgboost was chosen as the final model, and its hyperparameters were optimized using hyperopt(library) with a Bayesian optimization as search strategy.

Final model performance with the test set:
 - Accuracy: 0.99
 - F1-Score: 0.89
 - ROC-AUC: 0.91
 
 Feature importance
 ![image](https://github.com/Luissalazarsalinas/Fraud-Detection/blob/master/img/Feature_importance.png)
The variables that contribute most to the XGBoost final model were:
 - Type of transferent
 - New balance orig
 - Old balance orig
These variables could be good predictors to detect fraud in credit card transactions.



