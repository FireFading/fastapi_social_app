import stackprinter
import uvicorn
from app.routers.chats import router as chats_router
from app.routers.users import router as users_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

stackprinter.set_excepthook()

app = FastAPI()

add_pagination(app)
app.include_router(users_router)
app.include_router(chats_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
