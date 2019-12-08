import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.bootstrap import config
from api.router import user, device, auth, rule, message

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.DEBUG)

app = FastAPI(title="RIOT api")
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

app.include_router(
    auth.router,
    prefix="/token",
    tags=["auth"],

)

app.include_router(
    rule.router,
    prefix="/device",
    tags=["rule"]
)

app.include_router(
    message.router,
    prefix="/device",
    tags=["message"]
)

if __name__ == "__main__":
    uvicorn.run(app, host=config.server.host, port=config.server.port)
