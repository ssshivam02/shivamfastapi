from tkinter import CASCADE
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer,String, Boolean, nullslast
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
#database migration we use 

class Post(Base):
    __tablename__= "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable= False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    #this will make automatically relationship between posts and users
    owner=relationship("User")
class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable= False,server_default=text('now()'))

#post and user are interrealted
#one to many relationship one user can create many post
#fk is userid of User Table
#we need to delete table first if we wnt to update any new column or anything 
#because if table preexit then sqlachmey will not create new table or not update old table
