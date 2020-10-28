#import mysql.connector
import xmltodict
import json
import pandas as pd
from pandas import json_normalize
from pandas import ExcelWriter
import xml.etree.ElementTree as ET
import os
import os.path, sys
sys.path.append('C:\\PythonWorkspace\\Workwiz\\Control')
import numpy as np
import datetime as dt
import control_etc as etc
import control_dbConnect as dc
import Utils as log

logger = log.CreateLogger('Saramin_Crawling')

def make_dataframe(roots):
    print('START::make_dataframe()')
    dfs = []
    # print('make_dataframe::roots::: ', roots)
    i = 1
    for root in roots:
        root = ET.tostring(root, encoding='UTF-8', method='xml')
        data_dict = xmltodict.parse(root)
        json_data = json.dumps(data_dict)
        try:
            sta = json.loads(json_data)['job-search']['jobs']['job']
        except Exception as e:
            logger.error(f'XML Data Error:: [Saramin]XML->Json "{json_data}" [error={e}]')
            print('@'*60)
            print(i)
            print(json_data)
            print(e)
            print('@'*60)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):
            dfi = json_normalize(sta)
           #print(dfi)
            print(f'make_dataframe::dfi-{i}::count::: {len(dfi.index)}')
            dfs.append(dfi)
            # print('make_dataframe::dfs::: ', dfs[i-1].iloc [0:2, :])
            i += 1
    
    if len(dfs) == 1:
        df = dfs[0] 
        print('dfs has Only one df List')
    else:
        print('make_dataframe::len(dfs)::: ', len(dfs))
        try:
            df = dfs[0].append([pd.DataFrame(dfs[i])  for i in range(1 , len(dfs))], ignore_index=True)
            print(f'dataframe::df_rowcount::: {len(df.index)}')
            pd.DataFrame(df)
            # print(f'dupleData::: {data[df.duplicated()]}')
            df = df.drop_duplicates(["id"], keep='last')
            print(f'Post dropDuple::df_rowcount::: {len(df.index)}')
            setUpColumns(df)
            saveXlsx(df)
            print('END')
        except ValueError as e:
            logger.error(f'DF control Error:: [Saramin]DF value Error "-" [error={e}]')
            print('ValueError :: ', e)
            pass
        
    
    return df


def setUpColumns(df):
    print('START::setUpColumns()')
    print(df.columns)
    df.update('S' + df['id'].astype(str))
    df.rename(columns={'company.name.@href':'H'}, inplace=True)
    if 'company.name' in df:
        print('Column-company.name::\n', df['company.name'].dropna())
        df['company.name.#text'] = np.where((df['company.name.#text'].isna()), df['company.name'], df['company.name.#text'])
        del df['company.name']
    if 'position.location' in df:
        print('Column-position.location::\n', df['position.location'].dropna())
        del df['position.location']
    if 'position.job-type' in df:
        print('Column-position.job-type::\n', df['position.job-type'].dropna())
        del df['position.job-type']
    if 'position.industry' in df:
        print('Column-position.industry::\n', df['position.industry'].dropna())
        del df['position.industry']
    if 'position.job-category' in df:
        print('Column-position.job-category::\n', df['position.job-category'].dropna())
        del df['position.job-category']
    if 'position.required-education-level' in df:
        print('Column-position.required-education-level::\n', df['position.required-education-level'].dropna())
        del df['position.required-education-level']
    
    df['bizNum'] = df.H.str.split("csn=").str[1].str.split("&").str[0]
    # print(df.columns)
    df.update(df['posting-timestamp'].apply(etc.timestamp2datetime))
    df.update(df['modification-timestamp'].apply(etc.timestamp2datetime))
    df.update(df['opening-timestamp'].apply(etc.timestamp2datetime))
    df.update(df['expiration-timestamp'].apply(etc.timestamp2datetime))
    df.reset_index(drop=True, inplace=True)
    df.sort_values(by='id', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    today = (dt.datetime.today() + pd.DateOffset(days=-1)).date()
    df1 = df.copy()
    df1['posting-timestamp'] = df1.apply(lambda x: dt.datetime.strptime(x['posting-timestamp'], '%Y-%m-%d %H:%M:%S'), axis=1)
    df1['posting-timestamp'] = df1.apply(lambda x: x['posting-timestamp'].date(), axis=1)
    # print(df1['posting-timestamp'])
    df1['getDate'] = np.where(df1['posting-timestamp'] == today, today + pd.DateOffset(days=1), df1['posting-timestamp'].astype(str))
    df['getDate'] = df1['getDate']
    df['getDate'] = pd.to_datetime(df['getDate'])
    # print(df.dtypes)
    # df = df.apply(lambda col: col.astype(str) if col.dtype == 'datetime64[ns]' else col)
    # print(df.iloc [980:990, :])
    pass


def drop_rows(df):
    idx = df[(df['experience-level_code'].astype(int) == 1) | 
        (((df['min'].astype(int) < 10) & (df['min'].astype(int) > 0)) & (df['max'].astype(int) < 10))].index
    df1 = df.drop(idx)
    # print(df1)
    return df1

def saveXlsx(df):
    base_dir = "C:/Users/user/Documents"
    file_nm = "df.xlsx"
    xlxs_dir = os.path.join(base_dir, file_nm)
    df.to_excel(xlxs_dir, # directory and file name to write
            sheet_name = 'Sheet1', 
            # na_rep = 'NaN', 
            # float_format = "%.2f", 
            # header = True, 
            # #columns = ["group", "value_1", "value_2"], # if header is False
            # index_label = "id", 
            # startrow = 1, 
            # startcol = 1, 
            # #engine = 'xlsxwriter', 
            # freeze_panes = (2, 0)
            ) 
    pass

def DBdataToDataFrame(queryResult):
    df = pd.DataFrame(queryResult)
    return df


def getDBmakeDF(query):
    queryResult = dc.getDBdata(query)
    df = DBdataToDataFrame(queryResult)
    return df


def JoinInnerTexts(soup):
    soups = soup.stripped_strings
    innerTexts = ''
    for text in soups:
            innerTexts = innerTexts + text + ' | '
    return innerTexts


def setSaraminCols():
    df = getDBmakeDF("SELECT * FROM api_saramin_1todayGet;")
    # print(df.columns)
    # print('*'*60)
    mid = df['industry-keyword-code']
    df.drop(labels=['industry-keyword-code'], axis=1, inplace = True)
    df.insert(26, 'industry-keyword-code', mid)
    mid = df['job-category-keyword-code']
    df.drop(labels=['job-category-keyword-code'], axis=1, inplace = True)
    df.insert(26, 'job-category-keyword-code', mid)
    dc.setDFtoDB(df)
    # print(df.columns)
    return df