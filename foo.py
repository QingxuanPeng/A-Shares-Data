import pandas as pd
import os.path
from  datetime  import  *
import tushare as ts
def newfilename(code):
    '''make a clear name of the file containing individual stock data we will created at the first time'''
    #000001.SZ ->sz00001.csv
    a = code.split('.')
    if len(a)==1:
        return f'{a[0]}.csv'
    return f'{a[1]}_{a[0]}.csv'

def syn_stock(dir,row):
    '''get the China A stock information from tushare api (there is a test token of tushare. if
    cannot get valid information, you can create a account of tushare, then you will
    have a personal token:https://waditu.com/)'''
    try:
        # use tushare api with test token
        pro = ts.pro_api('76d6655af61d2d8b58e947b5b3573685ce1a04234b50aa0816ceb315')

        code=row["股票代码"]
        mode=row["增量更新"]

        dt = datetime.now()
        # get present time information(class is datetime)
        ed = dt.strftime('%Y%m%d')
        # change class from datetime to str
        st = '20020314'
        # the day a long time ago as the first day you want to see the information of stocks(can be changed)

        fn = dir + '/'+ newfilename(code)
        # store every stock's information as a file and saved in the path of dir(which is data file made
        # in main.py) and make the name of it by newfilename function

        if mode == 'Y' and row['结束日期'] and os.path.isfile(fn):
            # if the mode should be incremental updating and there is a file containing old information of
            # that stock,
            st = row['结束日期']
            dtst = datetime.strptime(str(st), "%Y%m%d")
            st = (dtst+timedelta(days=1)).strftime("%Y%m%d")
            # make start date later one day
        if ed < st:
            # if have already got the newest information last time, return to avoid repetition
            return
        df = pro.daily(ts_code=code, start_date=st, end_date=ed)
        # the ts_code is got by tushare_list function actually
        # get a dataframe containing a China A stock information by tushare api from the start date to
        # the end date we made before. if the mode is not incremental updating, we will get the information
        # from 20020314 to now.but if the mode is incremental updating, the start date will change in the
        # next(maybe not from 20020314 because there were some stocks appeared later)

        newdf = pd.DataFrame()
        # create a new empty dataframe and add the information of a specific stock respectively
        newdf['股票代码'] = df['ts_code']
        newdf['股票名称'] = row['股票名称']
        newdf['交易日期'] = df['trade_date']
        newdf['开盘价'] = df['open']
        newdf['最高价'] = df['high']
        newdf['最低价'] = df['low']
        newdf['收盘价'] = df['close']
        newdf['前收盘价'] = df['pre_close']
        newdf['涨跌额'] = df['change']
        newdf['涨跌幅'] = df['pct_chg']
        newdf['流通市值'] = df['vol']
        newdf['总市值'] = df['amount']

        if mode == 'Y' and os.path.isfile(fn):
            # if there was a file containing old information of that stock and the mode should be incremental
            # updating
            old_df = pd.read_csv(fn)
            newdf = pd.concat([newdf, old_df], axis=0)
            # make the new part of the information and the old part of information together in the same dataframe

        row["更新时间"] = dt.strftime('%Y-%m-%d %H:%m:%S')
        # get the updating time now

        if not df['trade_date'].empty:
            # only when there was a time information of that stock will get the earliest(will not be earlier
            # than the start date we made at the first time:20020314)trade date or will cause index error
            row['开始日期'] = newdf['交易日期'].iloc[-1]
        row['结束日期'] = ed
        # the last trade date is the last time we get valid information

        newdf.to_csv(fn,index=False)

    except Exception as e:
        print('except')
        print(str(e))
    finally:
        pass


def tushare_list():
    '''get the China A stock basis list from tushare api, we only use stock code and name here'''
    pro = ts.pro_api('2b1cbfed5b4bb9db8241cb61aad9a231945f6e52d671495dbeef1440')

    # 查询当前所有正常上市交易的股票列表

    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data
if __name__ == '__main__':
   print(tushare_list())