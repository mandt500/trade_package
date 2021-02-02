import mplfinance as mpf

# ローソク足でプロット(panel="lower"で下のグラフにプロット)
# パネルに複数のデータを追加可能だが、未対応（暇なときにする）
def plot(df, add = None, volume=False,panel =None,title="", figratio=(16,9)):
    if(add is None):
        mpf.plot(df, figratio=(16,9), volume=volume, style='yahoo', type='candle',title="\n"+title)
    else:
        if(panel is None):
            apd = mpf.make_addplot(add)
        else:
            apd = mpf.make_addplot(add, panel=panel)        
        mpf.plot(df,addplot=apd, figratio=(16,9), volume=volume, style='yahoo', type='candle', title="\n"+title)
        
# 表を出力（引数：df,列の幅）
def table(df,col_width):
    import plotly.graph_objects as go
    from datetime import datetime
    
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    rowColorList = []
    for i in range(len(df.index)):
        if(i%2 == 0):
            rowColorList.append(rowOddColor)
        else:
            rowColorList.append(rowEvenColor)
    
    fig = go.Figure(data=[go.Table(
            columnwidth = col_width,
            header=dict(values=["<b>"+i+"</b>" for i in df.columns], align='center', line_color='darkslategray',\
                        fill_color=headerColor, font=dict(color='white', size=16), height=40),
            cells=dict(values=df.values.T, align='center', line_color='darkslategray',\
                       fill_color = [rowColorList*len(df.columns)],font = dict(color = 'black', size = 14), height=28)
            )])
    fig.update_layout(margin = dict(     # グラフ領域の余白設定
          l = 1, r = 1, t = 0, b = 0,
          pad = 0,         # グラフから軸のラベルまでのpadding
          autoexpand = True,  # LegendやSidebarが被ったときに自動で余白を増やすかどうか
        ))     
    # fig.update_layout(title={'text': title,'y':0.85,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
    # fig.layout.title.font.size= 24 #タイトルフォントサイズの変更
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    fig.write_image("table_"+now+".jpg",height=(len(df.index))*28+40+1)#, width=sum(col_width))
            