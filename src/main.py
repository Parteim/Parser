from bs4 import BeautifulSoup as BS
import requests
import xlwt
import time


base_url = 'http://teh-treid.com'
products_urls = []
items_urls_list = []


def request(url, **kwargs):
    response = requests.get(
        url,
        params=kwargs
    )
    return response.content


def writer():
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Products')

    ws.write(0, 0, '_ID_')
    ws.write(0, 1, '_MAIN_CATEGORY_')
    ws.write(0, 2, '_CATEGORY_')
    ws.write(0, 3, '_NAME_')
    ws.write(0, 4, '_SKU_')
    ws.write(0, 5, '_MANUFACTURER_')
    ws.write(0, 6, '_PRICE_')
    ws.write(0, 7, '_QUANTITY_')
    ws.write(0, 8, '_DESCRIPTION_')
    ws.write(0, 9, '_IMAGE_')
    ws.write(0, 10, '_STATUS_')
    ws.write(0, 11, '_ATTRIBUTES_')
    ws.write(0, 12, '_IMAGES_')
    ws.write(0, 13, '_USE_')

    print(1)

    for num, product in enumerate(products_urls, 1):
        start = time.time()

        soup = BS(
            request(
                base_url+product
            ),
            'html.parser'
        )

        category_url = soup.find('div', class_='breadcrumbs').find_all('a')

        main_category = category_url[1].text
        category = category_url[2].text
        name = soup.find('div', class_='zagolovok').text
        sku = soup.find('div', class_='articul').text.split(' ')[1]
        price = soup.find('div', class_='price').text
        manufacturer = ' '
        use = ''
        texts = soup.find('div', class_='texts').find_all('p')
        print(texts)

        if 'Производитель' in texts[0].text:
            manufacturer = texts[0].text.split(':')[1]

        if 'Применение' in texts[1].text:
            use = texts[1].text.split(':')[1]

        print(
            f'main_category: {main_category}\n'
            f'category: {category}\n'
            f'name: {name}\n'
            f'sku: {sku}\n'
            f'price: {price}\n'
            f'manufacturer: {manufacturer}\n'
            f'use: {use}\n'
        )

        ws.write(num, 0, num)
        ws.write(num, 1, main_category)
        ws.write(num, 2, category)
        ws.write(num, 3, name)
        ws.write(num, 4, sku)
        ws.write(num, 6, price)
        ws.write(num, 5, manufacturer)
        ws.write(num, 13, use)

        wb.save('items.xls')

        end = time.time()

        print(end-start)


def get_items(soup):

    list_items = soup.find_all('div', class_='items')
    for item in list_items:
        item_url = item.find('a')['href']
        if item.find('div', class_='price') and item_url not in products_urls:
            products_urls.append(item_url)
            print('product', item_url)
        else:
            if item_url not in items_urls_list:
                items_urls_list.append(item_url)
                print("item url:", item_url)

    return items_urls_list


def run():
    start = time.time()

    url_zapchasty = 'http://teh-treid.com/catalog-zapchasti'
    soup = BS(request(url_zapchasty, show_elements=100), 'html.parser')

    get_items(soup)

    for item_url in items_urls_list:
        soup_of_item = BS(request(
            base_url + item_url,
            show_elements=100,
        ),
            'html.parser')
        get_items(soup_of_item)
        print(1, item_url)
        if len(products_urls) >= 5:
            break

    print(items_urls_list[-1])
    print(products_urls[-1])
    print(len(products_urls))

    end = time.time()
    print((end-start))

    second = time.time()
    writer()

    print(second-start)


if __name__ == '__main__':
    run()
