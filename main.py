import os.path
import sys
from Control import control_api_request as apic
from Control import control_dataframe as dfc
from Control import control_dbConnect as dc
from Control import control_etc as etc
# from Control import control_htmlParsing as craw
from Model import model_saramin as sm
from Model import model_jobkorea as jm
from Model import model_worknet as wm
from Control import control_htmlParsing as craw
from Control import Utils as log

def saramin():
    # status = True
    # result = []
    # result, status = apic.resp_api_saramin('upublished', 0)
    # df = dfc.make_dataframe(result) # xml to df
    # df, result = dc.setDFtoDB(df)  # DB setup z_api_saramin_all used df
    # # df = dfc.getDBmakeDF("SELECT * FROM z_api_saramin_all;") # 테스트용
    df = dfc.setSaraminCols()  # api_saramin_1todayGet DB to Df - 실데이터 가져오기
    df1 = dfc.drop_rows(df) # 중장년 1차 필터링(사람인) (경력, 신입제외)
    dc.DFappendDB(df1, 'z_api_saramin_b_filter') # DB setup z_api_saramin_b_filter
    craw.startCrawl()
    # df1 = dfc.getDBmakeDF("SELECT * FROM z_api_saramin_b_filter limit 40;") # 테스트용
    # dc.DFappendDB(df1, 'z_api_saramin_crawl') # DB setup z_api_saramin_crawl
    pass

def jobkorea():
    import requests
    from bs4 import BeautifulSoup as bs
    import xml.etree.ElementTree as ET
    import pandas as pd
    rbcd = ['cbo','cco','cdo','ceo','cfo','cho','cio','cko','cmo','coo','cro','cso','cto','pm','pl','director','Supervisor','Clerk','analyst','editor','designer','illustrator','database','developer','agent','chef','engineer','guide','research']
    rpcd = []
    # for n in range(10001, 10026):
    #     rbcd.append(n)
    # for n in range(1000001, 1000184):
    #     rpcd.append(n)
    GN = []
    GPN = []
    df = pd.DataFrame()
    for bcd in rbcd:
        code = 'keyword=' + bcd
        for i in range(1, 6):
            pageNo = i
            URL = 'http://www.jobkorea.co.kr/Service_JK/Data/JK_GI_XML_List.asp?' + code + '&api=483&page=' + str(pageNo)
            header = {'Accept': 'application/xml; charset=utf-8',
                'referer': 'http://www.jobkorea.co.kr/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
            req = requests.get(URL, headers=header)
            root = ET.fromstring(req.text)
            GI_No = root.findall('./Items/GI_No')
            GI_Part_No = root.findall('./Items/GI_Part_No')
            for gn in GI_No:
                # print(gn.text)
                GN.append(gn.text)
            for gpn in GI_Part_No:
                # print(gpn.text)
                GPN.append(gpn.text)

    df['GI_No'] = GN
    df['GI_Part_No'] = GPN
    # print(df)
    print(df.value_counts(sort=True, ascending=False))


    pass

if __name__ == "__main__":
    saramin()
    # jobkorea()

# df = getApi(saramin())
# df_f = firstFilter(df)
# df_c = crawling(df_f)

