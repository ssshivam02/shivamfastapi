from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
import psycopg2
import time
from psycopg2.extras import RealDictCursor   #this is for pgadmin
from .config import setting 
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:%s@{setting.database_hostname}:{setting.database_port}/{setting.database_name}' % quote(f'{setting.database_password}')

# engine for creating local postgres connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

def get_db():
    '''
    create session: creating session locally
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
#for direct running raw sql
while True:
    try:
        #this hard code password and host name
        conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',
        password='Shivam@1998',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error: ",error)
        time.sleep(2)
        #every two sec this will run again

'''