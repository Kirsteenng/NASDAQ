# mw spider gets all the details of article from individual article websites.
import scrapy
import pandas as pd
import pkgutil
from io import StringIO

class Reuters_article(scrapy.Spider):
	name= "ra"
	num_articles = 31717
	#31717
	Count = 0
	article_count = 1

	raw = pkgutil.get_data("tutorial", "res/reuters_feed.csv")
	#print("This is raw: ", raw)
	csvio = StringIO(unicode(raw))
	# array = pd.read_csv('/Users/Kirsteenng/tutorial/tutorial/res/market.csv',encoding="utf-8-sig")
	array = pd.read_csv(csvio)
	#print(array)
	start_urls = ['http://www.reuters.com/article/us-wisconsin-crime-idUSKBN16406U']

	def errhandling(self, response):
		self.Count+=1
		self.article_count = 1
		next_page = 'http://www.reuters.com/'+ self.array.href[self.Count].lstrip('u')
		#print(next_page)
		yield scrapy.Request(next_page,callback=self.parse,dont_filter = True,errback = self.errhandling)

	def parse(self,response):

		article_title = str(response.xpath('//*[@id="rcs-articleHeader"]/div[1]/div[1]/h1/text()').extract())
		article_time = str(response.xpath('//*[@id="rcs-articleHeader"]/div[1]/div[1]/div/span[3]/text()').extract())

		yield{
		'Article' : str(self.article_count)+ ' : '+ article_title,
		'Time': article_time,
		'Body':  response.xpath('//span[@id="article-text"]/p/text()').extract()}

		#article_body = response.xpath('//*[@id="article-text"]/p[*]').extract()

		self.Count += 1
		self.article_count += 1

		while '/article/' not in self.array.href[self.Count] and self.Count < self.num_articles:
			yield {'Name': self.array.href[self.Count]}
			self.Count += 1
			self.article_count = 1

		next_page = 'http://www.reuters.com/'+ self.array.href[self.Count].lstrip('u')
		yield scrapy.Request(next_page,callback=self.parse, dont_filter = True,errback = self.errhandling)
