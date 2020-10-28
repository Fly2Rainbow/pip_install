# import mysql.connector
 
# conn = mysql.connector.connect(host="localhost", user="root", passwd="youmin0915", database="testdb")
 
# curs = conn.cursor()
# sql = """insert into apitest(data1,data2)
#          values (%s, %s)"""
# curs.execute(sql, ('홍길동1', '서울1'))
# re = curs.execute(sql, ('이연수1', '서울1'))
# print(re)
# conn.commit()
 
# conn.close()

#import mysql.connector
import db_connector

dc = db_connector
mydc = dc.MydbConnector()

def dclExecute(query):
    try:
        mydc.execute(query)
    except Exception as e:	
        print(e)
    finally:
        dc.dbconn.close()

schemalist = ['dt1', 'dt2', 'dt3']
re = [sl + ' varchar(255)' for sl in schemalist]

print(re)

query_create = """CREATE TABLE PythonTable1 
    (idx int auto_increment primary key, 
    data1 varchar(255), 
    data2 varchar(255))
    """

query_drop = ("DROP TABLE PythonTable1")

query_select = ("select data1 from apitest")
query_select1 = ("select data3 from apitest")

#mydc.select(query_drop)
result = mydc.select(query_select).fetchall()
result1 = mydc.select(query_select1).fetchall()

import pandas as pd
pdres = pd.DataFrame(result)
print(pdres)

#final_result = [list(i) for i in result]  # result = (1,2,3,) or  result =((1,3),(4,5),)
final_result = [i[0] for i in result] # result = (1,2,3,)
final_result1 = [i[0] for i in result1] # result = (1,2,3,)
print(final_result)
print(final_result1)



temp3 = list(set(final_result) - set(final_result1)) #순서 보존이 안됨
print(temp3)
#또는
s = set(final_result1)
print(s)
temp3 = [x for x in set(final_result)if x not in s] #순서 보존됨
temp3 = [x for x in final_result if x in s] #순서 보존됨
print(temp3)