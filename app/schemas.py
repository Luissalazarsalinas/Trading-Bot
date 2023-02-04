import pandas as pd
from datetime import datetime
from pydantic import BaseModel

## Schemas 
class Strategyin(BaseModel):
    ticker: str
    invesment_mount: int
    add_new_data: bool

class MacdOut(Strategyin):
    
    index: list
    close_price: list
    macd_line: list
    signal_line: list
    histogram: list
    buy_signal: list
    sell_signal: list
    total_inves_ret: int
    profit_percentage: int
    total_bm_invs_ret: int
    profit_bm_percentage: int
    performance_strategy: int
    message: str

# MFI
class MfiOut(Strategyin):

    index: list
    close_price:list
    buy_signal: list
    sell_signal: list
    mfi_indicator: list
    buy_signal: list
    sell_signal: list
    total_inves_ret: int
    profit_percentage: int
    total_bm_invs_ret: int
    profit_bm_percentage: int
    performance_strategy: int
    message: str


class Deeplearningin(BaseModel):
    
    Teewts: str

# # Ml strategy
# class MlOut(Strategyin):

#     accuracy: float
#     roc_auc:float
#     f1_score:float
#     total_inves_ret: int
#     profit_percentage: int
#     total_bm_invs_ret: int
#     profit_bm_percentage: int
#     message: str
