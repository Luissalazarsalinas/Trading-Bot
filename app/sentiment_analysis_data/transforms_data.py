## data Tansform
import re
import string
import pandas as pd
from twitter_data import TweetsData

# Instance
td = TweetsData()
# Keyworks and limit
keywords = ["Stock Market", "Stock Market sentiment","Stocks"]
limit = 5000

# get data
raw_data = td.get_data(keywords, limit)

# wranglering and cleaning 
def wrangle(data: pd.DataFrame):

    # Copy
    data_c = data.copy(deep=True)

    # Drop unnecesaries data
    data_un = ["Date", "User", "LikeCount", "SourceLabel"]
    data_c.drop(columns= data_un, inplace=True)

    return data_c

def cleaning(text):

    text = str(text).lower()
    text = re.sub(r"\[.*\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "",  text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), "", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"w*\d\w*", "", text)
    text = re.sub(r"#[A-Za-z0-9]+", "", text)

    return text

## Apply funtions 
# wrangle
data = wrangle(raw_data)
# cleaning 
data["Tweets"] = data["Tweets"].apply(cleaning)


#  Stored data into a csv file
data.to_csv("Tweets_data.csv", index= False)
    
