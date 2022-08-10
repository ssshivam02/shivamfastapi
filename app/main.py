from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, misc, vote

#this like help in createtable when we save first our code but after use of alembic in code we dont need this
#models.Base.metadata.create_all(bind=engine)
origins=["https://www.google.com"] #this contain list of domain

app = FastAPI()
app.add_middleware(CORSMiddleware,
allow_origins=origins,  #for public use ["*"]
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"]
)
                
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(misc.router)
app.include_router(vote.router)

