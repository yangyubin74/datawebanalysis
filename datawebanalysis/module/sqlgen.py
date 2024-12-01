import sqlite3
import pandas as pd


database_name="D:\\work\\yubin_data.db"
#데이터베이스 Connection
def connection_cursor():
    connection = sqlite3.connect(database_name)   
    cursor = connection.cursor()
    return connection,cursor

#DB 생성
def create_db():

    connection,cursor=connection_cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS data (
        bld_name TEXT,
        flr_name TEXT,
        whole_no_name TEXT,
        whole_code TEXT,
        whole_name TEXT,
        org_nm TEXT,
        union_uid TEXT,
        order_dt TEXT,
        buy_amt REAL,
        return_yn TEXT,
        refund_yn TEXT,
        last_appr_status TEXT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

#DB 입력
def insert_db(df):
    connection, cursor = connection_cursor()
    insert_query = """
    INSERT INTO data (bld_name, flr_name, whole_no_name, whole_code, whole_name,
                      org_nm, union_uid, order_dt, buy_amt, return_yn, refund_yn, last_appr_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    df = df.drop(columns='z_score')
    data = df.values.tolist()
    cursor.executemany(insert_query, data)
    connection.commit()
    connection.close()

#플랫폼 가입자와 비가입자 조회
def select_org_member():
     connection, cursor = connection_cursor()
     select_query = """
       select whole_name,org_nm  from data
     """
     cursor.execute(select_query)
     rows = cursor.fetchall()
     return rows

def select_build_member():
     connection, cursor = connection_cursor()
     select_query = """
       select bld_name,whole_name  from data  group by bld_name,whole_name, org_nm 
     """
     cursor.execute(select_query)
     rows = cursor.fetchall()
     
     return rows