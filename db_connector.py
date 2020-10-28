	
import mysql.connector	

dbconn = mysql.connector.connect(host="workwiz.cafe24.com", user="workwiz", passwd="qwe123!@3", database="workwiz")	# real DB
#dbconn = mysql.connector.connect(host="localhost", user="root", passwd="youmin0915", database="testdb") # local

class MydbConnector: 	
  
  def select(self, query, bufferd=True):	
    global dbconn
    cursor = dbconn.cursor(buffered=bufferd)
    cursor.execute(query)
    return cursor
    
  # DML(Data Manipulation Language)의 insert, update, delete를 처리하는 함수	
  def dmlSql(self, query, values, bufferd=True):	
    global dbconn
    try:	
      cursor = dbconn.cursor(buffered=bufferd)
      cursor.execute(query, values)	
      dbconn.commit()	
    except Exception as e:	
      # 에러가 발생하면 쿼리를 롤백한다.	
      dbconn.rollback()	
      raise e	
    
  # DML(Data Manipulation Language)의 insert, update, delete를 대랑 처리하는 함수	
  def dmlSql_bulk(self, query, values, bufferd=True):	
    global dbconn	
    try:	
      cursor = dbconn.cursor(buffered=bufferd)	
      cursor.executemany(query, values)	
      dbconn.commit()	
    except Exception as e:	
      dbconn.rollback()	
      raise e	
    
  # DML이외의 쿼리를 실행하는 함수.	
  def execute(self, query, bufferd=True):	
    global dbconn	
    try:	
      cursor = dbconn.cursor(buffered=bufferd)	
      cursor.execute(query)	
      dbconn.commit()
    except Exception as e:
      #myconn.execute("DROP TABLE PythonTable")	
      dbconn.rollback()	
      raise e	
 	
myconn = MydbConnector()

try:	

  myconn.execute("""	
    CREATE TABLE PythonTable (	
    idx int auto_increment primary key,	
    data1 varchar(255),	
    data2 varchar(255)	
    )	
    """)	

  values = [('data1', 'test1'),	
            ('data2', 'test2'),	
            ('data3', 'test3'),	
            ('data4', 'test4'),	
            ('data5', 'test5')]	
  
  myconn.dmlSql_bulk("INSERT INTO PythonTable (data1, data2) VALUES (%s, %s)", values)	
  
  for row in myconn.select("SELECT * FROM PythonTable"):	
    print(row)	
  
  myconn.dmlSql("UPDATE PythonTable set data2=%s where data1=%s", ('update1','data1'))	
  
  for row in myconn.select("SELECT * FROM PythonTable"):	
    print(row)	

  #myconn.execute("DROP TABLE PythonTable")

except Exception as e:	
  print(e)	

finally:	
  dbconn.close()