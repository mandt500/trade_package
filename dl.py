import pandas as pd
import requests
from io import StringIO
import json
from datetime import datetime,date
import glob
import pandas_datareader.data as web
import yfinance as yf

# 新規で株価取得（日足,1銘柄）
def price(stock_code,start=None,end=None):
    data = web.DataReader(stock_code,"yahoo",start,end)
    return data

# 新規で株価取得、csv保存（日足,1銘柄）
def price_csv(stock_code,start=None,end=None):
    data = web.DataReader(stock_code,"yahoo",start,end)
    data.to_csv('./trade_package/data/price\\'+stock_code+'.csv') 

# 新規株価の取得と既存株価の更新（日足,銘柄リスト）
def price_update(stock_code:list,day=date.today()):
    list_file_exist = glob.glob("./trade_package/data/price/*")
    print("update_day:", end='')
    print(day)
    for code in stock_code:
        filename = './trade_package/data/price\\'+code+'.csv'
        if filename in list_file_exist:
            df = pd.read_csv(filename,index_col=0,parse_dates=True)
            if(df.index[-1]==day):
                pass
            else:
                print(code, 'UPDATE... ', end='')
                try:
                    new_df = price(code, start=df.index[-1].date())
                    df = pd.concat([df, new_df.iloc[1:,:]])
                    df.to_csv(filename)
                    print('SUCCESS')
                except Exception as e:
                    print('FAIL:', e)            
        else:
            print(code, 'GET... ', end='')
            try:
                price_csv(code, start='2015-1-1')
                print('SUCCESS')
            except Exception as e:
                print('FAIL:', e)  
                              
# 損益計算書データ取得 csv保存
def balance_sheet_csv(stock_code):
    data = yf.Ticker(stock_code).balance_sheet
    data.to_csv("./trade_package/data/balance_sheet/"+stock_code+".csv")

# キャッシュフロー計算書取得 csv保存
def cashflow_csv(stock_code):
    data = yf.Ticker(stock_code).cashflow
    data.to_csv("./trade_package/data/cashflow/"+stock_code+".csv")
    
# 貸借対照表（バランスシート）取得 csv保存
def finance_csv(stock_code):
    data = yf.Ticker(stock_code).financials
    data.to_csv("./trade_package/data/finance/"+stock_code+".csv")
    
# 銘柄のサマリー取得 csv保存
def stock_info_csv(stock_code):
    data = yf.Ticker(stock_code).info
    with open(f"./trade_package/data/stock_info/{stock_code}.json", mode="w") as f:
        d = json.dumps(data)
        f.write(d)

# finance, stock_info, cashflow，balance_sheetを指定した銘柄で保存する
def fundamental_csv(stock_code):
    balance_sheet_csv(stock_code)
    cashflow_csv(stock_code)
    finance_csv(stock_code)
    stock_info_csv(stock_code)
        
# price, finance, stock_info, cashflow，balance_sheetを指定した銘柄すべて保存する
def all_csv(stock_code:list):
    price_update(stock_code)
    print("Next:Download Fundamental")
    for code in stock_code:
        print(code)
        fundamental_csv(code)      
        
# 株価取得（分足）
# 最大：直近7日分
# やりすぎるとIPアドレスをbanされるリスクあり（1銘柄1分程度のインターバルが必要らしい）    
def get_price_m(stock_name,day=1):
    if(day>7):
        print("day≦7")
        day = 1
    URL="https://query1.finance.yahoo.com/v7/finance/chart/"+stock_name+"?range="+str(day)+"d&amp;interval=1m&amp;indicators=quote&amp;includeTimestamps=true"
    r = requests.get(URL)
    s = StringIO(r.text)
    j = json.load(s)
    df = pd.DataFrame()
    df['Date'] = [datetime.fromtimestamp(ts) for ts in j['chart']['result'][0]['timestamp']]
    df['Open'] = j['chart']['result'][0]['indicators']['quote'][0]['open']
    df['Low'] = j['chart']['result'][0]['indicators']['quote'][0]['low']
    df['High'] = j['chart']['result'][0]['indicators']['quote'][0]['high']
    df['Close'] = j['chart']['result'][0]['indicators']['quote'][0]['close']
    df['Volume'] = j['chart']['result'][0]['indicators']['quote'][0]['volume']
    return df    