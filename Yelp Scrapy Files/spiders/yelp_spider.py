from scrapy import Spider, Request
from yelp.items import YelpItem


class YelpSpider(Spider):
    name = "yelp_spider"
    allowed_urls = ['https://www.yelp.com']
    start_urls = ['https://www.yelp.com/search?cflt=restaurants&find_loc=New%20York%2C%20NY&sortby=review_count&start=0']

    def parse(self, response): #what to do on first page, how to get to next pages
        temp = 'https://www.yelp.com/search?cflt=restaurants&find_loc={}&sortby=review_count&start={}'
        splt_places = []
        city_urls = []
        page_urls = []
        places = ['New York NY', 'Los Angeles CA', 'Chicago IL', 'Houston TX', 'Philadelphia PA', 'Phoenix AZ', 'Columbus OH', 'San Antonio TX', 'Washington DC', 'San Diego CA', 'Indianapolis IN', 'Dallas TX', 'Boston MA', 'San Jose CA', 'Detroit MI', 'Austin TX', 'Baltimore MD', 'San Francisco CA', 'Milwaukee WI', 'Nashville TN']

        for i in places:
            splt_places.append(i.split(" "))
        for j in splt_places:
            if (len(j) == 2):
                city_urls.append(j[0] + '%2C%20' + j[1])
            if (len(j) == 3):
                city_urls.append(j[0] + '%20' + j[1] + '%2C%20' + j[2])
            if (len(j) == 4):
                city_urls.append(j[0] + '%20' + j[1] + '%20' + j[2] + '%2C%20' + j[3])

        for k in city_urls:
            for m in range(0,91,30):
                page_urls.append(temp.format(k, m))

        for url in page_urls:
            yield Request(url=url, callback = self.parse_result_page)
        
    def parse_result_page(self, response): #actually extracting the info from each page
        reviews = response.xpath('//span[@class="lemon--span__373c0__3997G display--inline__373c0__1DbOG border-color--default__373c0__2oFDT"]/div/@aria-label').extract()
        city = response.xpath('//span[@class="queryLocation__373c0__15viw"]/text()').extract()
        for k in range(1,len(reviews)): 
            print(k)
            item = YelpItem()
            item['reviews'] = reviews[k]
            item['city'] = city
            yield item
    