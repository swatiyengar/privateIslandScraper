#!/usr/bin/env python
# coding: utf-8

# # Private Island Scraper
# 
# Don't we all day dream about having "Bezos" money? Or at minimum, "David Schwimmer" money? I certainly do...and maybe I'd throw a few 'pennies' down on a private island. 
# 
# This scraper will tell me the list prices for private islands for sale every week based on the listings found in [Private Islands, Inc](https://www.privateislandsonline.com/search?availability=sale)

# Elements of the Private Island Database include: 
# - Name (class_ = "name")
# - Image (class_ = "img-container")
# - Acreage (class_ = "num")
# - Price in USD (class_ = "list-price")
# - Country (class_ = "list-name" a href = )
# - Continent (class_ = "list-name" a href = )
# - Type of Development
# - Type of Island
# - Type of Lifestyle
# - Tag list (class_ = "tags tags--listing")

import itertools
rows=[]
for i in itertools.count(start=1):
    url = f"https://www.privateislandsonline.com/search?availability=sale&page={i}"
    print(url)
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    if len(doc.select('.grid'))==0:
        break
    else:
        islands = doc.select('.grid')
        for island in islands:
            print('-----')
            row = {}
            row['name'] = clean_table(island.select_one('.name').text.strip())
            try:
                row['image'] = island.select_one('.islandImageWithoutBg')['src']
            except:
                print('No image link')
            try:
                row['acreage'] = island.select_one('.num').text.strip()
            except:
                print('No acreage')
            try:
                row['price'] = clean_table(island.select_one('.list-price').text.strip())
            except:
                print('No price')
            try:
                row['region'] = clean_table(island.select_one('.list-name').text.strip())
            except:
                print('No region data')
            try:
                row['tags'] = clean_table(island.select_one(".tags--listing").text.strip())
            except: 
                print('No tags')
            print(row)
            rows.append(row)

island_df = pd.DataFrame(rows)

island_df['tags'] = island_df.tags.str.replace(r'([a-z])([A-Z])', r'\1,\2', regex=True)

island_df.to_csv('island_scrape.csv')

island_df['price'] = island_df.price.str.replace(',', '').str.replace(r'[a-zA-Z]', '')
island_df['price'] = pd.to_numeric(island_df['price'], errors = 'coerce')
island_df = island_df.dropna(subset = ['price'])
island_df.to_csv('island_scrape_for_viz.csv')