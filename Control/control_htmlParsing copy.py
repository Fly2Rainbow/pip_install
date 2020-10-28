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
PREFIX = "<!doctype html><html lang='ko'><head><meta charset='utf-8'>" +\
            "<title>채용공고 상세</title>" +\
            "<base target='_blank'>" +\
            "<meta name='robots' content='noindex,nofollow'>" +\
            "<link href='https://www.saramin.co.kr/sri_css/recruit-template-reset.css' media='all' rel='stylesheet' type='text/css'>" +\
            "<link href='https://www.saramin.co.kr/sri_css/recruit-template.css' media='all' rel='stylesheet' type='text/css'>" +\
            "</head>" +\
            "<body style='margin:0 !important;padding:0 !important;background:#fff !important;'>"
POST = '</body></html>'
columns = ['crawlSummary1', 'crawlSummary2', 'crawlDetail',
            'crawlDeadline', 'crawlCompany', 'crawlCompanyLogo',
            'crawlSummary', 'iframe']
classNames = ['wrap_jv_header', 'jv_cont jv_summary', 'jv_cont jv_detail',
                'jv_cont jv_howto', 'jv_cont jv_company', 'logo']

def getDF():
    query = "SELECT * FROM z_api_saramin_b_filter limit 5;"
    df_org = dfc.getDBmakeDF(query)

    return df_org

        # log.RemoveFile('C:/PhythonWorkspace/logs/Saramin_Crawling.log')

def startCrawl(df_org):
    print(f'Start::Crawling_sri')
    # getDF()
    df_org[['crawlSummary1', 'crawlSummary2']] = ''
    print(f'Start Time::: {datetime.datetime.now()}')
    logger.info(f'StartTime Crawling:: [Saramin] "{datetime.datetime.now()}"')
    df_crawl = crawlingData(df_org)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
    #     print(df_crawl)
    df_crawl = df_crawl.drop(['crawlSummary1', 'crawlSummary2'], axis=1)
    dc.DFappendDB(df_crawl, 'z_api_saramin_crawl')
    print(f'End Time::: {datetime.datetime.now()}')
    logger.info(f'EndTime Crawling:: [Saramin] "{datetime.datetime.now()}"')
    pass


def modifyURL(df):
    urls = df.url.str.split("&").str[0].str.replace('relay/', '')
    # print(urls[0])
    return urls

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

# def proxy_generator():
    # response = requests.get("https://sslproxies.org/")
    # soup = bs(response.content, 'html5lib')
    # proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1]+' - '+x[2], list(zip(map(lambda x:x.text, 
    #    soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]), map(lambda x:x.text, soup.findAll('td')[3::8]))))))}
    # print(soup.findAll('td')[3::8])
    # return proxy


def crawlingData(df_org):
    urls = modifyURL(df_org)
    # print(len(urls))
    headers = getHeaders()
    rows = 0
    proxyList = readProxyFile()
    i = 0
    j = 0
    k = 0
    cycle = 20
    check = True
    err = True
    while check:
        cycle = cycle * (k+1)
        # print(f'cycle = {cycle}')
        while err:
            # print(f'j(no in urls) = {j}')
            # print(f'k(cycle count) = {k}')
            if j > cycle-1:
                err = False
                cycle = cycle / (k+1)
                # print(f'reset cycle = {cycle}')
                break
            if j == len(urls):
                check = False
                break
            # print(f'i(no in proxy) = {i}')
            proxy = proxyList[i]
            print(f'i = [{i}], proxy = [{proxyList[i]}]')
            try:
                print(f'url = [{urls[j]}]')
                # doc = requests.get(urls[j], headers=headers)
                doc = requests.get(urls[j], headers=headers, proxies={"http": proxy, "https": proxy})
            except Exception as e:
                logger.error(f'Proxy Error:: [Saramin]Proxy has some Problem! "{proxy}" [error={e}]')
                i +=1
                continue
            bs = BeautifulSoup(doc.content,"html.parser")

            newDFColumn(rows, urls[j], bs, classNames, df_org)
            rows += 1
            
            with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
                df_org.update(df_org['iframe'].astype(str).str.replace('\n', ''))
                df_org.update(df_org['iframe'].astype(str).str.replace('\r', ''))
                # for c in range(len(columns)):
                    # print(df_temp.iloc[:, c])
            j += 1

        i += 1
        k += 1
        err = True
        if i == len(proxyList) - 1:
            print(f'proxy all used:: Recycled')
            i = 0
    
    
    
    return df_org


def newDFColumn(rows, url, bs, classNames, df_org):
    i = 0
    for i in range(len(classNames)):
        # print(classNames[i])
        if bs.find('div', class_=classNames[i]):  # crawlDeadline jv_cont jv_howto
            soup = bs.find('div', class_=classNames[i])
            if classNames[i] == 'logo':
                logoUrl = soup.img['src']
                df_org.loc[rows, columns[i]] = logoUrl
                continue
            elif classNames[i] == 'sri_btn_expired_apply':
                df_org.loc[rows, 'active'] = str(0)
            else:
                innerText = dfc.JoinInnerTexts(soup)
                if classNames[i] == 'jv_cont jv_detail':
                    df_org.loc[rows, 'iframe'] = PREFIX + str(soup) + POST
                    # print(df_org.loc[rows, 'iframe'])
            df_org.loc[rows, columns[i]] = innerText
        else:
            logger.error(f'Parsing Error:: [Saramin]Tag not Exist! "{classNames[i]}" [url={url}]')
            # print('\033[31m \033[43m' + f'ERROR URL ::: {url} [접수기간및방법]' + '\033[0m') # 에러 발생시 색상 변경 강조
        if bs.find('span', class_='sri_btn_expired_apply'):
            df_org.loc[rows, 'active'] = str(0)
    df_org.loc[rows, 'crawlSummary'] = df_org.loc[rows, 'crawlSummary1'] + df_org.loc[rows, 'crawlSummary2']
    
    pass





