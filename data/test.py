#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description: 
#=======================================
#import helpers
from bs4 import BeautifulSoup
#import BeautifulSoup
import re 
from urllib import urlopen
import httplib,urllib
import sys
import urllib2, urllib
import redis

import simplejson as json
def json_encode(dict_data):
    if not dict_data:
        return json.dumps('')
    try:
        return json.dumps(dict_data, default=_json_handler)
    except:
        raise ValueError

path = sys.argv[1]
print path
dinner = path.split('.')[0]
print dinner
c = redis.Redis(host='127.0.0.1', port=6379, db=1)
with open ("%s"%path,"r") as data:
    webdata = data.read()
soup = BeautifulSoup(''.join(webdata))
all = soup
all_list = all.findAll('ul',attrs={"class":"all_dishes_list"})
for ul in all_list:
    for lis in ul.contents:
        if type(lis) != type(ul.contents[0]):
            cate = lis.find('h2').string
            menu = {}
            dishes = []
            menu["category"] = cate
            print cate
            for li in lis.findAll('li'):
                name = li.find('span',{"class":"dishes_name_r"}).string
                price = li.find('span',{"class":"dishes_price"}).string
                price = int(float(price) * 100)
                dish = {}
                dish['name'] = name.strip("...").strip("+")
                dish['price'] = price
                print dish['name']
                print dish['price']
                dishes.append(dish)
            menu["dishes"] = dishes
            menu =  helpers.json_encode(menu)
            #print menu
            c.lpush("dinner:data:%s"%dinner,menu)
            #kfc.append(menu)


'''
{
    "name": "肯德基",
    "content": [
        {
            "category": "cate",
            "dishes": [
                {
                    "name": "name",
                    "price": "price"
                },
                {
                    "name": "name",
                    "price": "price"
                }
            ]
        },
        {
            "category": "cate",
            "dishes": [
                {
                    "name": "name",
                    "price": "price"
                },
                {
                    "name": "name",
                    "price": "price"
                }
            ]
        }
    ]
}
'''
'''
[
    {
        "category": "cate",
        "dishes": [
            {
                "name": "name",
                "price": "price"
            },
            {
                "name": "name",
                "price": "price"
            }
        ]
    },
    {
        "category": "cate",
        "dishes": [
            {
                "name": "name",
                "price": "price"
            },
            {
                "name": "name",
                "price": "price"
            }
        ]
    }
]
'''
