import scrapy
import json

per_page = 5
property_codes = { 1: 'apartment' , 2:'house' }
deal_codes = { 1: 'sell' , 2: 'rent' }

class MySpider(scrapy.Spider):
    name = 'Real estate data'
    max_pages = 2 # int(11300/60) + 1
    base_api_url = 'https://www.sreality.cz/api'
    #logger.info('Max pages: ', max_pages)
    
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=2&category_type_cb=1&locality_country_id=10001&per_page=' + str(per_page) + '&page='+str(x)+''for x in range(1, max_pages)]
 
    def parse(self, response):
         jsonresponse = response.json() # json.loads(response.text)

         for item in jsonresponse["_embedded"]['estates']:
            # yield { 'url': item['_links']['self']['href'] }
             yield scrapy.Request( self.base_api_url + item['_links']['self']['href'] ,
                          callback=self.parse_detail_page)
            
    def parse_detail_page(self, response):  
        jsonresponse = response.json()        
        item = {} # empty dict item
        try:             
            # check if the property is an apartment or a house
            if jsonresponse['seo']['category_main_cb'] and 1 <= jsonresponse['seo']['category_main_cb'] <= 2:                
                item['PROPERTY_CODE'] = property_codes[ jsonresponse['seo']['category_main_cb'] ]
                item['DEAL_CODE'] = deal_codes[ jsonresponse['seo']['category_type_cb'] ]
                # house     -  category_main_cb=2
                # apartment - category_main_cb=1
                # pronájmu - rent     category_type_cb=2
                # prodej   - sell     category_type_cb=1
            else:
                return           
            

            item['URL'] = response.url
            item['meta'] = jsonresponse['meta_description']
            item['TITLE'] = jsonresponse['name']['value']
            item['DESCRIPTION'] = jsonresponse['text']['value']
            
            if jsonresponse['price_czk']['value']:
                item['PRICE'] =  jsonresponse['price_czk']['value']
            else:
                item['PRICE'] = ''
            item['LONGITUDE'] = jsonresponse['map']['lon']
            item['LATITUDE'] = jsonresponse['map']['lat']

            item["ADDRESS"] = jsonresponse['locality']['value']
            # gather images
            item['IMAGES'] = set()
            
            for images in jsonresponse['_embedded']['images']:                 
                if images['_links']['dynamicDown']:
                    item['IMAGES'].add( images['_links']['dynamicDown']['href'])
                if images['_links']['gallery']:
                    item['IMAGES'].add(images['_links']['gallery']['href'])
                if images['_links']['self']:
                    item['IMAGES'].add(images['_links']['self']['href'])
                if images['_links']['dynamicUp']:
                    item['IMAGES'].add(images['_links']['dynamicUp']['href'])
                if images['_links']['view']:
                    item['IMAGES'].add(images['_links']['view']['href'])
                    
            for i in jsonresponse['items']:
                if isinstance(i['value'] , list):
                    item[i['name']]= ''
                    for j in i['value']:
                        item[i['name']] += j['value'] + ', '
                    item[i['name']] = item[i['name']][:-2]   
                else:
                    item[i['name']] = i['value']
                    
        except Exception as e:
            print ('Error: ' , e, ' url: ',   response.url  )           
        yield item  
