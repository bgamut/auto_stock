from pykrx import stock
from datetime import datetime
from dateutil.relativedelta import *
import schedule
import time
import gspread
from google.oauth2.service_account import Credentials
import tweepy
import requests
import json


# google sheets credential stuff
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("google_sheets_cred.json",scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1vf8i7XPTX6tCkEUcK53OX8tOY6KY1oLQh07_LAzd97I"
sheet = client.open_by_key(sheet_id)


#twitter credential stuff
twitter_access_token ="4603598128-pxL4o1VP5vEkzHYE73orFrVbcEOoVRz7MNyIBu0"
twitter_access_token_secret = "SsfyVzE0mIeKRH2gPvAwJPCpFsYp4MUVFC9o8arOv8uAe"
twitter_apikey = "SmZ6R21BWo7OM38JSjRZwR92R"
twitter_apikey_secret = "fn55gONiJRbYj97kG832dqg8WtfE1kiBU83xiw9FMbWVd9ZFLN"
twitter_bearer_token = "AAAAAAAAAAAAAAAAAAAAAFBa%2BgAAAAAA3MZg94rT87sIgIgAwQEfNqAc9Pw%3DEjWsmwPG6hZwSJcOvmR29mtXJGvUO46fuyPhgVfgs2XwkWbvqy"

client=tweepy.Client= tweepy.Client(
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret,
    consumer_key=twitter_apikey,
    consumer_secret=twitter_apikey_secret,
    bearer_token=twitter_bearer_token
)

#request module headers
headers={'content-type': 'application/json'}


def compare():

    # search korean stock name in finance.naver.com
    # search google sheets list
    name_list = sheet.sheet1.col_values(1)
    price_list = sheet.sheet1.col_values(2)
    search_targets = []
    matching_names=[]
    for i in range(len(name_list)):
        search_targets.append([name_list[i],price_list[i]])
    search_targets.pop(0)
    print(search_targets)


    start_date=(datetime.now()-relativedelta(days=5)).strftime('%Y%m%d')
    end_date=datetime.now().strftime('%Y%m%d')
    matching_targets=[]
    
    for ticker in stock.get_market_ticker_list():
        name=stock.get_market_ticker_name(ticker)
        for i in range(len(search_targets)):
            if name in search_targets[i]:
                df = stock.get_market_ohlcv(start_date, end_date, ticker)
                current_price=df["종가"].values.tolist()[-1]
                if int(search_targets[i][1])<current_price:
                    matching_targets.append([name,current_price,search_targets[i][1]])
                    matching_names.append(name)

    print(datetime.now().strftime('%Y-%m-%d'))
    if len(matching_targets)>0:
        for i in range(len(matching_targets)):  
            print(matching_targets[i][0]+ " : "+str(matching_targets[i][2])+" -> "+str(matching_targets[i][1]))
            #print("update_index = " +  str(name_list.index(matching_targets[i][0])+1))
            update_index = name_list.index(matching_targets[i][0])+1
            sheet.sheet1.update_cell(update_index,3,str(matching_targets[i][1]))
            
        #send patch message to server and turn on light
        r = requests.patch('https://express-api-bice.vercel.app/update_light/1',headers=headers,data=json.dumps({"power":"on"}))
        
        #post names to twitter
        #result=client.create_tweet(text=",".join(str(x) for x in matching_names))
        #print(result)
    else:
        print("none for today.")

        #turn off light
        r = requests.patch('https://express-api-bice.vercel.app/update_light/1',headers=headers,data=json.dumps({"power":"off"}))


compare()

def weekday_job(x, t=None):
    week = datetime.today().weekday()
    if t is not None and week < 5:
        schedule.every().day.at(t).do(x)

weekday_job(compare, '17:20')

while True:
    schedule.run_pending()
    time.sleep(20)
