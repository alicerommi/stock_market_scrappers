# stock_market_scrappers
 Scrapy Framework to collect stock data from multiple websites like finvizz, yahoo finance, barchart, nasdaq, investing.com
 
 How to run the spider for collecting data of any stock symbol (ticker) like AAPL, PYPL
 scrapy crawl -a ticker=aapl spider_name [finviz_spider]  # in case of finviz
 
 If you want to convert the response of spider into json then use this
 
 scrapy crawl -a ticker=aapl spider_name [finviz_spider] -O aapl_response.json
