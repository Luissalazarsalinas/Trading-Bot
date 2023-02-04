import requests
import pandas as pd
from sqlalchemy import create_engine, text
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


## Stored data into postgresql
class PostgreSQL():

    def __db_connection(self):
        ## Connection with the database
        postgresurl = (
            "postgresql+psycopg2://"
            f"{settings.database_username}:"
            f"{settings.database_password}@"
            f"{settings.database_hostname}:"
            f"{settings.database_port}/"
            f"{settings.database_name}"
            )
        self.engine = create_engine(
            postgresurl 
            ) 
    
    def insert_table(self, data: pd.DataFrame, table_name:str, if_exists:str = "replace"):
        # Connection
        self.__db_connection()

        ## Insert values into a database
        with self.engine.connect().execution_options(autocommit = True) as conn:
            n_inserted = data.to_sql(
                name= table_name,
                con= conn,
                if_exists= if_exists
                )

        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
        }

    def read_table(self, table_name:str):
        # Connection
        self.__db_connection()
        
        # # SQL QUERY
        # query = f"""SELECT * FROM {table_name}"""

        # read data
        with self.engine.connect().execution_options(autocommit = True) as conn:
            df = pd.read_sql(
                f'''SELECT * FROM "{table_name}"''',
                con= conn,
                parse_dates= "date",
                index_col= "date"
        )

        return df