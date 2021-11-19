import os
import csv
import pandas as pd
import talib
from flask import Flask, render_template, request
from patterns import candlestick_patterns

app = Flask(__name__)


@app.route('/')
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}

    with open('stocks.csv', encoding='utf-8') as f:
        for row in csv.reader(f):
            if row[0] == 'code':  # skip the first row
                continue
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        data_files = os.listdir('./stock_data')
        for data_set in data_files:
            df = pd.read_csv(f'./stock_data/{data_set}')
            pattern_function = getattr(talib, pattern)

            symbol = data_set.split('.c')[0]

            result = pattern_function(
                df['open'], df['high'], df['low'], df['close'])
            last = result.tail(1).values[0]
            if last > 0:  # bullish
                stocks[symbol][pattern] = 'bullish'
            elif last < 0:  # bearish
                stocks[symbol][pattern] = 'bearish'
            else:
                stocks[symbol][pattern] = None

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)


@app.route('/stock')
def stock():
    return{
        'code': 'success'
    }

    # $env:FLASK_ENV = "development"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
