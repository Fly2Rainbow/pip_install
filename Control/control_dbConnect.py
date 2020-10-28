import mysql.connector	
import pymysql
from sqlalchemy import create_engine
import Utils as log

logger = log.CreateLogger('Saramin_Crawling')
 	
# mysql connection을 선언한다. 파라미터는 host는 접속 주소, user는 ID, passwd는 패스워드, database는 접속할 데이터 베이스이다.	
dbconn = mysql.connector.connect(host="workwiz.cafe24.com", port='3306', user="workwiz", passwd="qwe123!@3", database="workwiz")	
 	
# 검색을 할 경우 사용되는 함수.	
def select(query, bufferd=True):	
  global dbconn
  cursor = dbconn.cursor(dictionary=True, buffered=bufferd)
  cursor.execute(query.encode('utf8'))
  # cursor.fetchall()   #로 결과를 리스트로 내보낼 수도 있다. 	
  # 그러나 결과가 대용량일 경우 fetchall로 대량의 값을 메모리에 넣으면 느려질 수 있다.	
  return cursor
 	
# DML(Data Manipulation Language)의 insert, update, delete를 처리하는 함수	
def merge(query, values, bufferd=True):	
  global dbconn
  try:	
    cursor = dbconn.cursor(buffered=bufferd)
    cursor.execute(query, values)	
    dbconn.commit()	
  except Exception as e:	
    dbconn.rollback()	
    raise e	
 	
# DML(Data Manipulation Language)의 insert, update, delete를 대랑 처리하는 함수	
def merge_bulk(query, values, bufferd=True):	
  global dbconn	
  try:	
    cursor = dbconn.cursor(buffered=bufferd)	
    cursor.executemany(query, values)	
    #dbconn.commit()	
  except Exception as e:	
    dbconn.rollback()	
    raise e	
 	
# DML이외의 쿼리를 실행하는 함수.	
def execute(query, bufferd=True):	
  global dbconn	
  try:	
    cursor = dbconn.cursor(buffered=bufferd)	
    cursor.execute(query)	
    #dbconn.commit()	
  except Exception as e:	
    dbconn.rollback()	
    raise e	


def setDFtoDB(df): # insert to DB (first API response DF) original Data
    print('START::setDftoDB()')
    result = 1
    df_headers = df.columns
    db_headers = select("SELECT * FROM z_api_saramin_all LIMIT 0").column_names
    df.columns = db_headers[:len(df_headers)]
    
    execute('TRUNCATE z_api_saramin_all')
    dbconn.commit()
    dbconn.close()
    pymysql.install_as_MySQLdb()
    engine = create_engine('mysql://workwiz:qwe123!@3@workwiz.cafe24.com/workwiz')
    conn = engine.connect()
    try:
        df.to_sql(name='z_api_saramin_all', con=engine, if_exists='append', index=False)
        #df.to_sql(name='z_api_saramin', con=engine, if_exists='replace')
        print('**'*60)
    except Exception as e:
        logger.error(f'setDFtoDB(df) Error:: [Saramin]DF Not into DB [error={e}]')
        print(f'df into db Error:::{e}')
        result = 0
    finally:
        conn.close()
        
    return df, result


def DFappendDB(df, table): # df to DB what do you want Table
    print('START::DFappendDB()')
    result = 1
    execute('TRUNCATE ' + table)
    dbconn.commit()
    dbconn.close()
    pymysql.install_as_MySQLdb()
    engine = create_engine('mysql://workwiz:qwe123!@3@workwiz.cafe24.com/workwiz')
    conn = engine.connect()
    try:
        df.to_sql(name=table, con=engine, if_exists='append', index=False)
        #df.to_sql(name='z_api_saramin', con=engine, if_exists='replace')
        print('**'*60)
    except Exception as e:
        logger.error(f'DFappendDB(df, table) Error:: [Saramin]DF Not into DB [error={e}]')
        print(f'df append db Error:::{e}')
        result = 0
    finally:
        conn.close()
        
    return df, result


def getDBdata(query):
    import pandas as pd
    import mysql.connector
    from datetime import datetime
    import json
    query_result = []
    try:
        # DB Connection
        conn = mysql.connector.connect(
              host='workwiz.cafe24.com', 
              user='workwiz', 
              passwd='qwe123!@3', 
              port='3306', 
              database='workwiz', 
              charset='utf8mb4', autocommit=True)

        # Get a DB : select Data
        cursor = conn.cursor(dictionary=True) 
        # 쿼리를 실행할시에 query string을 'utf8'로 encode # cursor.execute(query)
        cursor.execute(query.encode('utf8'))
        query_result = cursor.fetchall()
        # query_result1 = json.dumps(query_result)
        # print(query_result)
    except Exception as e:
        logger.error(f'getDBdata(query) Error:: [Saramin]DB get error [error={e}]')
        print(e)
    finally:
        # Close connection
        conn.close()

    return query_result

def Cafe24Connector():  # 카페24 connector with auto_commit
    import pandas as pd
    import mysql.connector
    try:
        # DB Connection
        conn = mysql.connector.connect(
              host='workwiz.cafe24.com', 
              user='workwiz', 
              passwd='qwe123!@3', 
              port='3306', 
              database='workwiz', 
              charset='utf8mb4', autocommit=True)
        # Get a DB : select Data
        # cursor = conn.cursor(dictionary=True) 
    except Exception as e:
        logger.error(f'Cafe24Connection Error:: [Saramin] [error={e}]')
        conn.close()
    return conn

def selectDBdata(conn, query):
  cursor = conn.cursor(dictionary=True) 
  cursor.execute(query.encode('utf8'))
  query_result = cursor.fetchall()

  return query_result