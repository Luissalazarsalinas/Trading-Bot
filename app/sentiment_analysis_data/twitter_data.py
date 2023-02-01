import snscrape.modules.twitter as sntwitter
import pandas as pd


# Class
class TweetsData():

    def get_data(self, keyword: list, limit: int) -> pd.DataFrame:

        # Empy list 
        SM_container = []
        SMS_container = []
        ST_container = []

        # Search and loop for 
        for search in keyword:
            if search == "Stock Market":
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query="Stock Market").get_items()):
                    if i >= limit:
                        break
                    SM_container.append([tweet.date, tweet.user.username, tweet.likeCount, tweet.sourceLabel, tweet.rawContent])
            elif search == "Stock Market sentiment":
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query="Stock Market sentiment").get_items()):
                    if i >= limit:
                        break
                    SMS_container.append([tweet.date, tweet.user.username, tweet.likeCount, tweet.sourceLabel, tweet.rawContent])
            elif search =="Stocks":
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query="Stocks").get_items()):
                    if i >= limit:
                        break
                    ST_container.append([tweet.date, tweet.user.username, tweet.likeCount, tweet.sourceLabel, tweet.rawContent])

        # Dataframes 
        tweet_df_sm = pd.DataFrame(SM_container, columns=["Date", "User", "LikeCount", "SourceLabel", "Tweets"])
        tweet_df_sms = pd.DataFrame(SMS_container, columns=["Date", "User", "LikeCount", "SourceLabel", "Tweets"])
        tweet_df_st = pd.DataFrame(ST_container, columns=["Date", "User", "LikeCount", "SourceLabel", "Tweets"])

        # Contact the dataframes
        tweet_df = pd.concat([tweet_df_sm, tweet_df_sms, tweet_df_st], ignore_index=True)

        return tweet_df


## TASKS
# Clean the tweets data 




# # Query and limit
# query = ["Stock Market", "Stock Market sentiment","Stocks"]
# limit = 10

# # Dataframe form concat 
# tweet_df = pd.concat([tweet_df_sm, tweet_df_sms, tweet_df_st], ignore_index=True)

# # tweet_df.columns = ["Date", "LikeCount", "SourceLabel", "Tweets"]

# print(tweet_df)

# # # Save data to a csvfile 
# # tweet_df.to_csv("StockMarket_Tweets.csv", index = False)
