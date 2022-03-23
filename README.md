# The Scrapy framework scraper 
## The scraper is to get data of the site https://sreality.cz/ leveraging the service's API.

### The API categories url:
`https://www.sreality.cz/api/cs/v2/estates` 

Based on the filtering by the GET parameters (see below) we request all the info pertaining to needed categories. 

Parameters:

 - category_main_cb   ( property type: house/appartment)
 - category_type_cb   ( ad type: sale or rent )
 - locality_country_id 
 - per_page
 - page (page index)


The categories API request returns the individual property API URLs.


### The individual API property url
Eg. `https://www.sreality.cz/api/cs/v2/estates/<ad ID>`
  
where `<ad ID>` is an ad number, eg. 2103730524

Since the property ads number/count is a fluctuating/changing one, one may request the exact properties count thru corresponding URL:
https://www.sreality.cz/api/cs/v2/estates/count
Again, one may 

## The workflow
The scraper requests all the categories URLs (`start_urls` array) and parses them with the `parse` procedure. As it gets individual estate URLs, it spawns new Scrapy requests to be parsed by the `parse_detail_page` procedure. Both methods deal with JSON data. 

## Launch
`scrapy runspider spider.py -o resutl.jl` where `resutl.jl` is a file to have all the JSON data in lines.



