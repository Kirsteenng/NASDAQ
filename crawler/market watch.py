# market spider gets all the article links from individual websites.
import scrapy
import pandas as pd
import time
import pkgutil
from io import StringIO

class MW(scrapy.Spider):
	name= "market"
	num_tickers = 6678
	count = 5877

	# access by using array.Symbol[0]. total number of ticker = 667
	raw = pkgutil.get_data("tutorial", "res/array.csv")
	csvio = StringIO(unicode(raw))
	array = pd.read_csv(csvio,index_col=False)
	start_urls = ['http://www.marketwatch.com/investing/stock/bx/news']

	# if any of these word exists in the href, the href will not be taken
	list = ['video','http://www.marketwatch.com/videovideo', 'www.wsj.com','seekingalpha','www.fool.com','www.zacks.com']

	def errhandling(self, response):
		yield{
		'name' : self.array.Symbol[self.count]
		}
		self.count+=1
		next_page = 'http://www.marketwatch.com/investing/stock/'+ self.array.Symbol[self.count] + '/news'
		yield scrapy.Request(next_page,callback=self.parse,errback = self.errhandling)

	def parse(self,response):
		ticker = self.array.Symbol[self.count]
		yield{
		'name' : ticker
		}
		news = response.xpath('//*[@id="mwheadlines"]/p/text()').extract_first()
		if news != None :
			print '												NO NEWS FOR ' + ticker

		else:
			for item in response.xpath('//*[@id="mwheadlines"]/div[1]/ol/*'):
				#Select all of the list after ol
				#print '					going into '+ str(item)
				link_time = item.css('p.timestamp span::text').extract_first()
				#time = str(time
				#print link_time

				if link_time == None:
					break

				elif '2017' in link_time:
					link = item.css('a::attr(href)').extract_first()
					if link != None and any(x not in link for x in self.list) :
						print '														taking this article'
						yield{'href': link}


		self.count += 1
		if  self.count <= self.num_tickers:
			next_page = 'http://www.marketwatch.com/investing/stock/'+ self.array.Symbol[self.count] + '/news'
			yield scrapy.Request(next_page,callback = self.parse,errback =self.errhandling )
