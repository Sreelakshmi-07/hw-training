import scrapy
import datetime


class AmazonScrape(scrapy.Spider):

	# download_delay = 2

	name = 'gamingchairs'
	base_url = 'https://www.amazon.com/s?k=gaming+chairs&i=garden&rh=n%3A18682062011%2Cn%3A668180011&dc&page='
	headers = {
		# 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
		# 'sec-ch-ua-mobile': '?0',
		# 'sec-ch-ua-platform': '"Linux"',
		# 'Sec-Fetch-Dest': 'empty',
		# 'Sec-Fetch-Mode': 'cors',
			# 'Sec-Fetch-Site': 'same-site',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	def start_requests(self):

		page = 1

		next_page = self.base_url + str(page)

		yield scrapy.Request(url=next_page, headers=self.headers, callback=self.link_response
								 )

	def link_response(self, response):

		allowed_domain = 'https://www.amazon.com'

		links = response.xpath(
			'//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').extract()

		len_links = len(links)

		for i in range(len_links):

			link = links[i]

			if link.startswith('/gp/slredirect/picassoRedirect.html/') or link.startswith('/sspa/'):

				pass

			else:

				yield scrapy.Request(url=allowed_domain+link, headers=self.headers, callback=self.parse)
		next_page = response.xpath('//span[@class="s-pagination-strip"]/a[text()[contains(.,"Next")]]/@href').extract_first()
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(url = next_page,callback=self.link_response)
		else:
			print("end of page")

		

	def parse(self, response):

		# print(response.url)
		product_asin = response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th[text()[contains(.,'ASIN')]]/following-sibling::td/text()").extract_first().strip() or response.xpath(
			"//div[@class='a-expander-content a-expander-section-content a-section-expander-inner']/table[@id='productDetails_techSpec_section_1']/tr/th[text()[contains(.,'ASIN')]]/following-sibling::td/text()").extract_first().encode("ascii", "ignore").decode().strip()
		product_name = response.xpath('//span[@id="productTitle"]/text()').extract_first(
		).encode("ascii", "ignore").decode().strip().replace('\"', "")
		brand = response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th[text()[contains(.,'Brand')]]/following-sibling::td/text()").extract_first(
		) or response.xpath("//table[@class='a-normal a-spacing-micro']/tr[@class='a-spacing-small po-brand']/td[@class='a-span9']/span/text()").extract_first()
		product_brand = 'N/A' if brand is None else brand.encode(
			"ascii", "ignore").decode().strip()
		star_ratings = response.xpath(
			'//span[@class="a-icon-alt"][text()[contains(.,"out of 5 stars")]]/text()').extract_first()
		product_star_ratings = 0 if star_ratings is None else float(
			star_ratings[0:3])
		product_price = response.xpath(
			'//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]/span/text()').extract_first()
		product_price_list = 0 if product_price is None else float(
			product_price[1:].replace(",", ""))
		product_old_price = response.xpath(
			'//span[@class="a-size-small a-color-secondary aok-align-center basisPrice"]/span[@class="a-price a-text-price"]/span/text()').extract_first()
		product_old_price_list = 0 if product_old_price is None else float(
			product_old_price[1:].replace(",", ""))
		size = response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th[text()[contains(.,'Product Dimensions')]]/following-sibling::td/text()").extract_first() or response.xpath(
			"//div[@class='a-expander-content a-expander-section-content a-section-expander-inner']/table[@id='productDetails_techSpec_section_1']/tr/th[text()[contains(.,'Product Dimensions')]]/following-sibling::td/text()").extract_first()
		product_size = 'N/A' if size is None else size.encode(
			"ascii", "ignore").decode().strip().replace('\"', "")
		color = response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th[text()[contains(.,'Color')]]/following-sibling::td/text()").extract_first() or response.xpath(
			"//div[@class='a-expander-content a-expander-section-content a-section-expander-inner']/table[@id='productDetails_techSpec_section_1']/tr/th[text()[contains(.,'Color')]]/following-sibling::td/text()").extract_first()
		product_color = 'N/A' if color is None else color.encode(
			"ascii", "ignore").decode().strip()
		date = response.xpath("//table[@id='productDetails_detailBullets_sections1']/tr/th[text()[contains(.,'Date First Available')]]/following-sibling::td/text()").extract_first() or response.xpath(
			"//div[@class='a-expander-content a-expander-section-content a-section-expander-inner']/table[@id='productDetails_techSpec_section_1']/tr/th[text()[contains(.,'Date First Available')]]/following-sibling::td/text()").extract_first()
		date_formatted = 'N/A' if date is None else date.encode(
			"ascii", "ignore").decode().strip().replace(',', '')
		product_date = datetime.datetime.strptime(
			date_formatted, '%B %d %Y').date()

		yield {

			'product_url': response.url,
			'product_asin': product_asin,
			'product_name': product_name,
			'brand': product_brand,
			'star_rating': product_star_ratings,
				'price': product_price_list,
				'old_price': product_old_price_list,
				'size': product_size,
				'color': product_color,
				'date_first_available':  product_date

		}

		