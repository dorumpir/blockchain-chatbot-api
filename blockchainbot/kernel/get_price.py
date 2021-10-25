import requests
import gevent
from gevent.queue import Queue
#import gevent.monkey
#gevent.monkey.patch_all()


class CoinPrice:

    def __init__(self, mongo):
        self.mongo = mongo
        self.tasks = Queue()

    def find_pairs(self, coin, database, table):
        """
        给定一个币种，从数据库中查询存所有在该币种与USDT交易对的交易所，并返回所有交易所名与交易对名列表
        :param coin: 币种
        :param database: 查询交易所数据库
        :param table: 查询交易所数据表
        :return:
        """
        coin = coin.lower()
        db = self.mongo.connection(database)
        cursor = db[table].find({}, {"exchange": 1, "ts_pair": 1})
        pair_in_exchange = []
        for item in cursor:
            pair_list = [x for x in item.get("ts_pair")]
            exchange = item.get("exchange")
            for pair in pair_list:
                if (("%susdt" % coin == pair) or ("%susd" % coin == pair)) and (exchange != "bleutrade"):
                    pair_in_exchange.append({"exchange": exchange, "pair": pair})
        return pair_in_exchange

    def ask_pirce(self, exchange, pair, step):
        """
        调用aicoin API查询指定交易所交易对60s步长报价，返回最后一分钟的收盘价格
        :param exchange: 交易所名称
        :param pair: 交易对名称
        :param step: 查询时间步长
        :return:
        """
        url = "https://widget.aicoin.net.cn/chart/api/data/period?symbol=%s%s&step=%s" % (exchange, pair, step)
        try:
            r = requests.get(url=url)
            json_data = r.json()
            if json_data.get("data"):
                latest_price_list = json_data.get("data")
                latest_price = latest_price_list[-1][4]
                # -1 代表最后一分钟报价，4代表收盘价格，格式是由aicoin设置
                self.tasks.put(latest_price)
            else:
                pass
        except:
            pass

    def get_average_price(self, coin, database, table):
        """
        获取所有包含该币种的交个数据，求平均值并返回
        :param coin: 币种
        :param database: 交易所数据库
        :param table: 交易所数据表
        :return:
        """
        pair_in_exchanges = self.find_pairs(coin=coin, database=database, table=table)
        threads = [gevent.spawn(self.ask_pirce, pair_in_exchange.get("exchange"), pair_in_exchange.get("pair"), 60) for pair_in_exchange in pair_in_exchanges]
        gevent.joinall(threads)
        price = 0
        queue_size = self.tasks.qsize()
        while not self.tasks.empty():
            price += self.tasks.get()
        if queue_size:
            avg_price = price / queue_size
            return_pak = {'success': "1",
                          'msg': "ok",
                          'coin_info': {
                                'coin': coin.upper(),
                                'price': "%0.4f" % avg_price,
                                'rmb': "%0.2f" % (float(avg_price)*6.89),
                                },
                          }

            return return_pak
        else:
            return_pak = {'success': "0",
                          'msg': "not find this coin",
                          'coin_info': {
                                'coin': coin.upper(),
                                'price': None,
                                'rmb': None
                                },
                          }
            return return_pak

