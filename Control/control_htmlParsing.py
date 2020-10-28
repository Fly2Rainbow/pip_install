import control_api_request as apic
import control_dataframe as dfc
import control_dbConnect as dc
import control_etc as etc
import Utils as log
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pprint
import datetime 
# date = datetime.datetime.now() 
pp = pprint.PrettyPrinter(indent=4)


logger = log.CreateLogger('Saramin_Crawling')
px = [
    "<!doctype html><html lang='ko'><head><meta charset='utf-8'>",
    "<title>채용공고 상세</title>",
    "<base target='_blank'>",
    "<meta name='robots' content='noindex,nofollow'>",
    "<link href='https://www.saramin.co.kr/sri_css/recruit-template-reset.css' media='all' rel='stylesheet' type='text/css'>",
    "<link href='https://www.saramin.co.kr/sri_css/recruit-template.css' media='all' rel='stylesheet' type='text/css'>",
    "</head>",
    "<body style='margin:0 !important;padding:0 !important;background:#fff !important;'>"
]
PREFIX = log.longString(px)
POST = '</body></html>'
columns = ['crawlSummary1', 'crawlSummary2', 'crawlDetail',
            'crawlDeadline', 'crawlCompany', 'crawlCompanyLogo',
            'crawlSummary', 'iframe']
classNames = ['sri_btn_expired_apply', 'wrap_jv_header', 'jv_cont jv_summary', 'jv_cont jv_detail',
                'jv_cont jv_howto', 'jv_cont jv_company', 'logo']
FILTER = ["중년", "장년", "시니어", "부장", "감사", "이사", "상무", "전무", "부사장", "임원", "사장", "대표이사"
        "선임연구원", "책임연구원", "수석연구원", "연구소장", "팀장", "실장", "총무", "지사장", "지점장", 
        "파트장", "그룹장", "센터장", "매니저", "본부장", "사업부장", "원장", "국장", "사무국장", "사무장", 
        "총괄관리", "현장소장", "반장", "단장",
		"cbo","cco","cdo","ceo","cfo","cho","cio","cko","cmo","coo","cro","cso","cto","pm","pl",
        "director","Supervisor","Clerk","analyst","editor","designer","illustrator","database",
        "developer","agent","chef","engineer","guide","research"]

# log.RemoveFile('C:/PhythonWorkspace/logs/Saramin_Crawling.log')

def startCrawl():
    import json

    # print(f'Start::Crawling_sri')
    sTime = datetime.datetime.now()
    logger.info(f'StartTime Crawling:: [Saramin] "{sTime}"')

    # query = 'SELECT z.id, z.url, z.keyword, z.title from z_api_saramin_b_filter AS z WHERE z.id = "S37953353";'
    query = 'SELECT z.id, z.url, z.keyword, z.title from z_api_saramin_b_filter AS z;'
    conn = dc.Cafe24Connector()
    query_result = dc.selectDBdata(conn, query)
    # conn.close()

    strJson = json.dumps(query_result, indent = 4) # query result to json(type:str)
    listJson = json.loads(strJson) #convert str to list
    proxyList = readProxyFile()

    cycle = 20 # Proxy recycling fact
    c = cycle # default fact
    p = 0 # Proxy count
    for i in range(len(listJson)):
        # print(f'i = {i}  c = {c}')
        # print(f'cycle = {cycle}')
        if i > cycle - 1:
            cycle += c
            p += 1
        # print(f'ID = {ID}')
        # print(f'URL = {URL}')
        if p == len(proxyList):
            # print(f'proxy all used:: Recycled')
            p = 0
        print(f'rowsCnt = {i+1} | p = [{p}], proxy = [{proxyList[p]}]')
        ID = listJson[i]['id']
        URL = str(listJson[i]['url']).split("&")[0].replace('relay/', '')
        KEYWORD = listJson[i]['keyword']
        TITLE = listJson[i]['title']
        print(URL)
        try:
            values = crawlingData(URL, proxyList[p], KEYWORD, TITLE)
        except Exception as e:
            logger.error(f'Crawling Error:: [Saramin] Time = "{datetime.datetime.now()}", ID = {ID}, URL = [{URL}], ErrMSG={e}')
            pass
        
        strings = ['UPDATE z_api_saramin_b_filter ', 
                    'SET crawlSummary = %s, crawlDetail = %s, crawlDeadline = %s, ',
                    'crawlCompany = %s, crawlCompanyLogo = %s, iframe = %s, active = %s, middleAge = %s, ',
                    'crawlExist = %s ',
                    'WHERE id = %s;']
        update_query = log.longString(strings)
        val = (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], ID)
        # print(val)
        # dc.merge(update_query, val)
        cursor = conn.cursor()
        cursor.execute(update_query, val)	
        conn.commit()	

    conn.close()
    eTime = datetime.datetime.now()
    logger.info(f'EndTime Crawling:: [Saramin] "{eTime}" (durTime = {eTime - sTime})')
    pass


