import pandas as pd
import json
import numpy as np

# NYダウ
def dj():
    DJ=['AAPL','AXP','BA','CAT','CSCO','CVX','DIS','GS','HD',
        'IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE',
        'PFE','PG','TRV','UNH','UTX','V','VZ','WBA','WMT','XOM']
    return DJ

# 代表的な指数
def index():
    INDEX=["^DJI","^DJT","^DJU","^BANK","^IXCO","^NDX","^NBI",
           "^NDXT","^INDS","^INSR","^OFIN","^IXTC","^TRAN","^NYY","^NYI","^NY",
           "^NYL","^XMI","^OEX","^GSPC","^HSI","^FCHI","^BVSP","^N225","^RUA","^XAX"]
    return INDEX

# 日経平均株価（csvファイル必須）
def n225():
    n225 = pd.read_csv("./trade_package/data/market_info/nikkei225_all_code.csv", engine="python", names=("code","name"))
    return n225

# TPIX500（csvファイル必須）
def topix500():
    topix500 = pd.read_csv("./trade_package/data/market_info/topix500_all_code.csv", engine="python", names=("code","name"),usecols=[0,1])
    return topix500

# Mothers上場銘柄（csvファイル必須）
def mothers():
    mothers = pd.read_csv("./trade_package/data/market_info/mothers_all_code.csv", engine="python", names=("code","name"))
    return mothers
    
# 東証全銘柄
def tokyo():
    tokyo = pd.read_csv("./trade_package/data/market_info/tokyo_all_code.csv", engine="python", names=("date","code", "name","market", "CodeIndustry33", "ClassificationIndustry33", "CodeIndustry17", "ClassificationIndustry17", "CodeScale", "ClassificationScale"), skiprows=1, usecols=[1,2], encoding="utf-8")
    return tokyo

# sp100
def sp100():
    SP100=["AAPL","ABBV","ABT","ACN","AGN","AIG","ALL","AMGN","AMZN","AXP","BA","BAC","BIIB",
           "BK","BLK","BMY","BRKB","C","CAT","CHTR","CL","CMCSA","COF","COP","COST","CSCO",
           "CVS","CVX","DHR","DIS","DUK","EMR","EXC","F","FB","FDX","FOX","FOXA","GD","GE",
           "GILD","GM","GOOG","GOOGL","GS","HAL","HD","HON","IBM","INTC","JNJ","JPM","KHC","KMI",
           "KO","LLY","LMT","LOW","MA","MCD","MDLZ","MDT","MET","MMM","MO","MRK","MS","MSFT",
           "NEE","NKE","ORCL","OXY","PEP","PFE","PG","PM","PYPL","QCOM","RTN","SBUX",
           "SLB","SO","SPG","T","TGT","TXN","UNH","UNP","UPS","USB","UTX","V","VZ","WBA",
           "WFC","WMT","XOM"]
    return SP100

# 暗号通貨
def cc():
    CCURRENCY=["BTC-USD","XRP-USD","ETH-USD","LTC-USD","BCH-USD","BNB-USD",
               "EOS-USD","USDT-USD","LINK-USD","TRX-USD","ADA-USD",
               "XLM-USD","XMR-USD","DASH-USD","NEO-USD","IOT-USD",
               "VEN-USD","ETC-USD","XEM-USD","ZEC-USD","XRB-USD","QTUM-USD",
               "BTG-USD","BAT-USD","DOGE-USD"]
    return CCURRENCY

# 株価取得
def price(code, start=None, end=None):
    df = pd.read_csv("./trade_package/data/price/"+code+".csv",index_col=0, parse_dates=True)
    return df[start:end]

# 日足→〇足/分足→〇足
# [freq] W-MON：週足 MS:月足 30T:30分足 4H:4時間足
def change(df,freq):
    d_ohlcv = {'Open': 'first',
           'High': 'max',
           'Low': 'min',
           'Close': 'last',
           'Volume': 'sum'}
    df = df.resample(freq, closed='left', label='left').agg(d_ohlcv)
    return df

 # 銘柄情報       
def stock_info(stock_code :list):
    info   = {} # 銘柄情報
    for code in stock_code:
        # print(stock_name, 'SEACH... ', end='')
        try:
            with open(f"./trade_package/data/stock_info/{code}.json", mode="r") as f:
                d = json.load(f)
            info[code]={'sharesOutstanding':d["sharesOutstanding"], # 発行株式数
                                'forwardPER': d["forwardPE"],               # 予測PER
                                'marketCap': d["marketCap"],                # 時価総額
                                'dividendYield': d['dividendYield'],        # 配当利回り
                                'profitMargins':d['profitMargins'],         # 純利益比率
                                } # dataframeにinfoの項目を追加するにはここを追加する
            # print('SUCCESS')
        except Exception as e:
            info[code]=np.nan
            print('FAIL:', e)
    info = pd.DataFrame(info)
    return info

# 損益計算書
def finance(stock_code:list, item):
    # dummy作成
    dummy = pd.read_csv('./trade_package/data/finance/'+stock_code[0]+'.csv', index_col=0).T[item]
    dummy[:] = np.nan
    
    earnings = {}
    for code in stock_code:
        try:
            earnings[code] = pd.read_csv('./trade_package/data/finance/'+code+'.csv', index_col=0).T[item]
        except:
            earnings[code] = dummy # エラー発生時はダミーを入れる
    return pd.DataFrame(earnings)

# バランスシート
def bs(stock_code:list, item):
    equity   = {} # 自己資本
    dummy = pd.read_csv('./trade_package/data/balance_sheet/'+stock_code[0]+'.csv', index_col=0).T[item]
    dummy[:] = np.nan
    
    for code in stock_code:
        try:
            equity[code] = pd.read_csv('./trade_package/data/balance_sheet/'+code+'.csv', index_col=0).T[item]
        except:
            equity[code] = dummy # エラー発生時はダミーを入れる
    return pd.DataFrame(equity)
    