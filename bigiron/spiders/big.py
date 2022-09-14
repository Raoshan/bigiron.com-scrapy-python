import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.bigiron.com/Search?showTab=true&search={}&searchMode=All&userControlsVisible=false&distance=500&historical=false&tab=equipment-tab&page=1&itemsPerPage=20&filter=Open&sort=Start&sortOrder=Ascending'

class BigSpider(scrapy.Spider):
    name = 'big'
    # allowed_domains = ['bigiron.com']
    def start_requests(self):        
        for index in df:            
            yield scrapy.Request(base_url.format(index),cb_kwargs={'index':index})

    def parse(self, response, index):
        """Pagination"""
        total_pages = response.xpath("//div[@class='pager-pagination']/span[last()-1]/a/text()").extract()[0]
        # print(total_pages)
        current_page = response.css(".disabled a::text").extract()[0]
        # print(current_page)
        url = response.url           
        
        if total_pages and current_page:            
            if int(current_page) ==1:                
                for i in range(2, int(total_pages)+1):                   
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max) 
                    # print(url)                   
                    yield response.follow(url, cb_kwargs={'index':index})
                   

        links = response.css(".lot-title a::attr(href)")
        # print(links)
        for link in links:            
            yield response.follow("https://www.bigiron.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})
        
        
    def parse_item(self, response, index):         
        
        lot_id = response.css("span.lot-info span::text").extract()[0]
        image = response.css("img.media-object::attr(src)").extract()[0]  
        description = response.css("div.description span::text").get()     
        name = response.css(".lot-title a h1::text").extract()[0] 
        location = response.css(".lot-locale::text").extract()[0]
        auctioner = response.css(".seller strong::text").get()
        auction_date = response.css(".lot-auction::text").get()               
    
        yield{
            'product_url' : response.url,
            'item_type' : index.strip(),
            'image_link' : image,
            'product_name': name,
            'auction_date' : auction_date,
            'location' : location,            
            'lot_id' : lot_id,
            'auctioner' : auctioner,
            'website' : "bigiron",
            'description' : description
        }
        


   