import scrapy
from collections import defaultdict
class FinvizzSpiderSpider(scrapy.Spider):
    name = 'finviz_spider'
    allowed_domains = ['finviz.com']
    start_urls = ['https://finviz.com/']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+"quote.ashx?t="+self.ticker, dont_filter=True)
    def parse(self,response):
        my_dict = {"stock_basic_data":defaultdict(list),"stock_analyst_rating_data":defaultdict(list),"news":defaultdict(list),"insiders":defaultdict(list)}
        company_info_table = response.xpath('.//table[@class="fullview-title"]')
        company_info_table_rows = company_info_table.xpath('.//tr')
        my_dict['stock_basic_data']['exchange_name']  = company_info_table_rows[0].xpath('./td/span/text()')[0].extract().replace('[','').replace(']','')
        my_dict['stock_basic_data']['symbol'] = company_info_table_rows[0].xpath('./td/a/text()')[0].extract()
        my_dict['stock_basic_data']['company_website'] =  company_info_table_rows[1].xpath('./td/a/@href')[0].extract()
        my_dict['stock_basic_data']['company_name'] = company_info_table_rows[1].xpath('./td/a/b/text()')[0].extract()
        my_dict['stock_basic_data']['sector'] = company_info_table_rows[2].xpath('./td/a/text()')[0].extract()
        my_dict['stock_basic_data']['industry'] = company_info_table_rows[2].xpath('./td/a/text()')[1].extract()
        my_dict['stock_basic_data']['country'] = company_info_table_rows[2].xpath('./td/a/text()')[2].extract()
        my_dict['stock_basic_data']['about_company'] = response.css ('td.fullview-profile::text').get()
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
            
            my_dict['stock_basic_data'][key] = value

        ###### Rating Table ###########
        ratings_table_rows  = response.css('table.fullview-ratings-outer').css('td.fullview-ratings-inner')
        for  index,row in enumerate(ratings_table_rows.css('tr')):
            d = [rows_tds.css('::text').get() for rows_tds in row.css('td')]
            my_dict['stock_analyst_rating_data']['analyst_rating_date'].append(d[0])
            my_dict['stock_analyst_rating_data']['analyst_rating_status'].append (d[1])
            my_dict['stock_analyst_rating_data']['analyst_rating_name'].append (d[2])
            my_dict['stock_analyst_rating_data']['analyst_rating_call'].append (d[3])
            my_dict['stock_analyst_rating_data']['analyst_rating_target_price'].append(d[4])

        # Scrapping News #
        news_table_rows = response.css('table.fullview-news-outer').css('tr')
        for index, row in enumerate(news_table_rows):
            td_data= [td for td in row.css('td') ]
            my_dict['news']['news_datetime'].append(td_data[0].css('::text').get())
            my_dict['news']['news_text'].append(td_data[1].css('a::text').get())
            my_dict['news']['news_link'].append(td_data[1].css('a::attr(href)').get())
            my_dict['news']['news_source'].append(td_data[1].css('div.news-link-right>span::text').get())
        # scrapping insider table
        insider_table_rows = response.css('table.body-table tr')
        for row in insider_table_rows[1:]:
            td_data= [td for td in row.css('td') ]
            my_dict['insiders']['insider_name'].append(td_data[0].css('::text').get())
            my_dict['insiders']['insider_relationship'].append(td_data[1].css('::text').get())
            my_dict['insiders']['insider_date'].append(td_data[2].css('::text').get())
            my_dict['insiders']['insider_transaction'].append(td_data[3].css('::text').get())
            my_dict['insiders']['insider_cost'].append(td_data[4].css('::text').get())
            my_dict['insiders']['insider_shares'].append(td_data[5].css('::text').get())
            my_dict['insiders']['insider_value'].append(td_data[6].css('::text').get())
            my_dict['insiders']['insider_total_shares'].append(td_data[7].css('::text').get())
            my_dict['insiders']['insider_sec_filling_datetime'].append(td_data[8].css('::text').get())
        yield(my_dict)