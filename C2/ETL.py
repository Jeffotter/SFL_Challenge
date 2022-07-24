import pandas as pd
import numpy as np
import time
import psycopg2
from sqlalchemy import create_engine
from user_definition import *


print('Connecting to db')

def execute_commit(cur,conn,query):
    """ Executes the querys in psycopg2 """
    cur.execute(query)
    conn.commit()
    
conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
conn=psycopg2.connect(host=host,port=port,database=database, user=user,password=password)
cur=conn.cursor()
db=create_engine(conn_string)
query='''DROP TABLE IF EXISTS "Transformed" CASCADE;'''
execute_commit(cur,conn,query)


df=pd.read_csv('DATA.csv')
print('Data Loaded')
df[['user_name','email_service']]=df['email'].str.split('@',expand=True)
dummy_var=pd.get_dummies(df['gender'])
df1=pd.concat([df,dummy_var],axis=1)
#df2=df1['ip_address'].apply(find_loc)
#df_final=pd.DataFrame.from_dict(df2)
#final=pd.json_normalize(df_final['ip_address'])
#df1=pd.concat([df1,final],axis=1)
#df1.drop(columns=['bogon'])
df1.to_sql('Transformed', db)

cur.close()
conn.close()