# mw spider gets all the details of article from individual article websites.
import scrapy
import pandas as pd
import pkgutil
from io import StringIO

class MWA(scrapy.Spider):
	name= "mw"
	num_articles = 12258
	Count = 1
	article_count = 1

	raw = pkgutil.get_data("tutorial", "res/market.csv")
	#print("This is raw: ", raw)
	csvio = StringIO(unicode(raw))
	# array = pd.read_csv('/Users/Kirsteenng/tutorial/tutorial/res/market.csv',encoding="utf-8-sig")
	array = pd.read_csv(csvio)
	#print(array)
	start_urls = ['http://www.marketwatch.com/story/the-dows-21000-powered-by-apples-15-rally-since-jan-25-2017-03-01']

	def errhandling(self, response):
		self.Count+=1
		self.article_count = 1
		next_page = 'http://www.marketwatch.com/'+ self.array.href[self.Count]
		print(next_page)
		yield scrapy.Request(next_page,callback=self.parse,errback = self.errhandling)

	def parse(self,response):

		article_title = str(response.xpath('//*[@id="article-headline"]/text()').extract())
		article_time = str(response.xpath('//*[@id="published-timestamp"]/span/text()').extract())
		article_body = response.xpath('//*[@id="article-body"]/p[*]').extract()

		yield{
		'Article' : str(self.article_count)+ ' : '+ article_title,
		'Time': article_time,
		'Body': article_body}

		self.Count += 1
		self.article_count += 1

		while '/story/' not in self.array.href[self.Count] and self.Count < self.num_articles:
			yield {'Name': self.array.href[self.Count]}
			self.Count += 1
			self.article_count = 1

		next_page = 'http://www.marketwatch.com/'+ self.array.href[self.Count]
		yield scrapy.Request(next_page,callback=self.parse, dont_filter = True)
