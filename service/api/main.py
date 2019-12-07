import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.bootstrap import config
from api.router import user, device

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)
app.include_router(
    device.router,
    prefix="/device",
    tags=["device"],
)
if __name__ == "__main__":
    uvicorn.run(app, host=config.server.host, port=config.server.port)
