# Class to implemente trading strategies
import numpy as np
import pandas as pd
import math
from app.data import AlphaVantageApi

class MACD():
    """
    """
    def __init__(self, ticker):
        
        self.ticker = ticker


    def get_indicator(self):
        
        # Get daily data
        av = AlphaVantageApi()
        # Stored data into a object variable
        self.df =  av.get_daily(ticker = self.ticker)

        # Calculate the MACD and signal line indicators
        
        ## Calculate the short term exponetial moving average (EMA) with 12 units
        self.df["short_EMA"] = self.df["close"].ewm(span=12, adjust= False).mean()
        ## Calculate the long term exponetial moving average (EMA) with 26 units
        self.df["long_EMA"] = self.df["close"].ewm(span=26, adjust=False).mean()
        ## MACD line
        self.df["MACD_line"] = (self.df["short_EMA"] - self.df["long_EMA"])
        # Signal line with 9 units
        self.df["Signal_line"] = self.df["MACD_line"].ewm(span=9, adjust= False).mean()

        # Histogram
        self.df["Hist"] = (self.df["MACD_line"] - self.df["Signal_line"])
       
        
    def buy_sell_signal(self):

        # Empy list
        buy = []
        sell = []
        # buy signal = 1
        # sell signal = -1
        macd_signal = []
        # This flag for detect if the price after crossing continues rising or decreasing
        # This flag only change if the two lines cross
        # Only when there's a momentum shift
        flag = 0
        # loop 
        for i in range(0, len(self.df)):
            if self.df["MACD_line"][i] > self.df["Signal_line"][i]:
                sell.append(0.0)
                if flag != 1:
                    buy.append(self.df["close"][i])
                    flag = 1
                    macd_signal.append(flag)
                else:
                    buy.append(0.0)
                    macd_signal.append(0)

            elif self.df["MACD_line"][i] < self.df["Signal_line"][i]:
                buy.append(0.0)
                if flag != -1:
                    sell.append(self.df["close"][i])
                    flag = -1
                    macd_signal.append(flag)
                else:
                    sell.append(0.0)
                    macd_signal.append(0)
            else:
                buy.append(0.0)
                sell.append(0.0)
                macd_signal.append(0)

        # Create new column
        self.df["macd_signal"] = macd_signal

        return (buy, sell)

    def BackTesting(self, invesment_value: int = 500):

        # Creating position
        # Condition:
        # If we hold the stock == 1
        # If we don't own or hold the stock == 0 
        position = []
        for i in range(len(self.df["macd_signal"])):
            if self.df["macd_signal"][i] > 1:
                position.append(0)
            else:
                position.append(1)
        
        for i in range(len(self.df["close"])):
            if self.df["macd_signal"][i] == 1:
                position[i] = 1
            elif self.df["macd_signal"][i] == -1:
                position[i] = 0
            else:
                position[i] = position[i-1]
        # Add a new column 
        self.df["macd_position"] = position

        # Strategy returns 
        # daily returns 
        self.df["daily_return"] = self.df["close"].pct_change(1)

        # drop missing values 
        self.df.dropna(inplace=True)
        # Empy list
        macd_strategy_ret = []
        # loop for
        for i in range(len(self.df["daily_return"])):
            try:
                returns = self.df["daily_return"][i] * self.df["macd_position"][i]
                macd_strategy_ret.append(returns)
            except:
                pass
        
        # add columns
        self.df["macd_strategy_ret"] = macd_strategy_ret

        # number of stocks
        number_of_stock = math.floor(invesment_value/self.df["close"][0])
        # Returns of inversions
        bm_invesment_ret = [number_of_stock*self.df["daily_return"][i] for i in range(len(self.df["daily_return"]))]
        macd_investment_ret = [number_of_stock*self.df["macd_strategy_ret"][i] for i in range(len(self.df["macd_strategy_ret"]))]

        # MACD Total Investment returns and Profit porcentage
        Total_investment_ret = round(sum(macd_investment_ret), 2) 
        Profit_percentage = math.floor((Total_investment_ret / invesment_value)*100)

        # BenchMark total incesment returns and profit porcentage
        Total_bm_investment_ret = round(sum(bm_invesment_ret), 2) 
        Profit_bm_percentage = math.floor((Total_bm_investment_ret/invesment_value)*100)
        # Performance 
        strat_performance =  Profit_percentage - Profit_bm_percentage 

        return (Total_investment_ret, Profit_percentage, Total_bm_investment_ret, Profit_bm_percentage, strat_performance)



## NEXT TASKS
# Add next indicator FMI 

