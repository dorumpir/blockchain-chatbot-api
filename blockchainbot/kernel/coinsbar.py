import os
from functools import reduce

import tushare as ts
from datetime import datetime, timedelta, timezone
from blockchainbot.utils.switch import switch

import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num

import requests


class CoinsBar:

    def __init__(self, ts_token, mongo, pic_path):
        self.pro = ts.pro_api(ts_token)
        self.mongo = mongo
        self.pic_path = pic_path
        self.tz_utc_8 = timezone(timedelta(hours=8))

    @staticmethod
    def cal_ratio(open_price, close_price):
        return (close_price - open_price) / close_price * 100

    @staticmethod
    def cal_width(series):
        width = max(series) - min(series)
        return width

    def _ask_period_mongo(self, coin, step):
        price_list = []
        width_list = []
        ratio_list = []
        price_period = []
        latest_price_list = []
        price_timestamp_list = []
        import time
        import pymongo
        from operator import itemgetter
        from itertools import groupby
        if not hasattr(self, 'mongo_coin_prices_collection'):
            host = '124.65.136.106'
            port = 55119
            conn = pymongo.MongoClient(host=host, port=port, tz_aware=False)
            db = conn.get_database('ai_block_chain_crawler')
            col = db.get_collection('coin_prices')
            self.mongo_coin_prices_collection = col
        col = self.mongo_coin_prices_collection
        coin = coin.lower()
        def coin_realname(coin):
            coin_alias = {'zcash': 'zec', 'gin': 'ors', 'smart': 'smt', 'tronix': 'trx', 'zilliqa': 'zil'}
            return coin_alias.get(coin, coin) 
        ts_24hour_ago = int(time.time() - 24*60*60)
        ts_1hour_ago = int(time.time() - 1*60*60)
        ts_20min_ago = int(time.time() - 20*60)
        records = list(col.find({'symbol': coin_realname(coin)+'usdt', 'timestamp': {'$gt': ts_20min_ago}}).sort('timestamp', 1))
        records.sort(key=itemgetter('exchange'))
        for exchange, items in groupby(records, key=itemgetter('exchange')):
            print(exchange)
            itemslist = list(items)
            if itemslist[-1]['price'] <= 0:
                print('-> invalid price data in %s: %s' % (exchange, itemslist[-1]['price']))
                continue
            price_list.append(itemslist[-1]['price'])
            width_list.append(itemslist[-1]['width_24h'])
            ratio_list.append(itemslist[-1]['ratio_24h'])
            price_timestamp_list.append(itemslist[-1]['timestamp'])
            price_period.append([x['price'] for x in itemslist])
        avg_latest_price = sum(price_list) / len(price_list)
        avg_latest_width = sum(width_list) / len(width_list)
        avg_latest_ratio = sum(ratio_list) / len(ratio_list)
        avg_price_period = reduce(lambda X, Y: [(x+y) for x, y in zip(X, Y)], price_period)
        avg_price_period = list(map(lambda x: x/len(price_period), avg_price_period))
        latest_price_timestamp = max(price_timestamp_list)
        return_pak = {
            "msg": "ok",
            "avg_latest_price": avg_latest_price,
            "avg_latest_width": avg_latest_width,
            "avg_latest_ratio": avg_latest_ratio,
            "avg_price_period": avg_price_period,
            "price_list": latest_price_list,
            "latest_timestamp": latest_price_timestamp,
        }
        return return_pak

    def ask_period(self, coin, step):
        return self._ask_period_mongo(coin, step)

        price_list = []
        price_period = []
        huobi_url = "https://widget.aicoin.net.cn/chart/api/data/period?symbol=huobipro%susdt&step=%s" % (coin, step)
        okex_url = "https://widget.aicoin.net.cn/chart/api/data/period?symbol=okex%susdt&step=%s" % (coin, step)
        bittrex_url = "https://widget.aicoin.net.cn/chart/api/data/period?symbol=bittrex%susdt&step=%s" % (coin, step)
        import grequests
        urls = [huobi_url, okex_url, bittrex_url]
        tasks = [grequests.get(url) for url in urls]
        responses = grequests.map(tasks)
        for r in responses:
            if r and r.json().get("data", None):
                print(r.url)
                json_data = r.json()
                if json_data.get("data"):
                    latest_price_list = json_data.get("data")
                    latest_price = latest_price_list[-1][4]
                    price_list.append(latest_price)
                    price_period.append([x[4] for x in latest_price_list])
        ###################################################
        avg_latest_price = sum(price_list) / len(price_list)
        avg_price_period = reduce(lambda X, Y: [(x+y) for x, y in zip(X, Y)], price_period)
        avg_price_period = list(map(lambda x: x/len(price_period), avg_price_period))
        return_pak = {
            "msg": "ok",
            "avg_latest_price": avg_latest_price,
            "avg_price_period": avg_price_period,
            "price_list": latest_price_list,
        }
        return return_pak

    def find_pairs(self, coin):
        '''

        :param coin:
        :return:
        '''
        coin = coin.lower()
        db = self.mongo.connection("block_chain_basedata")
        cursor = db["exchange_pairs"].find({}, {"exchange": 1, "ts_pair": 1})
        pair_in_exchange = []
        for item in cursor:
            pair_list = [x for x in item.get("ts_pair")]
            exchange = item.get("exchange")
            for pair in pair_list:
                if ("%susdt"%coin == pair) or ("%susd"%coin == pair):
                    pair_in_exchange.append({"exchange": exchange, "pair": pair})
        return pair_in_exchange

    def get_trend_pic(self, df, **kwargs):
        coin = kwargs.get("coin")
        if not coin:
            return "Exception: need coin name"
        path = kwargs.get("path")
        if not path:
            # path = "./"
            return "Exception: need photo path"
        if not os.path.exists(path):
            return "Exception: path not found"
        source = kwargs.get("source")
        if not source:
            pass
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone(self.tz_utc_8)
        pic_name = "%s-usdt-%s-24hours-trend.png" % (coin, local_dt.strftime("%Y-%m-%d %H"))
        if os.path.exists(path=path+pic_name):
            return_pak = {
                "src": path+pic_name
            }
            return return_pak
        else:
            if source == "tushare":
                data_list = []
                for index, row in df.iterrows():
                    date_time = datetime.strptime(row["date"], "%Y-%m-%d")
                    t = date2num(date_time)
                    _open = row["open"]
                    high = row["high"]
                    low = row["low"]
                    close = row["close"]
                    datas = (t, _open, high, low, close)
                    data_list.append(datas)
                fig, ax = plt.subplots()
                fig.subplots_adjust(bottom=0.2)
                ax.xaxis_date()
                plt.xticks(rotation=45)
                plt.yticks()
                plt.title("%s recent 30 days trend" % coin)
                plt.xlabel("DATE")
                plt.ylabel("USD")
                mpf.candlestick_ohlc(ax, data_list, width=1, colorup='g', colordown='r')
                plt.grid()
                plt.savefig(path+pic_name)
                return_pak = {
                    "src": path+pic_name
                }
                return return_pak
            elif source == "aicoin":
                data_list = []
                for item in df:
                    t = date2num(datetime.fromtimestamp(item[0]))
                    _open = item[1]
                    high = item[2]
                    low = item[3]
                    close = item[4]
                    datas = (t, _open, high, low, close)
                    data_list.append(datas)
                fig, ax = plt.subplots()
                fig.subplots_adjust(bottom=0.2)
                ax.xaxis_date()
                plt.xticks(rotation=45)
                plt.yticks()
                plt.title("%s LATEST 24 HOURS TREND" % coin.upper())
                plt.xlabel("HOUR")
                plt.ylabel("USD")
                mpf.candlestick_ohlc(ax, data_list, width=1/24, colorup='g', colordown='r')
                plt.grid()
                plt.savefig(path + pic_name)
                return_pak = {
                    "src": path + pic_name
                }
                return return_pak
            else:
                pass

    def get_result(self, coin, exchange, symbol, freq, trend_pic=True, cached_coin_pak=None, **kwargs):

        coin = coin.lower()

        start_date_7days = kwargs.get("start_date_7_str")
        start_date_30days = kwargs.get("start_date_30_str")

        source = kwargs.get("source")

        if source == "aicoin":
            price_pak = self.ask_period(coin=coin, step=3600) if not cached_coin_pak else cached_coin_pak
            price_list = price_pak.get("price_list")
            # print(price_list)
            if True:#price_list:
                data_24 = price_list[-24:]

                if trend_pic:
                    trend_pic_pak = self.get_trend_pic(df=data_24, coin=coin, path=self.pic_path, source=source)
                    trend_pic_src = trend_pic_pak.get("src")
                else:
                    trend_pic_src = ''

                if 'avg_latest_width' in price_pak and 'avg_latest_ratio' in price_pak:
                    width = price_pak['avg_latest_width']
                    ratio = price_pak['avg_latest_ratio']
                else:
                    open_price = data_24[0][1]
                    close_price = data_24[-1][4]
                    ratio = self.cal_ratio(open_price=open_price, close_price=close_price)
                    series = [x[2] for x in data_24] + [y[3] for y in data_24]
                    width = self.cal_width(series=series)
                if ratio >= 0:
                    summary = "%s近24小时整体趋势为上涨, 涨幅为%.2f%%。24小时内报价最大差价为%.4f美金(%.2f人民币)。" % (coin.upper(), ratio, width, width*6.89)
                    return_pak = {
                        "success": 1,
                        "msg": "ok",
                        "trend_info": {
                            "coin": coin.upper(),
                            "trend_summary": summary,
                            "trend_pic_src": trend_pic_src,
                        }
                    }
                else:
                    summary = "%s近24小时整体趋势为下跌, 跌幅为%.2f%%。24小时内报价最大差价为%.4f美金(%.2f人民币)。" % (coin.upper(), abs(ratio), width, width*6.89)
                    return_pak = {
                        "success": 1,
                        "msg": "ok",
                        "trend_info": {
                            "coin": coin.upper(),
                            "trend_summary": summary,
                            "trend_pic_src": trend_pic_src,
                        },
                    }
                return return_pak
            else:
                return "error in aicoin"
        else:
            return "please identify data source"

    def get_price(self, coin, timestamp=None, cached_coin_pak=None):
        '''

        :param coin: different kind of coin like BTC, ETH, BCH etc.
        :param timestamp: the price at this timestamp
        :return:
        '''
        if not isinstance(coin, str):
            return "wrong coin type:{}".format(type(coin))
        if timestamp:
            pass
        else:
            coin = coin.lower()
            usd_price_pak = self.ask_period(coin=coin, step=60) if not cached_coin_pak else cached_coin_pak
            if usd_price_pak.get("avg_latest_price"):
                avg_price = usd_price_pak.get("avg_latest_price")
                return_pak = {
                    'success': 1,
                    'msg': 'ok',
                    'timestamp': usd_price_pak.get('latest_timestamp'),
                    'coin_info': {
                        'coin': coin.upper(),
                        'price': "%0.4f" % avg_price,
                        'rmb': "%0.2f" % (float(avg_price)*6.89),
                        },
                }
                return return_pak
            else:
                return_pak = {
                    'success': 1,
                    'msg': usd_price_pak.get('msg'),
                    'coin_info': {}
                }
                return return_pak

    def get_trend(self, coin, freq="daily", start_date=None, end_date=None, trend_pic=True, cached_coin_pak=None):
        '''

        :param coin: different kind of coin like BTC, ETH, BCH etc.
        :param freq: the frequency of price like 15min, 30min, 60min, daily, week
        :param start_date: the start date of price like 20180910
        :param end_date: the end date of price like 20180910
        :return:
        '''
        if not isinstance(coin, str):
            return "wrong coin type:{}".format(type(coin))
        if not start_date and not end_date:
            end_date = datetime.now().date()
            start_date_7 = end_date - timedelta(days=7)
            start_date_30 = end_date - timedelta(days=30)
            start_date_7_str = start_date_7.strftime("%Y%m%d")
            start_date_30_str = start_date_30.strftime("%Y%m%d")
        coin = coin.upper()
        result = self.get_result(coin=coin, exchange='bitfinex', symbol='btcusdt',freq=freq, start_date_7_str=start_date_7_str, start_date_30_str=start_date_30_str, source="aicoin", trend_pic=trend_pic, cached_coin_pak=cached_coin_pak)

        return result


    def query(self, coin, price=True, trend=True, trend_pic=True, *args, **kwargs):
        if not isinstance(coin, str):
            return "wrong coin type:{}".format(type(coin))
        step = kwargs.get('step', 60)
        cached_coin_pak = self.ask_period(coin, step)
        ret_pak = {}
        if price:
            pak = self.get_price(coin, cached_coin_pak=cached_coin_pak)
            ret_pak.update(pak)
        if trend:
            pak = self.get_trend(coin, trend_pic=trend_pic, cached_coin_pak=cached_coin_pak)
            ret_pak.update(pak)
        return ret_pak