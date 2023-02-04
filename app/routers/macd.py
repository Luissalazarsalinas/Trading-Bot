from fastapi import APIRouter, status
from sqlalchemy import create_engine
from app.trading_strategy import MACD
from app.schemas import Strategyin, MacdOut

# Intance to the router
router = APIRouter(
    prefix = "/macd",
    tags = ["MACD"]
)


# ENDPOINT 
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= MacdOut)
def macd_strategy(data: Strategyin):
     
     # Create connection an
     # Get a dict for the results
     response = data.dict()
     #
     try:
          macd = MACD(ticker= data.ticker, new_data= data.add_new_data)

          # Get dataframe with componen of the indicator 
          macd.get_indicator()
          # sell and buy signal
          buy_sell_siganl = macd.buy_sell_signal()

          # buy signal
          buy_signal = buy_sell_siganl[0]
          #sell signal
          sell_signal = buy_sell_siganl[1]
          # Backtesting 
          backtesting = macd.BackTesting(invesment_value = data.invesment_mount)
         
          # index
          response["index"] = list(macd.df.index)
          # close prince 
          response["close_price"] = list(macd.df["close"])
          # macd line
          response["macd_line"] = list(macd.df["MACD_line"])
          # signal line
          response["signal_line"] = list(macd.df["Signal_line"])
          # signal line
          response["histogram"] = list(macd.df["Hist"])
          # buy signal
          response["buy_signal"] = buy_signal[1:]
          # sell signal
          response["sell_signal"] = sell_signal[1:]
          # invesment and profit from strategy 
          response["total_inves_ret"] = backtesting[0]
          response["profit_percentage"] = backtesting[1]
          # invesment and profit from benchmark 
          response["total_bm_invs_ret"] = backtesting[2]
          response["profit_bm_percentage"] = backtesting[3]

          # Performance 
          response["performance_strategy"] = backtesting[4]
          # message
          response["message"] = "All it's ok"

     except Exception as e:

         # index
         response["index"] = []
         # Close price
         response["close_price"] = []
         # macd line
         response["macd_line"] = []
         # signal line
         response["signal_line"] = []
         # signal line
         response["histogram"] = []
         # buy signal 
         response["buy_signal"] = []
         # sell signal
         response["sell_signal"] = []
         # invesment and profit from strategy 
         response["total_inves_ret"] = 0
         response["profit_percentage"] = 0
         # invesment and profit from benchmark 
         response["total_bm_invs_ret"] = 0
         response["profit_bm_percentage"] = 0
         # Performance 
         response["performance_strategy"] = 0
         # message
         response["message"] =str(e) 
         
     return response




