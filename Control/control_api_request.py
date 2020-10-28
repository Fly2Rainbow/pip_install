import numpy as np
import os.path
import sys
sys.path.append('C:\\PythonWorkspace\\Workwiz\\Model')
sys.path.append('C:\\PythonWorkspace\\Workwiz\\Control')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.insert(0, "C:\\PythonWorkspace\\Workwiz\\Model\\model_saramin.py")
# print(sys.path)
import Utils as log
from Model import model_saramin as msa  
import requests
import xml.etree.ElementTree as ET
import datetime

logger = log.CreateLogger('Saramin_Crawling')

def checkCondition(URL, headers, key_no, page_no):
    condition = True
    req = requests.get(URL, headers=headers)
    root = ET.fromstring(req.text)
    pages = root.find('./jobs/job/id')
    reg_code = root.findtext('code')
    #print('errCode=', err)
    if  reg_code == '4' or reg_code == '2': 
        key_no += 1
        page_no = page_no - 1
        print(f'인증키 갱신 key={key_no} / Pages = {page_no}')
        return condition, URL, key_no, page_no, root, reg_code

    if pages is None: 
        print(root.text)
        condition = False
        #print('condition = false :')
        return condition, URL, key_no, page_no, root, reg_code
    
    return condition, URL, key_no, page_no, root, reg_code


def setUpURL(arg, page_no, key_no):
    URL, headers = msa.set_api(arg, key_no, page_no)
    condition, URL, key_no, page_no, root, reg_code = checkCondition(URL, headers, key_no, page_no)
    
    return condition, page_no, key_no, root, reg_code


def resp_api_saramin(arg, page_no):
    sTime = datetime.datetime.now()
    logger.info(f'Start resp_api_saramin:: [Saramin] "{sTime}"')
    status = True
    result = []
    key_no = 0
    page_no = 0  # 시작페이지
    while True:
        condition, page_no, key_no, root, reg_code = setUpURL(arg, page_no, key_no)
        page_no += 1
        key_no = key_no
        if not condition: 
            print('End Page::: ', page_no)
            print('break:::')
            status = False
            break
        if reg_code == '4' or reg_code == '2':
            logger.info(f'Registry Code Error::: {reg_code}')
            # condition, page_no, key_no, root, reg_code = setUpURL(arg, page_no, key_no)
            continue
        result.append(root)
        print(f'while key_no={key_no} :: Page_No={page_no}')
    
    return result, status





