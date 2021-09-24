import os
import shutil
import mplfinance as mpf
import pandas as pd


def get_kchart(src):
    df = pd.read_csv(f'.\stock_data\{src}.csv')
    data = df.drop(columns='code')
    data.index = pd.DatetimeIndex(data['date'])

    save = dict(fname=f'.\k_chart\{src}.jpg', dpi=80, pad_inches=0.25)
    mpf.plot(data.tail(100), type='candle',
             volume=True, savefig=save, style='yahoo')


def clear_kchart_buffers():
    path = '.\k_chart'
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)


if __name__ == '__main__':
    get_kchart('sh.600000')
    src_path = '.\k_chart'
    src_list = os.listdir(src_path)
    print(src_list)
