# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:14:31 2019

@author: Dimitrid
"""

import bs4 as bs
import requests
import pandas as pd
from urllib.parse import unquote
import time
import concurrent.futures

# chage this link based on the area you want to select
url='https://www.spitogatos.gr/search/results/residential/rent/r100/m100m101m102m103m104m/'
     

headers={}
headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
link= unquote(url)
#    print(link)
text= requests.get(link, headers=headers).text
soup= bs.BeautifulSoup(text)

num_of_listing= soup.find('h2',class_="padding-left h5 searchTotalNumberOfResults").parent.find_next('b')
print(num_of_listing.text.strip())
lenght= int(float(num_of_listing.text.strip())*1000)

page_links=[]
for number in range(0,lenght,10):
        #print(number)
        url_pages = url + 'offset_' + str(number)
        page_links.append(url_pages)


posts=[]

t3=time.perf_counter()

def spitogatos_links(pages):
    req1= unquote(pages)
    resp1 = requests.get(req1,headers=headers).text
    soup1 = bs.BeautifulSoup(resp1,'html.parser')
    for post in soup1.find_all('div',class_="bd padding-right"):
        post= post.a.get('href')
        posts.append(post)
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(spitogatos_links, page_links)

t4= time.perf_counter()

print('Finished in: ', (t4-t3),' seconds')

prices=[]
pricesper=[]
sizes=[]
kinds=[]
heat_types=[]
num_of_rooms=[]
num_of_baths=[]
floors=[]
parking=[]
year_builts=[]
last_update=[]
area=[]
offices=[]

t1=time.perf_counter()

def spitogatos_posts(post):
    link = post
    link= unquote(link)
#    print(link)
    texts= requests.get(link, headers=headers).text
    soup2= bs.BeautifulSoup(texts)
    
    try:
        price= soup2.find('h6',string='Τιμή').parent.find_next('div') 
        prices.append(price.text.strip())
    except AttributeError:
        prices.append('None')
   
    try:
        priceper= soup2.find('h6', string='Τιμή ανά τ.μ.').parent.find_next('div')
        pricesper.append(priceper.text.strip())
    except AttributeError:
        pricesper.append('None')
    
    try:    
        size= soup2.find('h6', string='Εμβαδό').parent.find_next('div')
        sizes.append(size.text.strip())
    except AttributeError:
        sizes.append('None')
    
    try:
        kind= soup2.find('h6', string='Τύπος').parent.find_next('div')
        kinds.append(kind.text.strip())
    except AttributeError:
        kinds.append('None')
        
    try:
        num_of_room= soup2.find('h6', string='Υπνοδωμάτια').parent.find_next('div')
        num_of_rooms.append(num_of_room.text.strip())
    except AttributeError:
        num_of_rooms.append('None')
    
    try:
        num_of_bath= soup2.find('h6', string='Μπάνια').parent.find_next('div')
        num_of_baths.append(num_of_bath.text.strip())
    except AttributeError:
        num_of_baths.append('None')
    
    
    try:
        floor= soup2.find('h6', string='Όροφος').parent.find_next('div')
        floors.append(floor.text.strip())
    except AttributeError:
        floors.append('None')
    
    try:
        park= soup2.find('h6', string='Θέση στάθμευσης').parent.find_next('div')
        parking.append(park.text.strip())
    except AttributeError:
        parking.append('None')
    
    try:
        year_buitl= soup2.find('h6', string='Έτος κατασκευής').parent.find_next('div')
        year_builts.append(year_buitl.text.strip())
    except AttributeError:
        year_builts.append('None')
        
    try:
        last_updates= soup2.find('h6',string='Τελευταία ενημέρωση').parent.find_next('div')
        last_update.append(last_updates.text.strip())
    except AttributeError:
        last_update.append('None')
    
    try:
        areas= soup2.find('h6',string='Περιοχή').parent.find_next('div')
        area.append(areas.text.strip())
    except AttributeError:
        area.append('None')
        
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(spitogatos_posts, posts)        
        
t2= time.perf_counter()

print('Finished in: ', (t2-t1),' seconds')   

unique_info= pd.DataFrame(
                    {'prices':prices,
                     'priceper':pricesper,
                     'size':sizes,
                     'kind':kinds, 
                     'num_of_rooms':num_of_rooms,
                     'num_of_bath':num_of_baths,
                     'floor':floors,
                     'parking':parking,
                     'year_buitl':year_builts,
                     'last_update':last_update,
                     'area':area})    
    
unique_info.to_csv('spitogatos_athens.csv')

