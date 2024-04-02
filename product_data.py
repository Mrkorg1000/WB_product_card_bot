import aiohttp
import re


# Название, артикул, цена, рейтинг товара, количество товара НА ВСЕХ СКЛАДАХ.

def get_product_overall_quantity(text):
    quantity_pattern = r'"qty":(\d+),'
    result = re.findall(quantity_pattern, text)
    quantity = sum([int(i) for i in result])

    return quantity


def get_product_name(text):
    name_pattern = r'"name":"([А-ЯЁ][^"]+)",'
    product_name = re.search(name_pattern, text).group(1)

    return product_name


def get_product_price(text):
    price_pattern = r'"salePriceU":(\d+),'
    product_price = re.search(price_pattern, text).group(1)

    return int(product_price[:-2])


def get_product_rating(text):
    rating_pattern = r'"supplierRating":([0-9]*[.][0-9]*),'
    product_rating = re.search(rating_pattern, text).group(1)

    return product_rating


async def get_product_data(product_id):
    async with aiohttp.ClientSession() as session:
        print(session)
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={product_id}"
        async with session.get(url) as response:
            text = await response.text()
            name = get_product_name(text)
            product_id = product_id
            price = get_product_price(text)
            rating = get_product_rating(text)
            quantity = get_product_overall_quantity(text)

            return name, product_id, price, rating, quantity


def get_articul(text):
    articul_pattern = r'Артикул (\d+)\n'
    articul = re.search(articul_pattern, text).group(1)

    return articul 


