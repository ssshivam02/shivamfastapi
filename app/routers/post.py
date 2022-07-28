from fastapi import Depends,Response,status,HTTPException,APIRouter
from .. import models,schemas,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
router = APIRouter(
    prefix="/posts",tags=['POST']
)

#by using orm
#in get we get list in return so we need List[]
@router.get("/",response_model=List[schemas.Post])        #int is not imp we can add anything here #limit 10 is default
def get_posts(db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]= ""):
    #this will make private as per owner_id
    #post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #for accessing limit in url we need to add posts?limit=3 or for default we use posts? only
    #for adding skip in our url we need to add posts?limit=3&skip=0
    #for seraching url posts?limit=3&skip=3&search=king
    #for seraching url posts?limit=3&skip=3&search=king%is%best % for spaces between word
    post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return post
    #we can remove "data"
    #return post.


#by sql
'''
@app.get("/posts",status_code=status.HTTP_202_ACCEPTED)
def get_posts():
    cursor.execute("""select * from posts""")
    my_post= cursor.fetchall()
    print(my_post)
    return {"data": my_post}
'''

#by using orm #use of response_model is imp
@router.post("/create",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def post_create(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #print(post.dict())
    #if we have many column then we can use **post.dict() this will unpack automatically
    #new_post=models.Post(title=post.title,content= post.content, published= post.published)
    #add then commiting
    #print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    # refresh as like returning *
    db.refresh(new_post)
    return new_post

#bysql
'''
@app.post("/",status_code=status.HTTP_201_CREATED)
def post_create(post:schemas.Post):
    print(post)                                     #%s we using to protecting our code from sql injection %s as like variable
    cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # post_dict=post.dict()
    #new_post currently a pydantic model if we want to change this dict
    #print(post.dict())
    conn.commit()
    new_post=cursor.fetchone()
    return {"new post": new_post}
'''
'''
def find_post(id:int):
    for p in my_posts:
        if p["id"]==int(id):
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i
'''
#validation also possible by add int and str in argument in func
'''
@app.get("/{id}")
def get_post_id(id:int,response: Response):    # :int is checking type of id
    post=find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND 
        return {'message':f"post with  id: {id} was not found"}
    return {"post_details": post}
'''
#by using orm
@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    #print(post) this will work after removing .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    #by applying this two line our get method become private
    #if post.owner_id!=current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    return post


#better way of doing not found id by using httpexception
#by sql

'''
@app.get("/{id}")
def get_post(id:int):
    cursor.execute("""select *from posts where id = %s""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return {"post_details": post}
'''
#by using orm
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT )


#by using sql
#delete
'''
@app.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # find the index in the array that has required id
    #my_posts.pop(index)
    cursor.execute("""delete from posts where id =%s returning * """,(str(id)))
    post=cursor.fetchone()
    conn.commit()
    #index= find_index_post(id)
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT )
'''
#by using orm

@router.put("/{id}")
def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #index= find_index_post(id)
    #print(type(current_user))
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    #we can do updatation in one like also
    #db.query(models.Post).filter(models.Post.id==id).update(post.dict(),syncsynchronize_session=False)
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

#by using sql
#update
'''
@app.put("/{id}")
def update_post(id: int,post: schemas.Post):
    #index= find_index_post(id)
    cursor.execute(""" update posts set title =%s, content=%s,published =%s where id=%s returning * """,
    (post.title,post.content,post.published,str(id)))
    post= cursor.fetchone()
    conn.commit()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return {'message':post}
'''
