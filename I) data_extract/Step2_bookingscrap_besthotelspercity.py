# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging
from urllib import request

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess

class BookingCitiesSpiderPage(scrapy.Spider):


    # Name of your spider
    name = "hoteldatabooking__bestpercitycenter"

    # ListofCities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas",
    #                 "Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

    def start_requests(self):

        ListofCities =["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas",
                    "Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

        url='https://www.booking.com/searchresults.fr.html?ss={}&nflt=distance%3D3000%3Bclass%3D5%3Breview_score%3D80%3Bht_id%3D204%3Bclass%3D3%3Bclass%3D4%3Breview_score%3D90&order=bayesian_review_score'

        for cities in range(len(ListofCities)) : 
            yield scrapy.Request(url=url.format(ListofCities[cities]), callback=self.parse)
            
    # Callback function that will be called when starting your spider
    # It will get text, author and tags of all <div> with class="quote"
    def parse(self, response):
        quotes = response.xpath('//div[@class="b978843432"]')
        for quote in quotes:

            yield{
                'hotelname' : quote.xpath('.//div[@class="fcab3ed991 a23c043802"]/text()').get(),
                'location': quote.xpath('.//span[@class="f4bd0794db b4273d69aa"]/text()').get(),
                'description': quote.xpath('.//div[@class="d8eab2cf7f"]/text()').get(),
                'rating' : quote.xpath ('.//div[@class="b5cd09854e d10a6220b4"]/text()').get(),
            }
                       
# Name of the file where the results will be saved
filename = "hoteldatabooking_bestpercitycenter.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('/Users/fezzibasma/Desktop/Data Full-Stack/Data Collection & Management/src/'):
        os.remove('/Users/fezzibasma/Desktop/Data Full-Stack/Data Collection & Management/src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        '/Users/fezzibasma/Desktop/Data Full-Stack/Data Collection & Management/src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingCitiesSpiderPage)
process.start()

