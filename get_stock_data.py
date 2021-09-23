import time
import baostock as bs
import pandas as pd

fields = 'date, code, open, high, low, close, volume'

time_start = time.time()

lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

rs_300 = bs.query_hs300_stocks()

hs300_stocks = []
while (rs_300.error_code == '0') & rs_300.next():
    hs300_stocks.append(rs_300.get_row_data())
hs300_result = pd.DataFrame(hs300_stocks, columns=rs_300.fields)[
    ['code', 'code_name']]
hs300_result.to_csv('.\hs300.csv', index=False)

stocks = pd.read_csv('.\hs300.csv')

for index, row in stocks.iterrows():
    this_code = row['code']
    this_stock = row['code_name']

    rs = bs.query_history_k_data(
        this_code, fields, start_date='2020-01-01', frequency='d')
    print(f"Collecting klines: {this_code}")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond error_msg:'+rs.error_msg)
    print('-------------------------------------------------------------')
    data_list = []
    while(rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv(f".\stock_data\{this_code}.csv", index=False)

time_end = time.time()
time_sum = round(time_end - time_start, 2)
print(f"Takes up {time_sum}s to complete collecting data.")
