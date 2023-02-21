# from fastapi import APIRouter, status
# from app.trading_strategy import MFI
# from app.schemas import Strategyin, MfiOut


# # Intance to the router
# router = APIRouter(
#     prefix= "/mfi",
#     tags = ["MFI"]
# )


# # ENDPOINT 
# @router.post("/", status_code = status.HTTP_201_CREATED, response_model= MfiOut)
# def macd_strategy(data: Strategyin):
#     # Get a dict for the results
#     response = data.dict()
#     #
#     try:
#          mfi = MFI(ticker= data.ticker, new_data= data.add_new_data)

#          # Get dataframe with componen of the indicator 
#          mfi.get_indicator()
#          # sell and buy signal
#          buy_sell_siganl = mfi.buy_sell_signal()

#          # buy signal
#          buy_signal = buy_sell_siganl[0]
#          #sell signal
#          sell_signal = buy_sell_siganl[1]
#          # Backtesting 
#          backtesting = mfi.BackTesting(invesment_value = data.invesment_mount)
         
#          # index
#          response["index"] = list(mfi.new_df.index)
#          # close prince 
#          response["open_price"] = list(mfi.new_df["open"])
#          # close prince 
#          response["close_price"] = list(mfi.new_df["close"])
#          # macd line
#          response["mfi_indicator"] = list(mfi.new_df["MFI"])
#          # buy signal
#          response["buy_signal"] = buy_signal[1:]
#          # sell signal
#          response["sell_signal"] = sell_signal[1:]
#          # invesment and profit from strategy 
#          response["total_inves_ret"] = backtesting[0]
#          response["profit_percentage"] = backtesting[1]
#          # invesment and profit from benchmark 
#          response["total_bm_invs_ret"] = backtesting[2]
#          response["profit_bm_percentage"] = backtesting[3]

#          # Performance 
#          response["performance_strategy"] = backtesting[4]

#          # message
#          response["message"] = "All it's ok"

#     except Exception as e:
        
#         # index
#         response["index"] = []
#         # close prince 
#         response["open_price"] = []
#         # close prince 
#         response["close_price"] = []
#         # macd line
#         response["mfi_indicator"] = []
#         # buy signal
#         response["buy_signal"] = []
#         # sell signal
#         response["sell_signal"] = []
#         # invesment and profit from strategy 
#         response["total_inves_ret"] = 0
#         response["profit_percentage"] = 0
#         # invesment and profit from benchmark 
#         response["total_bm_invs_ret"] = 0
#         response["profit_bm_percentage"] = 0
#         # Performance 
#         response["performance_strategy"] = 0
#         # message
#         response["message"] =str(e) 
        
#     return response