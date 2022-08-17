import scrapy


class AmazonScrape(scrapy.Spider):

	name = 'gamingchairs'
	base_url = 'https://www.amazon.com/s?k=gaming+chairs&i=garden&rh=n%3A18682062011%2Cn%3A668180011&dc&page='
	headers = {
		"Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Linux"',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		"Sec-Fetch-Site": 'same-origin',
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
	}

	def start_requests(self):

		self.product_url = []

		for page in range(1, 2):

			next_page = self.base_url + str(page)

			yield scrapy.Request(url=next_page, headers=self.headers, callback=self.link_response
								 )

	def link_response(self, response):

		allowed_domain = 'https://www.amazon.com'

		for detailed_page in response.xpath('//span[@data-component-type="s-product-image"]'):

			links = detailed_page.xpath('a/@href').extract()
			len_links = len(links)

			for i in range(len_links):

				link = links[i]
				if link.startswith('/gp/slredirect/picassoRedirect.html/') or link.startswith('/sspa/') :
				 # :
					pass
				else:
					# print(link)
					# self.product_url.append(allowed_domain+link)
					# print(self.product_url)
	#                 yield scrapy.Request(url=allowed_domain+link, headers=self.headers, callback=self.parse)

	# def parse(self, response):

	#     # len_product_url = len(self.product_url)

	#     # for i in range(len_product_url):

	#     # 	url = self.product_url[i]

	#     yield {

	#         # 'product_url' : url ,
	#         # 'product_asin': response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr[21]/td/text()").extract_first(),
	#         'product_name': response.xpath('//span[@id="productTitle"]/text()').extract_first(),
	#         # 'brand': response.xpath("//tr[@class='a-spacing-small po-brand']/td[@class='a-span9']/span/text()").extract_first(),
	#         'star_rating': response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract_first(),
	#         'price': response.xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span/text()').extract_first(),
	#         # 'old_price': response.xpath('//span[@class="a-size-small a-color-secondary aok-align-center basisPrice"]/span[@class="a-price a-text-price"]/span/text()').extract_first(),
	#         # 'size': response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr[18]/td/text()").extract_first(),
	#         # 'color': response.xpath("//tr[@class='a-spacing-small po-color']/td[@class='a-span9']/span/text()").extract_first(),
	#         # 'date_first_available':  response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr[25]/td/text()").extract_first()

	#     }
# 		price
# old_price
# size
# color
# date_first_available
