import xml.etree.ElementTree as ET
import requests
import xmltodict
import json
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import datetime
import numpy as np


access_key_sa = [
    'oABj4P5DPdMeQYOD6MiojOau0V4eO2PGQt8GCRiytoFrpq5vHpOG',
    'tNhJjw8rjeJ02koc0dzYXOHoa2lobdysuVd3wMV9fVmg28WiPBG',
    'apNPeyfia5Er2TWiC14nluj4NnRFz4onHHETo5ANYZyi6MNzhsO',
    'z9e2CRM9ytxHaA2W9FCoOvkP770IDhyVfkY5VZbNczZ8Uv1u0y',
    'qapOoQuojX76OA7WV3qye6Olyw1Q83coUXqnwYCxXpg4kB7Ela',
    'jo7abWobJ9jUElhiCiAcjeY06pN8ClISZpKQPHE5NEztfsniLYG',
    'KP7xtZEXslt47atHqRtECeAfTxb6i0dxWF8nZbWGnNRgq8AfLmGC',
    'zO2S04ShRmktKDMsxeEO4pWHrSyzg6NB4ISlgDhqEVjv5PV3Ba',
    'JgtMgeO8H9YnQVMxUGRLuE9zvgfuLsrVtD28Yq86GxTCGdnkkC',
    'KQEbnI89RuK9eOgqRYOvukpOqFKDDGu9C8GBelQAyB9SUmeYZ2a'
]

def set_api(n, arg, key):
    condition = True
    getDate = str(datetime.date.today() - datetime.timedelta(1))
    headers = {'Accept': 'application/xml; charset=utf-8'}
    URL = 'https://oapi.saramin.co.kr/job-search' +\
    '?fields=count,keyword-code,posting-date,expiration-date' +\
    '&count=110' +\
    '&' + arg + '=' + getDate +\
    '&access-key=' + access_key_sa[key] +\
    '&start=' + str(n)
    #print(URL)
    req = requests.get(URL, headers=headers)
    root = ET.fromstring(req.text)
    pages = root.find('./jobs/job/id')
    err = root.findtext('code')
    #print('errCode=', err)
    if  err == '4': 
        key += 1
        n = n - 1
        print('인증키 갱신 key=', key)
        return condition, [], key, n

    if pages is None: 
        condition = False
        #print('condition = false :')
        return condition, [], key, n
    
    arr_id = [child.text for child in root.iter('id')] #modification-timestamp
    arr_id = np.array(arr_id)
    
    return condition, arr_id, key, n

def get_api_saramin(arg, key):
    re = []
    re = np.array(re)
    n = 0  # 시작페이지
    while True:
        condition, arr_id, key, n = set_api(n, arg, key)
        if not condition: 
            print('break:::')
            break
        #try:
        result = np.concatenate([re, arr_id])
        re = result
        n += 1
        # except Exception as e:
        #     condition, arr_id, key, n = set_api(n, arg, key)
        #     print(e)
        
    return re
'''
print(datetime.datetime.now())
p = get_api_saramin('published', 0)
print(datetime.datetime.now())
u = get_api_saramin('updated', 0)
print(datetime.datetime.now())
#print(p)
print('Published id:::', len(p))
print('Published Overlap id:::', len(set(p)))
#print(u)
print('Updated id:::', len(u))
print('Updated Overlap id:::', len(set(u)))

#s = set(u)
#print(s)
#temp3 = [x for x in set(final_result)if x not in s] #순서 보존됨
temp3 = [x for x in p if x not in u] 
temp4 = [x for x in p if x in u] 
print('Unique id:::', len(temp3))
print('Equal id:::', len(temp4))
print(temp4)
print(datetime.datetime.now())
#print(n-1)
'''
# result = {}
# re = ''
# s_tag = ''
# tag_attr = ''
# class MyHTMLParser(HTMLParser):
    
#     def handle_starttag(self, tag, attrs):
#         global result
#         global re, tag_attr, s_tag
#         # dt = tag + attrs
#         #result = result[tag] 
#         if attrs is not None:
#             tag_attr = attrs
#         s_tag = tag
#         re = s_tag, ':', tag_attr
#         #print("Encountered a start tag:", tag_name, ':', tag_attr)
#         if s_tag == 'job':
#             print('#'*150)
#         return print(re)

#     def handle_endtag(self, tag):
#         #print("Encountered an end tag :", tag, "-", re)
#         return

#     def handle_data(self, data):
#         global s_tag
#         global tag_attr
        
#         #s_tag = str(self.__getattribute__())
#         print("InnerText: ", s_tag, ",", data)
#         if len(tag_attr) > 0:
#             print("attr: ", tag_attr)
#         tag_attr = None

    #result[handle_starttag.tag] = handle_data.data

# parser = MyHTMLParser()
# parser.feed(req.text)
