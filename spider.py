import scrapy

class MySpider(scrapy.Spider):
    name = 'data'
    max_pages = int(11300/60) + 1
    #print ('max pages: ', max_pages)
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=2&category_type_cb=1&locality_country_id=10001&per_page=60&page=1'+str(x)+''for x in range(1, max_pages)]
 
    def parse(self, response):
         jsonresponse = response.json() # json.loads(response.text)

         for item in  jsonresponse["_embedded"]['estates']:
             yield { 'url': item['_links']['self']['href'] }

