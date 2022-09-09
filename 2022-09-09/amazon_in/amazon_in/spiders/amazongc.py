import scrapy
import datetime
import dateutil.parser as dparser
import logging


class AmazonScrape(scrapy.Spider):

    # download_delay = 1
    name = 'gamingchairs'
    base_url = 'https://www.amazon.in/s?k=gaming+chairs&i=furniture&rh=n%3A976442031%2Cn%3A1380441031%2Cn%3A3591666031%2Cn%3A3591675031%2Cn%3A28205294031&dc&page='
    headers = {
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-platform': '"Linux"',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    def start_requests(self):

        page = 1
        start_url = self.base_url + str(page)

        yield scrapy.Request(
            url=start_url, headers=self.headers, callback=self.parse_link
        )

    def parse_link(self, response):

        allowed_domain = 'https://www.amazon.in'
        links = response.xpath(
            '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href'
        ).extract()
        len_links = len(links)

        for href in range(len_links):

            link = links[href]

            if link.startswith(
                '/gp/slredirect/picassoRedirect.html/'
            ) or link.startswith('/sspa/'):

                pass

            else:

                url = allowed_domain + link
                yield scrapy.Request(
                    url=url, headers=self.headers, callback=self.parse
                )

        next_page = response.xpath(
            '//span[@class="s-pagination-strip"]\
            /a[text()[contains(.,"Next")]]/@href'
        ).extract_first()
        if next_page:

            yield response.follow(url=next_page, callback=self.parse_link)

        else:

            logging.warning('End of page')

    def parse(self, response):

        # Retrieving product information

        product_url = response.url
        product_asin = response.xpath(
            '//span[text()[contains(.,"ASIN")]]/following-sibling::span/text()\
            | //th[text()[contains(.,"ASIN")]]/following-sibling::td/text()'
        ).extract_first().encode("ascii", "ignore").decode().strip()
        product_name = response.xpath(
            '//span[@id="productTitle"]/text()'
        ).extract_first().encode("ascii", "ignore").decode().strip().replace(
            '\"', "")
        star_ratings = response.xpath(
            '//div[@id="averageCustomerReviews"]\
            //span[@class="a-icon-alt"]\
            [text()[contains(.,"out of 5 stars")]]/text()'
        ).extract_first()
        product_star_ratings = 0 if star_ratings is None else float(
            star_ratings[0:3])
        # Formatting list price and MRP price into float
        product_price = response.xpath(
            '//div[@id="apex_desktop"]\
            //span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]\
            /span/text()\
            | //span[@class="a-price a-text-price a-size-medium apexPriceToPay"]\
            /span/text()').extract_first()
        product_price_list = 0 if product_price is None else float(
            product_price[1:].replace(",", ""))
        product_price_formatted = format(product_price_list, '.2f')
        product_old_price = response.xpath(
            '//div[@id="apex_desktop"]\
            //span[@class="a-price a-text-price"]/span/text()\
            | //span[@class="a-price a-text-price a-size-base"]\
            /span/text()'
        ).extract_first()
        product_old_price_list = 0 if product_old_price is None else float(
            product_old_price[1:].replace(",", ""))
        product_old_price_formatted = format(product_old_price_list, '.2f')
        for details in response.xpath(
            '//div[@id="detailBullets_feature_div"]\
             | //div[@id="prodDetails"]'):

            product_brand = details.xpath(
                '//span[text()[contains(.,"Importer")]]\
                /following-sibling::span/text()\
                | //th[text()[contains(.,"Brand")]]\
                /following-sibling::td/text()'
            ).extract_first(default='N/A').encode(
                "ascii", "ignore").decode().strip()
            product_size = details.xpath(
                '//span[text()[contains(.,"Product Dimensions")]]\
                /following-sibling::span/text()\
                | //th[text()[contains(.,"Product Dimensions")]]\
                /following-sibling::td/text()'
            ).extract_first(default='N/A').encode(
                "ascii", "ignore").decode().strip().replace('\"', "")
            product_color = details.xpath(
                '//span[text()[contains(.,"Colour")]]\
                /following-sibling::span/text()\
                | //th[text()[contains(.,"Colour")]]\
                /following-sibling::td/text()'
            ).extract_first(default='N/A').encode(
                "ascii", "ignore").decode().strip()
            date = details.xpath(
                '//span[text()[contains(.,"Release date")]]\
                /following-sibling::span/text()\
                | //th[text()[contains(.,"Date First Available")]]\
                /following-sibling::td/text()'
            ).extract_first()
            product_date = 'N/A' if date is None \
                else datetime.datetime.strptime(
                    date.encode(
                        "ascii", "ignore").decode().strip(), '%d %B %Y').date()
        product_sold_by = response.xpath(
            '//div[@id="merchant-info"]/a/span/text()\
            | /a[@id="sellerProfileTriggerId"]/text()'
        ).extract_first()
        product_seller = 'N/A' if product_sold_by is None else \
            product_sold_by.encode(
                "ascii", "ignore").decode().strip()

        proDetails = {
            'product_url': product_url,
            'product_asin': product_asin,
            'product_name': product_name,
            'brand': product_brand,
            'star_rating': product_star_ratings,
            'price': product_price_formatted,
            'old_price': product_old_price_formatted,
            'size': product_size,
            'color': product_color,
            'date_first_available': product_date,
            'seller': product_seller,
            'reviews': []
        }
        reviews_link = f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber='
        page = 1
        review_pages = reviews_link + str(page)
        yield scrapy.Request(
            url=review_pages, headers=self.headers,
            callback=self.parse_customer_reviews, priority=1,
            cb_kwargs={
                'proDetail': proDetails
            }
        )

    def parse_customer_reviews(self, response, proDetail):

        product_asin = proDetail['product_asin']
        no_reviews = response.xpath(
            '//div[@data-hook="arp-no-reviews-some-ratings-message"]')
        if no_reviews:

            customer_review = 'N/A'
        else:

            reviews_list = response.xpath(
                '//div[@id="cm_cr-review_list"]//div[@data-hook="review"]')

            for review in reviews_list:

                review_dict = {}
                review_dict['review_author'] = review.xpath(
                    './/div[@class="a-profile-content"]/span/text()'
                ).extract_first()
                review_date = review.xpath(
                    './/span[@data-hook="review-date"]/text()').extract_first()
                review_dict['review-date'] = dparser.parse(
                    review_date, fuzzy=True).date()
                review_rating = review.xpath(
                    './/i[@data-hook="review-star-rating"]/span/text()'
                ).extract_first()
                review_dict['review_rating'] = float(review_rating[0:3])
                review_dict['review_text'] = review.xpath(
                    './/span[@data-hook="review-body"]/span/text()'
                ).extract_first(default='N/A').encode(
                    "ascii", "ignore").decode().strip()
                proDetail['reviews'].append(review_dict)

            customer_review = proDetail['reviews'] if reviews_list else 'N/A'

        proDetail = {
            'product_url': proDetail['product_url'],
            'product_asin': proDetail['product_asin'],
            'product_name': proDetail['product_name'],
            'brand': proDetail['brand'],
            'star_rating': proDetail['star_rating'],
            'price': proDetail['price'],
            'old_price': proDetail['old_price'],
            'size': proDetail['size'],
            'color': proDetail['color'],
            'date_first_available': proDetail['date_first_available'],
            'seller': proDetail['seller'],
            'reviews': customer_review

        }

        next_page = response.xpath(
            '//div[@data-hook="pagination-bar"]//a/@href').extract_first()
        if next_page:

            next_page_url = f'https://www.amazon.in/product-reviews/{product_asin}?reviewerType=all_reviews&pageNumber='
            for pages in range(2, 4):

                next_page_urls = next_page_url + str(pages)
                yield response.follow(
                    url=next_page_urls, headers=self.headers,
                    callback=self.parse_customer_reviews,
                    cb_kwargs={
                        'proDetail': proDetail
                    }
                )

        url_ajax = f'https://www.amazon.in/gp/product/ajax/ref=auto_load_aod?asin={product_asin}&pc=dp&experienceId=aodAjaxMain'

        yield scrapy.Request(
            url=url_ajax, headers=self.headers,
            callback=self.parse_ajax_requests,
            cb_kwargs={
                'proDetails': proDetail
            })

    def parse_ajax_requests(self, response, proDetails):

        # Retreving more seller options

        offers_option_list = []
        for offer_list in response.xpath('//div[@id="aod-offer-list"]'):
            # Formatting prices into float
            product_price_option = offer_list.xpath(
                '//div[@id="aod-offer"]//span[@class="a-offscreen"]/text()'
            ).extract()
            product_price_option_formatted = [
                price_format.replace(
                    ',', '') for price_format in product_price_option
            ]
            product_price_option_float = [
                float(price_float[1:]) for price_float in product_price_option_formatted
            ]
            product_seller_option = offer_list.xpath(
                '//div[@id="aod-offer-soldBy"]\
                //*[contains(@aria-label, "Opens a new page")]/text()'
            ).extract()
            product_seller_option_formatted = [
                seller_formatted.strip() for seller_formatted in product_seller_option]
            for price, seller in zip(
                product_price_option_float, product_seller_option_formatted
            ):
                offers_option_dict = {'offer_price': format(
                    price, '.2f'), 'seller': seller}
                offers_option_list.append(offers_option_dict)
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
            'date_first_available': proDetails['date_first_available'],
            'seller': proDetails['seller'],
            'offer_listing': offers_options,
            'reviews': proDetails['reviews']
        }

        yield item
