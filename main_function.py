from pykrx import stock
#from pykrx import bond
import time
from datetime import datetime
from dateutil.relativedelta import *
#from py_imessage import imessage
#import tweepy
#import os
import matplotlib.pyplot as plt
#import matplotlib.patches as patches
import schedule
def regression(x,y):
    n=len(x)
    X=sum(x)
    Y=sum(y)

    A=sum([xi**2 for xi in x])
    C=sum([xi*yi for xi, yi in zip(x,y)])
    D=X**2-n*A
    if(float(D)!=0.0):
        m=(X*Y - n*C) / float(D)
        b=(C*X - A*Y) / float(D)
    else:
        m=0
        b=0
    return(m,b)
def main():
    start_date=(datetime.now()-relativedelta(days=90)).strftime('%Y%m%d')
    end_date=datetime.now().strftime('%Y%m%d')
    print(start_date+" ~ "+end_date)
    data=[]
    name=[]
    simple_array=[]
    index_list=[]
    price_slope_list=[]
    ticker_list=[]

    for ticker in stock.get_market_ticker_list():
        ticker_list.append(ticker)
        print(stock.get_market_ticker_name(ticker))
        name.append(stock.get_market_ticker_name(ticker))
        df = stock.get_market_ohlcv(start_date, end_date, ticker)
        simple_array.append(df["종가"].values.tolist())
        #time.sleep(1)

    for i in range(len(ticker_list)):
        data.append([])
    for i in range(len(simple_array[0])-1):
        index_list.append(i)

    for i in range(len(ticker_list)):
        data[i].append(ticker_list[i])
        data[i].append(name[i])
        data[i].append(simple_array[i])
        temp_regression_coefficients=regression(index_list,simple_array[i])
        data[i].append(temp_regression_coefficients[0])
        data[i].append(temp_regression_coefficients[1])
        regression_line_temp=[]
        for j in range(len(simple_array[0])-1):
            regression_line_temp.append(j*temp_regression_coefficients[0]+temp_regression_coefficients[1])
        data[i].append(regression_line_temp)
        if temp_regression_coefficients[1]!=0.0:
            data[i].append(1000*temp_regression_coefficients[0]/temp_regression_coefficients[1])
        else:
            data[i].append(0.0)

    data.sort(key=lambda x:x[6],reverse=True)

    legend_list=[]
    plt.rcParams['font.family'] ='AppleGothic'
    plt.rcParams['axes.unicode_minus'] =False
    for i in range(5):
        colors=['red','orange','green','blue','purple']
        #plt.title(str(data[i][0])+ " "+ str(data[i][5])+"%")

        plt.figure(str(datetime.now()))
        plt.title(data[i][1])
        plt.plot(data[i][2],color=colors[i], label='')
        plt.plot(data[i][5],linestyle='dashed',color=colors[i],label=str(round(data[i][6],2)))
        plt.legend(loc="upper left")
        #below is the most recent closing price
        print(data[i][1][len(data[i][1])-1])
    plt.figure(str(datetime.now()))
    for i in range(5):
        colors=['red','orange','green','blue','purple']
        plt.plot(data[i][2],color=colors[i])
        legend_list.append(str(data[i][1]))
        plt.plot(data[i][5],linestyle='dashed',color=colors[i])
        legend_list.append(str(round(data[i][6],2)))
        plt.legend(legend_list, loc="upper left")

    plt.show()

#main()

def plot_graph():
    plt.close('all')
   
    plt.title('title')
    for i in range(3):
        print("countdown "+str(3-i))
        time.sleep(1)

        plt.plot([1,2,3,4,5,6,7,8,9,10])
    plt.show()
"""
def weekday_job(x, t=None):
    week = datetime.today().weekday()
    if t is not None and week < 5:
        schedule.every().day.at(t).do(x)
weekday_job(main, '17:30')
"""
def friday_job(x,t=None):
    schedule.every().friday.at(t).do(x)
friday_job(main,"17:10")
"""
def saturday_job(x,t=None):
    schedule.every().saturday.at(t).do(x)
saturday_job(main,"04:00")
"""
main()
while True:
    schedule.run_pending()
    time.sleep(20)
