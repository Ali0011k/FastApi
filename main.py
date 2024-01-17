from fastapi import FastAPI
from databases.sqlite import Base, engine
from views import get
from views import post
from views import put
from views import patch
from views import delete
from views import jwt
from views import database

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(get.router, tags=["get requests"])
app.include_router(post.router, tags=["post requests"])
app.include_router(put.router, tags=["put requests"])
app.include_router(patch.router, tags=["patch requests"])
app.include_router(delete.router, tags=["delete requests"])
app.include_router(database.router, tags=["database"])
app.include_router(jwt.router, tags=["jwt"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
