from generate_k_chart import print_kchart
from get_stock_data import get_stock_data
import schedule
import time

def daily_fetch():
    print("Start to fetch data and print k chart.")
    print("--------------------------------")
    get_stock_data()
    print_kchart()
    
    
schedule.every().day.at("19:00").do(daily_fetch)


while True:
    schedule.run_pending()
    time.sleep(30)
