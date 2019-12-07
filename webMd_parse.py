# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 01:51:34 2017

@author: Dimitrid
"""
# I would not recommend to use this to parse the website. It was an initial try and it takes 5-6 hours to parse the entrire message board
import bs4 as bs
import requests
import urllib
import pandas as pd
import urllib.parse
import re
from urllib.parse import unquote
import time
from myprogressbar import printProgressBar
import concurent.futures


url='https://messageboards.webmd.com/'
headers={}
headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
req= urllib.request.Request(url, headers=headers)
source = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(source,'lxml')
    
df = pd.DataFrame(columns = ['link'],data=[url.a.get('href') for url in soup.find_all('div',class_="link")])
lists =[]
page_links = []

for i in range(len(df)):
    link = (df.link.iloc[i])
    req = urllib.request.Request(link, headers=headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    temp1=re.findall(r'Filter by</span>(.*?)data-pagedcontenturl',str(respData))
    temp1=re.findall(r'data-totalitems=(.*?)data-pagekey',str(temp1))[0]
    pageunm=round(int(re.sub("[^0-9]","",temp1))/10)
    lists.append(pageunm)
    

    for number in range(1,pageunm+1):
        url_pages = link + '#pi14=' + str(number)
        page_links.append(url_pages)

l= len(page_links)
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
count=0   
lists2=[]
for pages in page_links:
    link= unquote(pages)
    #   print(link)
    texts= requests.get(link, headers=headers).text
    soup1= bs.BeautifulSoup(texts)
    for body_links in soup1.find_all('div',class_="thread-detail"):
        body= body_links.a.get('href')
        lists2.append(body)
    count+=1
    time.sleep(0.01)
    printProgressBar(count,l , prefix = 'Progress:', suffix = 'Complete', length = 50)




usernames=[]
bodies=[]
dates=[]
titles=[]
tags=[]
categories=[]
l1= len(lists2)
printProgressBar(0,l1 , prefix = 'Progress:', suffix = 'Complete', length = 50)
count=0

def postscraper(post):
    post= unquote(post)
    posts= requests.get(post, headers=headers).text
    soup2= bs.BeautifulSoup(posts)
    username=soup2.find_all('div', class_="user-name")[0].get_text().strip()
    if username is not None:
          usernames.append(username)
    
    body= soup2.find_all('div',class_="thread-body")[0].get_text().strip()
    if body is not None:
        bodies.append(body)
   
    date = soup2.find_all('div',class_="thread-ago")[0].get_text().strip()
    if date is not None:
        dates.append(date)
        
    title= soup2.find_all('div',class_="thread-detail")[0].a.get_text().strip()
    if title is not None:    
        titles.append(title)
        
    tag= soup2.find_all('div',class_="thread-tags")[0].get_text().strip()
    if tag is not None:
        tags.append(tag)
        
    category= soup2.find_all('h1',class_="title")[0].get_text().strip()
    if category is not None:
        categories.append(category)

    count+=1
    printProgressBar(count, l1  , prefix = 'Progress:', suffix = 'Complete', length = 50)



unique_inf_parenting= pd.DataFrame(
                    {'title':titles,
                     'username':usernames,
                     'date':dates,
                     'body':bodies,
                     'tags':tags, 
                     'Category':categories})
    
    
    
posttags=pd.DataFrame({'tags':tags})
posttags.to_csv('tags_final')

categories_final = pd.DataFrame({'category':categories})
categories_final.to_csv('categories')
unique_inf_parenting.to_csv('WebMd-data.csv')

            
        
