import requests
import pandas as pd
from app.config import settings




class AlphaVantageApi():

    def __init__(self, api_key = settings.api_key):

        self.__api_key = api_key
    
    # methods
    def get_daily(self, ticker: str, output_size: str = "full"):


        # Api url to make the request
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY_ADJUSTED&"
            f"symbol={ticker}&"
            f"outputsize={output_size}&"
            f"apikey={self.__api_key}"
        )

        # Request
        response = requests.get(url=url)
        # Convert response to a python data-structure
        response_data = response.json()
        # Check if there is a error
        if "Time Series (Daily)" not in response_data:
            raise Exception(
                f"Invalic API call check that ticker symbol {ticker} is correct"

            )
        # Stored stock daily data in a variable
        stock_data = response_data.get("Time Series (Daily)")

        # Convert data into a dataframe
        df = pd.DataFrame.from_dict(stock_data, dtype= float).T
        # Create a datetime index
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        # Trund columns name
        df.columns = [c.split(". ")[1] for c in df.columns]
        # Sort data
        df.sort_index(ascending=True, inplace= True)

        return df