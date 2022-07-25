import requests
import json
from parsel import Selector

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}
url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page="

properties = []
for page in range(1, 6):
    next_page = url + str(page)
    print(next_page)
    pages = requests.get(next_page, headers=headers).text
    selector = Selector(text=pages)

    allowed_domain = "http://www.olx.in"
    for houses in selector.xpath("//ul[@data-aut-id='itemsList']/li"):

        link = houses.xpath("a/@href").extract_first()

        if link is not None:

            print(link)

            item_response = requests.get(
                url=allowed_domain + link, headers=headers).text
            item_data = Selector(text=item_response)
            list1 = " ".join(
                    map(
                        str,
                        item_data.xpath(
                            "//section[@class='_2wMiF']/span[@class='_2xKfz']/text()"
                        ).getall(),
                    )
            )

            convert_list = list1.split(" ")
            for price_dict in range(len(convert_list)):

                price_dict = {"amount": convert_list[0]}
            price_dict = {
                "amount": convert_list[-1], "currency": convert_list[0]}

            properties.append({

                'property_name': item_data.xpath(
                    "//div[@class='rui-2CYS9']/section[@class='_2wMiF']/h1[@class='_3rJ6e']/text()"
                ).get(),
                'property_id': " ".join(
                    map(
                        str,
                        item_data.xpath(
                            "//div[@class='fr4Cy']/strong/text()"
                        ).re(r"\d+"),
                    )
                ),
                'breadcrumbs': item_data.xpath(
                    "//ol[@class='rui-10Yqz']/li/a/text()"
                ).getall(),
                'price': price_dict,
                'img': item_data.xpath(
                    "//figure/img[@class='_39P4_']/@src"
                ).get(),
                'description': " ".join(
                    map(
                        str,
                        (
                            item_data.xpath(
                                '//*[@id="container"]/main/div/div/div/div[4]/section[1]/div/div/h3[2]/span/text()'
                            ).get(),
                            item_data.xpath(
                                '//*[@id="container"]/main/div/div/div/div[4]/section[1]/div/div/div[2]/p/text()'
                            ).get(),
                        ),
                    )
                ),
                'seller_name': item_data.xpath(
                    "//div[@class='_3oOe9']/text()"
                ).get(),
                'location': item_data.xpath(
                    "//div[@class='_2A3Wa']/span[@class='_2FRXm']/text()"
                ).get(),
                'property_type': item_data.xpath(
                    "//div[@class='_3_knn'][1]/div[@class='_2ECXs']/span[@class='_2vNpt']/text()"
                ).get(),
                'bathroom': item_data.xpath(
                    "//div[@class='_3_knn'][3]/div[@class='_2ECXs']/span[@class='_2vNpt'][position()=1]/text()"
                ).get(),
                'bedrooms':
                    item_data.xpath(
                        "//div[@class='_3JPEe']/div[@class='_3_knn'][2]/div[@class='_2ECXs']/span[@class='_2vNpt'][position()=1]/text()"
                ).get(),
            })

        filename = f"olx_house_properties.json"
        with open(filename, "w") as f:
            f.write(json.dumps(properties, indent=4))
