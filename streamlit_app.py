import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf
from plotly._subplots import make_subplots
import plotly.graph_objects as go
from app.trading_strategy import MACD
from app.routers.sentiment_analysis import predict

# App title
st.title("Trading System App")

#some image
st.image("img/trading_system.png")

# Description
st.write(
    """
    ## About
    Automated trading system also referred to as algorimith trading, 
    allow traders to establish specific rules for both trade entries and exits that, once programmed, 
    can be automatically executed via a computer. In this sese, there is a long list of advantages to having a computer monitor the markets for trading opportunities and execute the trades, including:
    
    - Minimizing emotions
    - Backtesting
    - Peserving discipline
    - Improving order entry speed
    - Diversiying trading

    On the other hand,  Sentiment analysis is also one of the more successful methods of including the effects of market psychology in a trading strategy. 
    Empirical evidence suggests that investor sentiment is one of the most reliable indicators of future price movements.

    This Streamlit App utilizes an Automated Trading System as an API to get one trading strategy (MACD and MFI) and a sentiment detector based on a deep learning model(GRU). 
    
    
    All documentations are available on [Github](https://github.com/Luissalazarsalinas/Trading-Strategies-Setiment-Project)
    
    **Made by Luis Fernando Salazar S.**

    """
)
#### Transform funtion #############################################################
###################### Funtions to transform categorical variable #############################################
def add_data(content):
    if content == "YES":
        content = True
    elif content == "NOT":
        content = False
    return content

################################# INPUT DATA ###########################################
########################################################################################
st.sidebar.subheader("Trading Strategies Input Data")


ticker = st.sidebar.text_input("Symbol")
invesment_mount = st.sidebar.number_input("Invesment Mount", min_value= 100, max_value= 50000)
# layers
data_new = ("YES", "NOT")
add_new_data = st.sidebar.selectbox("Are you want use new data?", data_new)
################################### PLOTS #################################
###########################################################################
#############################################################################################################################################
#################################### MACD  ############################################################################
st.subheader(" TRADING STRATEGY")

macd_strategy = st.button("MACD STRATEGY")

if macd_strategy:
    # Data
    try:
        # Instnace
        macd = MACD(ticker= ticker, new_data= add_data(add_new_data))

        # Get dataframe with componen of the indicator 
        macd.get_indicator()
        # sell and buy signal
        buy_sell_siganl = macd.buy_sell_signal()

        # buy signal
        buy_signal = buy_sell_siganl[0]
        #sell signal
        sell_signal = buy_sell_siganl[1]
        # Backtesting 
        backtesting = macd.BackTesting(invesment_value = invesment_mount)
        
    except Exception as e:
        print(e)
        
    # plotly go object
    fig = go.Figure()

    # make subplots 
    fig = make_subplots(
        rows = 3, cols = 1, shared_xaxes = True,
        vertical_spacing=0.001, row_heights=[3.5,2.5,2.5]
    )

    # candlestick charts
    fig.add_trace(
        go.Candlestick(
            x = macd.df.index,
            open = macd.df["open"],
            high=macd.df['high'],
            low=macd.df['low'],
            close=macd.df['close'], name=f'{ticker} Share Data',
            showlegend=False
        ), row=1, col=1
    )

    # # Volume chart
    # color_v = ['green' if row['open']- row['close']>= 0 else 'red' for index, row in macd.df.iterrows()]
    # fig.add_trace(
    #     go.Bar(
    #         x = macd.df.index,
    #         y = macd.df['volume'],
    #         marker_color = color_v,
    #         showlegend=False
    #     ), row=2, col=1
    # )

    # MACD Indicator plot 
    fig.add_trace(
        go.Scatter(
            x = macd.df.index,
            y = macd.df['MACD_line'],
            line = dict(color='blue', width=1),
            showlegend=False
        ), row=2, col=1
    )
    # Signal
    fig.add_trace(
        go.Scatter(
            x = macd.df.index,
            y = macd.df['Signal_line'],
            line = dict(color='black', width=1),
            showlegend=False
        ), row=2, col=1
    )

    # Histogram
    color_h = ['green' if val >= 0 else 'red' for val in macd.df['MACD_line']]
    fig.add_trace(
        go.Bar(
            x = macd.df.index,
            y = macd.df['Hist'],
            marker_color = color_h,
            showlegend=False
        ), row=2, col=1
    )

    # Buy and sell signal char
    fig.add_trace(
        go.Scatter(
            x = macd.df.index,
            y = buy_signal,
            mode = 'markers',
            text = buy_signal,
            marker = dict(color='green'),
            showlegend=False
        ), row=3, col=1
    )
    fig.add_trace(
        go.Scatter(
            x = macd.df.index,
            y = sell_signal,
            mode= 'markers',
            text = sell_signal,
            marker = dict(color='red'),
            showlegend=False
        ), row=3, col=1
    )

    fig.add_trace(
        go.Scatter(
            x = macd.df.index,
            y = macd.df['close'],
            line = dict(color='blue', width=1),
            opacity= 0.7,
            showlegend=False
        ), row=3, col=1
    )

    # Update Title
    fig.update_layout(
        title = f'{ticker} - MACD Strategy',
        xaxis_rangeslider_visible=False,
        width=5900,height=900
        )
    # update y-axis label
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=2, col=1)
    fig.update_yaxes(title_text="Price", row=3, col=1)    


    st.plotly_chart(fig, use_container_width=True, width=5900,height=900)

    with st.expander('Trading Strategy Performance'):

        st.write(
          f""" 
        ### **Model Details**
        Stock Symbol: {ticker}\n
        Invesment Amount[$]: {invesment_mount}

        #### **MACD Strategy**
        Total Invesment Return[$]: {backtesting[0]}\n
        Profit Percentage: {backtesting[1]}

        #### **Benchmark Strategy**
        Total Invesment Return[$]: {backtesting[2]}\n
        Profit Percentage: {backtesting[3]}

        #### **MACD Performance**
        Macd strategy perfromance: {backtesting[4]}
        """
    )


#################################################################################################
########################## SENTIMENT DETECTOR #####################################################
st.subheader("SENTIMENT DETECTION")

## Input text data
text = st.text_area('Text to analyze')

setiment = st.button("Get Sentiment")

if setiment:
    
    # Inference 
    pred = predict(text)

    # Results
    if pred == 0:
        st.write("Sentiment: Negative")
        
    elif pred == 1:
        st.write("Sentiment: Positive")
    else:
        st.write("Sentiment: Neutro")

