import scrapy
import datetime
import re
import dateutil.parser as dparser


class AmazonScrape(scrapy.Spider):

	# download_delay = 2

	name = 'gamingchairtest22'
	base_url = 'https://www.amazon.in/s?k=gaming+chairs&i=furniture&rh=n%3A976442031%2Cn%3A1380441031%2Cn%3A3591666031%2Cn%3A3591675031%2Cn%3A28205294031&dc&page='
	headers = {
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	def start_requests(self):

		for page in range(1, 4):
			next_page = self.base_url + str(page)

			yield scrapy.Request(url=next_page, headers=self.headers, callback=self.link_response
								 )

	def link_response(self, response):

		allowed_domain = 'https://www.amazon.in'

		links = response.xpath(
			'//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').extract()

		len_links = len(links)
		print(len_links)

		for i in range(len_links):

			link = links[i]

			if link.startswith('/gp/slredirect/picassoRedirect.html/') or link.startswith('/sspa/'):

				pass

			else:
				# pass
				yield scrapy.Request(url=allowed_domain+link, headers=self.headers, callback=self.parse)
		# next_page = response.xpath(
		# 	'//span[@class="s-pagination-strip"]/a[text()[contains(.,"Next")]]/@href').extract_first()
		# print(next_page)
		# if next_page:
		# 	next_page = response.urljoin(next_page)
		# 	print(next_page)
		# 	yield scrapy.Request(url=next_page, callback=self.link_response)
		# else:
	# 	# 	print("end of page")

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
		yield scrapy.Request(url=url_ajax, headers=self.headers, callback=self.ajax_requests,
							 cb_kwargs={'proDetails': proDetails}
							 )

	def ajax_requests(self, response, proDetails):

	
		product_asin = proDetails['product_asin']
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
			# 'review_list' : []


		}

		reviews_link = f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber='
		page = 1
		for pages in range(page,4):
			review_pages = reviews_link + str(pages)
			yield scrapy.Request(url=review_pages, headers=self.headers, callback=self.customer_reviews, cb_kwargs={'proDetail': item})

	def customer_reviews(self, response, proDetail):

		product_asin = proDetail['product_asin']
		date_list = []
		review_list = []
		count = 0
		review_author = response.xpath(
					'//div[@data-hook="review"]//div[@class="a-profile-content"]/span/text()').extract()
		review_date = response.xpath(
					'//div[@data-hook="review"]//span[@data-hook="review-date"]/text()').extract()
		len_review_date = len(review_date)
		for i in range(len_review_date):
			str_review_date = review_date[i]
			date = dparser.parse(str_review_date, fuzzy=True).date()
			date_list.append(date)
		review_rating = response.xpath(
					'//div[@data-hook="review"]//i[@data-hook="review-star-rating"]/span/text()').extract()
		review_rating_formatted = [float(i[0:3]) for i in review_rating]
		review_text = response.xpath(
					'//div[@data-hook="review"]//span[@data-hook="review-body"]/span/text()').extract()

		for review in review_author:
			review_list.append({ 'review_author' : review,
			 'review_date' :date_list[count],
			 'review_rating' : review_rating_formatted[count],
			 'review_text' : review_text[count].encode("ascii", "ignore").decode().strip()})
			count += 1
			
	
		customer_review = review_list if review_author else 'N/A'

		# next_page = response.xpath(
		# 	'//div[@data-hook="pagination-bar"]//a/@href').extract_first()
		# if next_page:
			
		# 	# page = 2
		# 	# next_page_url = re.sub("pageNumber=2","pageNumber="+str(page),next_page)
		# 	# if next_page_url <= 3:
		# 	# 	for page in range(2, 4):	
		# 	yield response.follow(url = next_page,headers=self.headers,callback = self.customer_reviews,cb_kwargs = {'proDetail':proDetail})
		# 	# else:


		# else:

		yield {
				'product_url': proDetail['product_url'],
				'product_asin': proDetail['product_asin'],
				'product_name': proDetail['product_name'],
				'brand': proDetail['brand'],
				'star_rating': proDetail['star_rating'],
				'price': proDetail['price'],
				'old_price': proDetail['old_price'],
				'size': proDetail['size'],
				'color': proDetail['color'],
				'date_first_available':  proDetail['date_first_available'],
				'seller': proDetail['seller'],
				'offer_listing': proDetail['offer_listing'],
				'reviews' :customer_review
		}
			
				
				# next_page_url =  f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber=' + str(page)
				# if page <= 2:
				# 	yield response.follow(url = next_page_url,headers=self.headers,callback = self.customer_reviews , cb_kwargs = {'proDetail':proDetail})
				# else:
				# 	yield response.follow(url = next_page_url,headers=self.headers,callback = self.customer_reviews , cb_kwargs = {'proDetail':proDetail})
