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

# In[1]:


# import libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import numpy as np
pd.set_option("max_colwidth", 500)


# In[2]:


# exploring data
response = requests.get("https://www.privateislandsonline.com/search?availability=sale")
doc = BeautifulSoup(response.text, 'html.parser')
island_names = doc.select('.name')
for name in island_names:
    print(name.text.strip())

island_images = doc.select('.islandImageWithoutBg')
for image in island_images:
    print(image.get('src'))
    
island_acreage = doc.select('.num')
for acreage in island_acreage:
    print(acreage.text.strip())
    
island_price = doc.select('.list-price')
for price in island_price:
    print(price.text.strip())
    
island_region = doc.select('.list-name')
for region in island_region:
    print(region.text.strip())

island_tags = doc.select(".tags--listing")
for tag in island_tags:
    print(tag.text.strip())
    print(type(tag))


# In[3]:


# creating a function to strip new lines and currency symbols
import re

def clean_table(x):
    x = x.replace("\n", "").strip()
    x = x.replace('$', "")
    return x


# In[4]:


# # testing loop on first page
# response = requests.get("https://www.privateislandsonline.com/search?availability=sale")
# doc = BeautifulSoup(response.text, 'html.parser')

# islands = doc.select('.grid')


# rows = []

# for island in islands:
#     print('-----')
#     row = {}
    
#     row['name'] = island.select_one('.name').text.strip()
#     try:
#         row['image'] = island.select_one('.islandImageWithoutBg')['src']
#     except:
#         print('No image link')
    
#     try:
#         row['acreage'] = island.select_one('.num').text.strip()
#     except:
#         print('No acreage')

#     try:
#         row['price'] = clean_table(island.select_one('.list-price').text.strip())
#     except:
#         print('No price')
    
#     try:
#         row['region'] = clean_table(island.select_one('.list-name').text.strip())
#     except:
#         print('No region data')
        
#     try:
#         row['tags'] = clean_table(island.select_one(".tags--listing").text.strip())
#     except: 
#         print('No tags')
    

    
#     print(row)
#     rows.append(row)

# island_df = pd.DataFrame(rows)
# island_df


# In[5]:


# url = "https://www.privateislandsonline.com/search?availability=sale"
# page = 76
# island_data = []


# # max_num=0
# # for item in doc.select_one(".pagination"):
# #     if len(item.select('a'))>0:
# #         if item.select('a')[0].text !="»":
# #             if int(item.select('a')[0].text)>max_num:
# #                 max_num = int(item.select('a')[0].text)
# # print(max_num)

# while True:
#     print("---")
#     url = f"https://www.privateislandsonline.com/search?availability=sale&page={page}"
#     print("Requesting", url)
#     response = requests.get(url)
#     doc = BeautifulSoup(response.text, 'html.parser')

    
#     if len(doc.select('.grid')) ==0:
#         break
    
#     islands = doc.select('.grid')
#     rows = []
    
#     for island in islands:
#         print('-----')
#         row = {}

#         row['name'] = island.select_one('.name').text.strip()
#         try:
#             row['image'] = island.select_one('.islandImageWithoutBg')['src']
#         except:
#             print('No image link')

#         try:
#             row['acreage'] = island.select_one('.num').text.strip()
#         except:
#             print('No acreage')

#         try:
#             row['price'] = clean_table(island.select_one('.list-price').text.strip())
#         except:
#             print('No price')

#         try:
#             row['region'] = clean_table(island.select_one('.list-name').text.strip())
#         except:
#             print('No region data')

#         try:
#             row['tags'] = clean_table(island.select_one(".tags--listing").text.strip())
#         except: 
#             print('No tags')

#         print(row)
#         rows.append(row)
    
    
#     island_data.extend(doc)
#     page = page + 1
    
# island_df = pd.DataFrame(rows)
# island_df


# In[6]:


#iterate through all pages to grab data
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


# In[7]:


#send data to dataframe
island_df = pd.DataFrame(rows)


# In[8]:


#clean tags
island_df['tags'] = island_df.tags.str.replace(r'([a-z])([A-Z])', r'\1,\2', regex=True)


# In[9]:


#add scrape date
from datetime import datetime

island_df['scrape_date'] = pd.datetime.today().date()


# In[10]:


#replace null values with np.nan
island_df['tags'] = island_df.tags.replace(r'^\s*$', np.nan, regex=True)


# In[11]:


island_df['region'] = island_df.region.replace(r'(\s,)', ',', regex = True)


# In[12]:


island_df


# In[13]:


# island_df[island_df.name == "Burts Island"]


# In[14]:


# #read baseline scraped data for full archiving
url = 'https://raw.githubusercontent.com/swatiyengar/privateIslandScraper/main/island_scrape.csv'
private_islands = pd.read_csv(url, error_bad_lines=False)


# In[15]:


#append scraped data frame to baseline scrape
private_islands = private_islands.append(island_df, ignore_index = True).drop(columns = 'Unnamed: 0')


# In[18]:


#drop duplicates
private_islands.drop_duplicates(subset = ['name','price', 'region','tags', 'acreage', 'image'], keep = 'first')


# In[19]:


#send new file to island scrape
island_df.to_csv('island_scrape.csv')


# In[20]:


#take the newest scraped dataframe and clean price data
island_df['price'] = island_df.price.str.replace(',', '').str.replace(r'[a-zA-Z]', '')
island_df['price'] = pd.to_numeric(island_df['price'], errors = 'coerce')


# In[21]:


island_df.sort_values('price')


# In[22]:


#drop nas
island_df = island_df.dropna(subset = ['price'])


# In[23]:


#send newest scrape to file specifically for data viz
island_df.to_csv('island_scrape_weekly.csv')

