import time
import os
import baostock as bs
import pandas as pd
from tqdm import tqdm

fields = 'date, code, open, high, low, close, volume'



def get_stock_data(start_date='2018-01-01'):
    
    if not os.path.exists('./stock_data'):
        os.mkdir('./stock_data')

    lg = bs.login()

    rs_300 = bs.query_hs300_stocks()

    hs300_stocks = []
    while (rs_300.error_code == '0') & rs_300.next():
        hs300_stocks.append(rs_300.get_row_data())
    hs300_result = pd.DataFrame(hs300_stocks, columns=rs_300.fields)[
        ['code', 'code_name']]

    append_df = pd.DataFrame({
        'code': ['sh.000001', 'sz.399106', 'sh.000300'],
        'code_name': ['上证指数', '深证综指', '沪深300']
    })

    stocks = append_df.append(hs300_result, ignore_index=True)

    path = './stock_data'
    if not os.path.exists(path):
        os.mkdir(path)

    stocks_iter = tqdm(stocks.iterrows(), total=len(stocks))
    
    for index, row in stocks_iter:
        stocks_iter.set_description('Downloading data of ' + row['code'])
        this_code = row['code']
        this_stock = row['code_name']

        rs = bs.query_history_k_data(
            this_code, fields, start_date=start_date, frequency='d')

        data_list = []
        while(rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        result.to_csv(f"./stock_data/{this_code}.csv", index=False)

    bs.logout()

if __name__ == '__main__':
    get_stock_data()

