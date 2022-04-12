import scrapy
#from bs4 import BeautifulSoup
class FinvizzSpiderSpider(scrapy.Spider):
    name = 'finviz_spider'
    allowed_domains = ['finviz.com']
    start_urls = ['https://finviz.com/']
    def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        #
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue` 

        for url in self.start_urls:
            yield scrapy.Request(url+"quote.ashx?t="+self.ticker, dont_filter=True)

    def parse(self,response):
        #bs4_response = BeautifulSoup(response.text, 'lxml')
        my_dict = {"stock_basic_data":{},"stock_analyst_rating_data":{}}
        company_info_table = response.xpath('.//table[@class="fullview-title"]')
        company_info_table_rows = company_info_table.xpath('.//tr')
        
        my_dict['stock_basic_data']['exchange_name']  = company_info_table_rows[0].xpath('./td/span/text()')[0].extract().replace('[','').replace(']','')
        my_dict['stock_basic_data']['symbol'] = company_info_table_rows[0].xpath('./td/a/text()')[0].extract()
        my_dict['stock_basic_data']['company_website'] =  company_info_table_rows[1].xpath('./td/a/@href')[0].extract()
        my_dict['stock_basic_data']['company_name'] = company_info_table_rows[1].xpath('./td/a/b/text()')[0].extract()
        my_dict['stock_basic_data']['sector'] = company_info_table_rows[2].xpath('./td/a/text()')[0].extract()
        my_dict['stock_basic_data']['industry'] = company_info_table_rows[2].xpath('./td/a/text()')[1].extract()
        my_dict['stock_basic_data']['country'] = company_info_table_rows[2].xpath('./td/a/text()')[2].extract()

        ############# Key points data
        first_table=response.xpath('.//table[@class="snapshot-table2"]')
        first_table_rows = first_table.xpath('.//tr[@class="table-dark-row"]')
        names_tds = first_table_rows.xpath('.//td[@class="snapshot-td2-cp"]')
        values_tds = first_table_rows.xpath('.//td[@class="snapshot-td2"]')
        
        for index, td in enumerate(values_tds):
            key  = names_tds[index].css('td::text').get()
            td_element = td.xpath('.//b/*')
            if len(td_element)==0:
                value = td.xpath('.//b/text()')[0].extract()
            else:
                element = td.xpath('.//b[span]')
                if len(element)==1:
                    value = element.xpath('.//text()')[0].extract()
                else:
                    element = td.xpath('.//b[small]')
                    value = element.xpath('.//text()')[0].extract()
            dt[key] = value
            my_dict['stock_basic_data'][key] = value

        ###### Rating Table ###########
        ratings_table_rows  = response.css('table.fullview-ratings-outer').css('td.fullview-ratings-inner')
        for  index,row in enumerate(ratings_table_rows.css('tr')):
            d = [rows_tds.css('::text').get() for rows_tds in row.css('td')]
            my_dict['stock_analyst_rating_data']['analyst_rating_date_'+str(index+1)] = d[0]
            my_dict['stock_analyst_rating_data']['analyst_rating_status_'+str(index+1)] = d[1]
            my_dict['stock_analyst_rating_data']['analyst_rating_name_'+str(index+1)] = d[2]
            my_dict['stock_analyst_rating_data']['analyst_rating_call_'+str(index+1)] = d[3]
            my_dict['stock_analyst_rating_data']['analyst_rating_target_price_'+str(index+1)] =d[4]
        yield (my_dict)