def getHeaders():
    header = {'Accept': 'application/xml; charset=utf-8',
        'referer': 'https://www.saramin.co.kr/zf_user/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    return header


def readProxyFile():
    with open('G:\\내 드라이브\상상우리\\4. 온라인서비스\\41. 워크위즈팀\\41_B. 플랫폼 개발\\41_Bb.워크위즈개발(2020)\\프록시유동_모모아이피.txt', 'r') as file:
        lines = file.readlines()
        proxy = []
        for line in lines:
            proxy.append(line.rstrip('\n'))
    return proxy


def crawlingData(URL, proxy, KEYWORD, TITLE):
    headers = getHeaders()
    try:
        doc = requests.get(URL, headers=headers, proxies={"http": proxy, "https": proxy})
    except Exception as e:
        logger.error(f'Proxy Error:: [Saramin]Proxy has some Problem! "{proxy}" [error={e}]')
        pass
    bs = BeautifulSoup(doc.content,"html.parser")
    result = runCrawling(bs, URL, KEYWORD, TITLE)
    
    return result


def runCrawling(bs, URL, KEYWORD, TITLE):
    i = 0
    # global active
    crawlSummary1 = ''
    crawlSummary2 = ''
    crawlSummary = ''
    crawlDetail = ''
    crawlDeadline = ''
    crawlCompany = ''
    crawlCompanyLogo = ''
    iframe = ''
    active = str(1)
    middleAge = str(0)
    filterDB = []
    for i in range(len(classNames)):
        if bs.find('div', class_=classNames[i]):  # crawlDeadline jv_cont jv_howto
            soup = bs.find('div', class_=classNames[i])
            if classNames[i] == 'logo':
                crawlCompanyLogo = soup.img['src']
            elif classNames[i] == 'sri_btn_expired_apply':
                active = str(0)
            else:
                innerText = dfc.JoinInnerTexts(soup)
                if classNames[i] == 'jv_cont jv_detail':
                    iframe = (PREFIX + str(soup) + POST).replace('\n', '')
                    iframe = iframe.replace('\r', '')
                    crawlDetail = innerText
                elif classNames[i] == 'wrap_jv_header':
                    crawlSummary1 = innerText
                elif classNames[i] == 'jv_cont jv_summary':
                    crawlSummary2 = innerText
                elif classNames[i] == 'jv_cont jv_howto':
                    crawlDeadline = innerText
                elif classNames[i] == 'jv_cont jv_company':
                    crawlCompany = innerText
        # else:
        #     logger.error(f'Parsing Error:: [Saramin]Tag not Exist! "{classNames[i]}" [url={URL}]')
    
    str_list = [crawlSummary1, crawlSummary2]
    crawlSummary = log.longString(str_list)
    crawlExist = str(1)
    filterDB = [crawlSummary, crawlDetail, KEYWORD, TITLE]
    try:
        if any(f.lower() in db.lower() for f in FILTER for db in filterDB):
            middleAge = str(1)
    except Exception as e:
        logger.error(f'MiddleAge Filter Error:: [Saramin]Filterring Error! "{URL}" [error={e}]')

    result_crawl = [crawlSummary, crawlDetail, crawlDeadline, crawlCompany, crawlCompanyLogo, iframe, active, middleAge, crawlExist]
    return result_crawl