class MFI():

    def __init__(self, ticker):
        
        self.ticker = ticker
    
    def get_indicator(self) -> pd.DataFrame:
        
        # Get daily data
        av = AlphaVantageApi()
        # Stored data into a object variable
        df =  av.get_daily(ticker = self.ticker)

        # typical price
        typical_price = (df["high"] + df["low"] + df["close"])/ 3
        # The MFI is usually calculated using 14 periods of price data
        period = 14
        # raw money flow
        money_flow = typical_price * df['volume']

        # get all positive and negative money flow 
        positive_flow = []
        negative_flow = []

        # loop for 
        for i in range(1, len(typical_price)):
            # Positive flow
            if typical_price[i] > typical_price[i-1]:
                positive_flow.append(money_flow[i-1])
                negative_flow.append(0)
            # negative flow
            elif typical_price[i] < typical_price[i-1]:
                negative_flow.append(money_flow[i-1])
                positive_flow.append(0)
            else:
                positive_flow.append(0)
                negative_flow.append(0)

        # get all positive and negative money flow within a period of time
        positive_mf = []
        negative_mf = []
        
        for i in range(period - 1, len(positive_flow)):
            positive_mf.append(sum(positive_flow[ i + 1 - period: i + 1]))
        for j in range(period - 1, len(negative_flow)):
            negative_mf.append(sum(negative_flow[ j + 1 - period: j +1]))
        
        # Claculate the money flow index
        mfi = 100 *(np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

        # Create a new dataframe
        self.new_df = pd.DataFrame()
        # Get all data starting from the periods units 
        self.new_df = df[period:]
        # Create a new column
        self.new_df["MFI"] = mfi

        

    def buy_sell_signal(self, high: int = 80, low: int = 20):
        
        # Empy list
        buy_signal = []
        sell_signal = []
        flag = 0
        mfi_signal = []

        # Loop for
        for i in range(len(self.new_df["MFI"])):
            # MFI above 80 - sell signal
            if self.new_df["MFI"][i] > high:
                buy_signal.append(0.0)
                if flag != -1:
                    sell_signal.append(self.new_df["close"][i])
                    flag = -1
                    mfi_signal.append(flag)
                else:
                    sell_signal.append(0.0)
                    mfi_signal.append(0)
            # MFI below 20 - buy signal
            elif self.new_df["MFI"][i] < low:
                sell_signal.append(0.0)
                if flag != 1:
                    buy_signal.append(self.new_df["close"][i])
                    flag = 1
                    mfi_signal.append(flag)
                else:
                    buy_signal.append(0.0)
                    mfi_signal.append(0)                
            else:
                buy_signal.append(0.0)
                sell_signal.append(0.0)
                mfi_signal.append(0)

        # add mfi signal to the dataframe
        self.new_df["mfi_signal"] = mfi_signal 

        return (buy_signal, sell_signal)

    def BackTesting(self, invesment_value: int = 500):

        # Creating position
        # Condition:
        # If we hold the stock == 1
        # If we don't own or hold the stock == 0 
        position = []
        for i in range(len(self.new_df["mfi_signal"])):
            if self.new_df["mfi_signal"][i] > 1:
                position.append(0)
            else:
                position.append(1)
        
        for i in range(len(self.new_df["close"])):
            if self.new_df["mfi_signal"][i] == 1:
                position[i] = 1
            elif self.new_df["mfi_signal"][i] == -1:
                position[i] = 0
            else:
                position[i] = position[i-1]
        # Add a new column 
        self.new_df["mfi_position"] = position

        # Strategy returns 
        # daily returns 
        self.new_df["daily_return"] = self.new_df["close"].pct_change(1)

        # drop missing values 
        self.new_df.dropna(inplace=True)
        # Empy list
        mfi_strategy_ret = []
        # loop for
        for i in range(len(self.new_df["daily_return"])):
            try:
                returns = self.new_df["daily_return"][i] * self.new_df["mfi_position"][i]
                mfi_strategy_ret.append(returns)
            except:
                pass
        
        # add columns
        self.new_df["mfi_strategy_ret"] = mfi_strategy_ret

        # number of stocks
        number_of_stock = math.floor(invesment_value/self.new_df["close"][0])
        # Returns of inversions
        bm_invesment_ret = [number_of_stock*self.new_df["daily_return"][i] for i in range(len(self.new_df["daily_return"]))]
        mfi_investment_ret = [number_of_stock*self.new_df["mfi_strategy_ret"][i] for i in range(len(self.new_df["mfi_strategy_ret"]))]

        # MFI Total Investment returns and Profit porcentage
        Total_investment_ret = round(sum(mfi_investment_ret), 2) 
        Profit_percentage = math.floor((Total_investment_ret / invesment_value)*100)

        # BenchMark total incesment returns and profit porcentage
        Total_bm_investment_ret = round(sum(bm_invesment_ret), 2) 
        Profit_bm_percentage = math.floor((Total_bm_investment_ret/invesment_value)*100)
        # Performance 
        strat_performance =  Profit_percentage - Profit_bm_percentage 

        return (Total_investment_ret, Profit_percentage, Total_bm_investment_ret, Profit_bm_percentage, strat_performance)

    
        







            

