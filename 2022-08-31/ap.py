import scrapy
import datetime
import re
import dateutil.parser as dparser
from copy import deepcopy
from ..items import AmazonInItem

class AmazonScrape(scrapy.Spider):

	# download_delay = 2

	name = 'ap'
	base_url = 'https://www.amazon.in/Multi-Purpose-Ergonomic-Adjustable-Massager-Reclining/dp/B0B17ZGRQM/ref=lp_28205294031_1_2'
	headers = {
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	def start_requests(self):

		

		yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse
							 )

	def parse(self, response):

		# print(response.url)

		product_url = response.url
		
		product_asins = response.xpath(
			'//div[@id="detailBullets_feature_div"]//span[text()[contains(.,"ASIN")]]/following-sibling::span/text()').extract_first() or response.xpath(
			'//div[@id="prodDetails"]//th[text()[contains(.,"ASIN")]]/following-sibling::td/text()').extract_first()
		product_asin = product_asins.encode("ascii", "ignore").decode().strip()
		product_name = response.xpath('//span[@id="productTitle"]/text()').extract_first(
		).encode("ascii", "ignore").decode().strip().replace('\"', "")
		brand = response.xpath(
			'//div[@id="detailBullets_feature_div"]//span[text()[contains(.,"Importer")]]/following-sibling::span/text()').extract_first() or response.xpath(
			'//div[@id="prodDetails"]//th[text()[contains(.,"Brand")]]/following-sibling::td/text()').extract_first()
		product_brand = 'N/A' if brand is None else brand.encode(
			"ascii", "ignore").decode().strip()
		star_ratings = response.xpath(
			'//span[@class="a-icon-alt"][text()[contains(.,"out of 5 stars")]]/text()').extract_first()
		product_star_ratings = 0 if star_ratings is None else float(
			star_ratings[0:3])
		product_price = response.xpath(
			'//div[@id="apex_desktop"]//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span/text()').extract_first() or response.xpath(
			'//div[@id="apex_desktop"]//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span/text()').extract_first()
		product_price_list = 0 if product_price is None else float(
			product_price[1:].replace(",", ""))
		product_old_price = response.xpath(
			'//div[@id="apex_desktop"]//span[@class="a-price a-text-price"]/span/text()').extract_first() or response.xpath(
			'//div[@id="apex_desktop"]//span[@class="a-price a-text-price a-size-base"]/span/text()').extract_first()
		product_old_price_list = 0 if product_old_price is None else float(
			product_old_price[1:].replace(",", ""))
		size = response.xpath(
			'//div[@id="detailBullets_feature_div"]//span[text()[contains(.,"Product Dimensions")]]/following-sibling::span/text()').extract_first() or response.xpath(
			'//div[@id="prodDetails"]//th[text()[contains(.,"Product Dimensions")]]/following-sibling::td/text()').extract_first()
		product_size = 'N/A' if size is None else size.encode(
			"ascii", "ignore").decode().strip().replace('\"', "")
		color = response.xpath(
			'//div[@id="detailBullets_feature_div"]//span[text()[contains(.,"Colour")]]/following-sibling::span/text()').extract_first() or response.xpath(
			'//div[@id="prodDetails"]//th[text()[contains(.,"Colour")]]/following-sibling::td/text()').extract_first()
		product_color = 'N/A' if color is None else color.encode(
			"ascii", "ignore").decode().strip()
		date = response.xpath(
			'//div[@id="detailBullets_feature_div"]//span[text()[contains(.,"Release date")]]/following-sibling::span/text()').extract_first() or response.xpath(
			'//div[@id="prodDetails"]//th[text()[contains(.,"Date First Available")]]/following-sibling::td/text()').extract_first()
		product_date = 'N/A' if date is None else datetime.datetime.strptime(
			date.encode("ascii", "ignore").decode().strip(), '%d %B %Y').date()
		product_sold_by = response.xpath(
			'//div[@id="merchant-info"]/a/span/text()').extract_first() or response.xpath('//div[@id="merchant-info"]/a[@id="sellerProfileTriggerId"]/text()').extract_first()
		product_seller = 'N/A' if product_sold_by is None else product_sold_by.encode(
			"ascii", "ignore").decode().strip()
		url_ajax = f'https://www.amazon.in/gp/product/ajax/ref=auto_load_aod?asin={product_asin}&pc=dp&experienceId=aodAjaxMain'
		proDetails = {
			'product_url': product_url,
			'product_asin': product_asin,
			'product_name': product_name,
			'brand': product_brand,
			'star_rating': product_star_ratings,
			'price': product_price_list,
			'old_price': product_old_price_list,
			'size': product_size,
			'color': product_color,
			'date_first_available':  product_date,
			'seller': product_seller,
			# 'link' : reviews_link
		}

		# yield proDetails

		yield scrapy.Request(url=url_ajax, headers=self.headers, callback=self.ajax_requests,
							 cb_kwargs={'proDetails': proDetails}
							 )

	def ajax_requests(self, response, proDetails):

		
		product_asin = proDetails['product_asin']
		start_urls = []
		offers_option_list = []
		
		for offer_list in response.xpath('//div[@id="aod-offer-list"]'):

			product_price_option = offer_list.xpath(
				'//div[@id="aod-offer"]//span[@class="a-offscreen"]/text()').extract()
			product_price_option_formatted = [
				i.replace(',', '') for i in product_price_option]
			product_price_option_float = [
				float(j[1:]) for j in product_price_option_formatted]
			product_seller_option = offer_list.xpath(
				'//div[@id="aod-offer-soldBy"]//*[contains(@aria-label, "Opens a new page")]/text()').extract()
			product_seller_option_formatted = [
				k.strip() for k in product_seller_option]
			for i, j in zip(product_price_option_float, product_seller_option_formatted):
				offers_option_dict = {'offer_price': i, 'seller': j}
				offers_option_list.append(offers_option_dict)
			print(offers_option_list)
			offers_options = offers_option_list if offers_option_list else 'N/A'
		item = {

			'product_url': proDetails['product_url'],
			'product_asin': proDetails['product_asin'],
			'product_name': proDetails['product_name'],
			'brand': proDetails['brand'],
			'star_rating': proDetails['star_rating'],
			'price': proDetails['price'],
			'old_price': proDetails['old_price'],
			'size': proDetails['size'],
			'color': proDetails['color'],
			'date_first_available':  proDetails['date_first_available'],
			'seller': proDetails['seller'],
			'offer_listing': offers_options,
			

		}
		# yield item
		reviews_link = f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber='
		page = 1
		for pages in range(page, 4):
		# 	start_urls.append(reviews_link+str(pages))
		# 	len_start = len(start_urls)
		# 	for i in range(len_start):
		# self.result = []9
			np = reviews_link + str(pages)
			yield scrapy.Request(url=np, headers=self.headers, callback=self.customer_reviews,priority=1,cb_kwargs = {'proDetail' : item})

	def customer_reviews(self, response,proDetail):

		# result = response.meta.get('result', [])
		date_list = []
		product_asin = proDetail['product_asin']
		item = AmazonInItem()
		r =[]
		count = 0
		reviews = response.xpath('//div[@data-hook="review"]')
		for review in reviews:
			data={'r': review.xpath(
					'//div[@class="a-profile-content"]/span/text()').extract_first()}
		#  = review
		yield data
		# review_date = response.xpath(
		# 				'//div[@data-hook="review"]//span[@data-hook="review-date"]/text()').extract()
		# len_review_date = len(review_date)
		# for i in range(len_review_date):
		# 	str_review_date = review_date[i]
		# 	date = dparser.parse(str_review_date, fuzzy=True).date()
		# 	date_list.append(date)
		# review_rating = response.xpath(
		# 				'//div[@data-hook="review"]//i[@data-hook="review-star-rating"]/span/text()').extract()
		# review_rating_formatted = [float(i[0:3]) for i in review_rating]
		# review_text = response.xpath(
		# 				'//div[@data-hook="review"]//span[@data-hook="review-body"]/span/text()').extract()
			
		
		# # yield {'r': review_author}
		# 	data = {'a' : review_author}
		# self.result.append(data)
		# # 	 'review_date' :date_list[count],
		# # 	 'review_rating' : review_rating_formatted[count],
		# # 	 'review_text' : review_text[count].encode("ascii", "ignore").decode().strip()}
			
		# 	# count += 1
		# # 	res.append(reviews)
		
		# cr = self.result if review_author else 'N'

		# # item = AmazonInItem()
		# # item['result'] = result
		# # yield item
		# yield {'cr' : cr}

		# next_page = response.xpath(
		# 	'//div[@data-hook="pagination-bar"]//a/@href').extract_first()
		# if next_page:
		# 	# next_page_url =  f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber='
		# 	# page = 2
		# 	# for pages in range(page,4):
		# 	# 	next_page_urls = next_page_url + str(pages)
		# 	# 	if pages <= 3:
		# 	# 		yield scrapy.Request(url = next_page_urls,headers=self.headers,callback = self.customer_reviews , cb_kwargs = {'proDetail':proDetail})
			
		# 	# 	else:
		# 	yield response.follow(next_page,headers = self.headers,callback = self.customer_reviews,cb_kwargs={'proDetail':proDetail} )

		# # else:
		# # 	yield {'r' : cr}
