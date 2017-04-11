# market spider gets all the article links from individual websites.
import scrapy
import pandas as pd
import time
import pkgutil
from io import StringIO

class Reuters(scrapy.Spider):
	name= "reuters"
	num_tickers = 6678
	count = 0


#6678
	# access by using array.Symbol[0]. total number of ticker = 667
	raw = pkgutil.get_data("tutorial", "res/reuters.csv")
	csvio = StringIO(unicode(raw))
	array = pd.read_csv(csvio,index_col=False)
	start_urls = ['http://www.reuters.com/search/news?blob=PIH&sortBy=date&dateRange=pastYear']

	# if any of these word exists in the href, the href will not be taken
	list = ['video','http://www.marketwatch.com/videovideo', 'www.wsj.com','seekingalpha','www.fool.com','www.zacks.com']

	def errhandling(self, response):
		yield{
		'Name' : self.array.Symbol[self.count]
		}
		self.count+=1
		next_page = 'http://www.reuters.com/search/news?blob=' + self.array.Name[self.count] + '&sortBy=date&dateRange=pastYear'
		yield scrapy.Request(next_page,callback=self.parse,errback = self.errhandling,dont_filter = True)

	def parse(self,response):
		ticker = self.array.Symbol[self.count]
		yield{
		'Name' : ticker
		}

		for i in response.xpath('//div[re:test(@class, "search-result-indiv")]'):
			#print(i)
			time = i.css('h5.search-result-timestamp::text').extract()
			#print (time)
			if '2017' in str(time):
				link = i.css('h3.search-result-title a::attr(href)').extract()
				print (link)
				yield {'href': link}

			else:
				break

		self.count +=1
		if  self.count <= self.num_tickers:
			next_page = 'http://www.reuters.com/search/news?blob=' + self.array.Name[self.count] + '&sortBy=date&dateRange=pastYear'
			yield scrapy.Request(next_page,callback = self.parse,errback =self.errhandling, dont_filter= True )
