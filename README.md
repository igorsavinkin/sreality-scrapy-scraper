# The Scrapy framework scraper 
## The scraper is to get data of the site https://sreality.cz/ leveraging its API.

### The API categories url:
https://www.sreality.cz/api/cs/v2/estates 

Based on the filtering with GET parameters 
 - category_main_cb 
 - category_type_cb 
 - locality_country_id
 - per_page
 - page 
we  request all the info pertaining to needed categories (property type: house/appartment or ad type: sale or rent).



### The API individual property url:
https://www.sreality.cz/api/cs/v2/estates/<ad ID>
  
where <ad ID> is the ad number, eg. 2103730524



