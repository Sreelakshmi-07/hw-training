import scrapy


class OlxScrap(scrapy.Spider):

    fieldname=['property_name','property_id','breadcrumbs','price','img','description','seller_name','location','property_type','bathroom','bedrooms']
    name = 'olx'
    base_url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page='
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    def start_requests(self):
        for page in range(1, 2):
            next_page = self.base_url + str(page)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.link_requests)



    def link_requests(self, response):

        allowed_domain = 'http://www.olx.in'
        for houses in response.xpath("//ul[@data-aut-id='itemsList']/li"):
            link = houses.xpath('a/@href').extract_first()

            if link is not None:

                yield scrapy.Request(
                    url=allowed_domain+link, headers=self.headers,callback = self.parse)

    def parse(self,response):

                list1 = ' '.join(map(str,
                        response.xpath("//span[@data-aut-id='itemPrice']/text()"
                                        ).getall()))

                convert_list = list1.split(' ')
                for price_dict in range(len(convert_list)):

                        price_dict = {'amount': convert_list[0]}
                price_dict = {
                        'amount': convert_list[-1],
                        'currency': convert_list[0]
                        }

                bathroom = response.xpath("//div/span[@data-aut-id='value_bathrooms']/text()"
                                                            ).get()

                bathrooms = 0 if bathroom is None else ''.join(bathrooms for bathrooms in bathroom if bathrooms.isdigit())


                bedroom = response.xpath("//div/span[@data-aut-id='value_rooms']/text()"
                                                            ).get() 
                
                bedrooms = 0 if bedroom is None else ''.join(bedrooms for bedrooms in bedroom if bedrooms.isdigit())
                

                yield {
                    'property_name': response.xpath("//h1[@data-aut-id='itemTitle']/text()"
                                                         ).get(),
                    'property_id': ' '.join(map(str,
                                                    response.xpath("//div/strong[contains(text(),'AD ID')]/text()"
                                                                    ).re(r"\d+"))),
                    'breadcrumbs': response.xpath("//div[@data-aut-id='breadcrumb']/div/ol/li/a/text()"
                                                       ).getall(),
                    'price': price_dict,
                    'img': response.xpath("//figure/img[@class='_39P4_']/@src"
                                               ).get(),
                    'description':response.xpath("//div[@data-aut-id='itemDescriptionContent']/p/text()"
                                                       ).get(),
                    'seller_name': response.xpath("//div[@data-aut-id='profileCard']/div/a/div/text()"
                                                       ).get(),
                    'location': response.xpath("//div[@data-aut-id='itemLocation']/div/span/text()"
                                                    ).get(),
                    'property_type': response.xpath("//div/span[@data-aut-id='value_type']/text()"
                                                         ).get(),
                    'bathroom':int(bathrooms),
                    'bedrooms': int(bedrooms),
                }


