### 部署：
参见 [link](DEPLOY.md)

### 对外API：

``` shell
 GET  /api/v1/bc/keywords         # 给一个句子，返回关键词， p.s. 句子放在body里
 resopnse ->
 {
    'success': 0 成功, 其他值失败
    'msg': 失败信息 str / 成功 ok，
    'keywords': ['kw1', 'kw2' ...]     # 全部关键字列表
    'bc_keywords': ['kw1', 'kw2' ...]  # 区块链相关关键字列表
 }

 GET  /api/v1/bc/news/keywords    # 给一条新闻，返回关键词， p.s. news放在body里
 resopnse ->
 {
    'success': 0 or 1,
    'msg': 失败信息 str / 成功 ok，
    'keywords': 
        {'keyword': 关键词 str, 'tag': 词性 list, 'keyword': 关键词 str, 'tag': 词性 list...}
 }

 GET  /api/v1/bc/news?keywords=aaa+bbb+ccc       # 给几个关键字（加号分割），返回一个高相关新闻
 返回最新快讯需要传入keywords=default
 response ->
 {
    'success': 0 or 1,
    'msg': 失败信息 str / 成功 ok，
    'news': {
        'id': 新闻id int,
        'title': 新闻标题 str,
        'content': 新闻内容 str,
        'timestamp': 新闻时间戳 int,
    }
 }

 GET  /api/v1/bc/qapairs?qkeywords=aaa+bbb+ccc   # 给几个关键字（加号分割），返回一个高相关问答对
 response ->
 {
    'success': 0成功 或 -1失败
    'msg': 失败信息 str
    'qapairs': {
        'question': 问题 str
        'answer': 回答 str
    }
 }

 GET  /api/v1/bc/knowledge?questions=qqqqq+qqqqq    # 给一个问题，返回一个相应知识
 response ->
 {
    'success': 0成功 or 1失败
    'msg': 失败信息 str
    'data': [知识1 str, 知识2 str, ...]
 }
 
 GET  /api/v1/bc/summary         # 各一个新闻，返回一个总结语句
 response ->
 {
    'success': 0 or 1
    'msg': 失败信息 str
    'summary': 总结 str
 }
 
 GET  /api/v1/bc/sentence?keywords=aaa+bbb+ccc       # 给几个关键字，返回一个造句
 response ->
 {
    'success': 0成功 or 1失败
    'msg': 失败信息 str
    'sentence': 造句 str
 }

 GET  /api/v1/bc/price?coin=btc    # 给一个币种的缩写，返回该币种当前价格
 response ->
 {
    'success': 0 or 1
    'msg': 失败信息 str
    'coin_info': {
        'coin': 'btc',
        'price': 6295.01058507
    }
 }
 
 GET  /api/v1/bc/trend?coin=btc    # 给一个币种的缩写，返回该币种近30日日K线图，以及图片路径
 response ->
 {
    'success': 0 or 1,
    'msg': 失败信息 str,
    'trend_info': {
        'coin': 'BTC',
        'trend_summary': 'BTC近30日整体趋势为上涨, 涨幅为3.00%, 30日内报价最大差价为1533.8500美金',
        'trend_pic_src': './BTC-usdt-30days-trend.png',
    }
 }
 
 GET  /api/v1/bc/wordcloud  # 获取最近一天的快讯词云
 response ->
 {
    'success': 0 or 1,
    'word_cloud_src': './1538101233-word-cloud.png'
 }
```


 
 
### 附加:
 
 - 词典用法： 参考[SnowNLP](https://github.com/isnowfy/snownlp) 关于训练部分
 