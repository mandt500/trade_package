import talib as ta
import numpy as np

# 移動平均
# 代表値:分足(5,25,75), 日足(25,50,75), 週足(12,26,52), 月足(9,24,60)
def sma_temp(df, period=(25,50,75)):
    df["sma_s"]= df["Close"].rolling(period[0]).mean().round(2)
    df["sma_m"]= df["Close"].rolling(period[1]).mean().round(2) 
    df["sma_l"]= df["Close"].rolling(period[2]).mean().round(2)

# 移動平均（単一）
def sma(df,period=9):
    df["sma_"+str(period)]= df["Close"].rolling(period).mean().round(2)
    
# ボリンジャーバンド
def bb(df,period=25, sigma=2):
    df["bb_u"],df["bb_m"],df["bb_l"] = ta.BBANDS(df['Close'], timeperiod=period, nbdevup=sigma, nbdevdn=sigma, matype=0)
    
# MACD
def macd(df,fastperiod=12, slowperiod=26, signalperiod=9):
    df['macd'], df['signal'], df['hist'] = ta.MACD(df['Close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)

# RSI
def rsi(df,period=14):
    df["rsi"]=ta.RSI(df['Close'], timeperiod=period)
    
# 変化率:rate of change (percentage) （period=1,日足なら前日から何%増減したか）
def roc(df,period=9):
    df["roc"]=ta.ROC(df['Close'],timeperiod=period)
    
# モーメンタム
def mom(df,period=10):
    df["mom"]=ta.MOM(df['Close'],timeperiod=period)

# 加重移動平均
def wma(df,period=9):
    df["wma_"+str(period)]=ta.WMA(df['Close'],timeperiod=period)

# 指数移動平均
def ema(df,period=9):
    df["ema_"+str(period)]=ta.EMA(df['Close'],timeperiod=period)
    
# スローストキャスティクス
def stoch(df,fastK=14,slowK=3,slowD=3):
    df["slowk"],df["slowd"]=ta.STOCH(df['High'],df['Low'],df['Close'],fastk_period=fastK, slowk_period=slowK, slowd_period=slowD)   
    
# ファーストストキャスティクス
def stochf(df,K=14,D=3):
    df["fastk"],df["fastd"]=ta.STOCHF(df['High'],df['Low'],df['Close'],fastk_period=K, fastd_period=D)

# 分散
def var(df,period=5):
    df["var"]=ta.VAR(df["Close"],timeperiod=period)
    
# 相関 correlation corefficient
def cc(df,symbol,period=20):
    cor = [np.nan]*(period-1)
    for i in range(len(df["Close"])-period+1):
        x = np.array(df["Close"][i:i+period])
        y = np.array(symbol[i:i+period])
        cor.append(np.corrcoef(x,y)[0,1])
    df["cc"] = cor
    