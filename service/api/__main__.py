import logging
import sys
from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.bootstrap import config, db_engine
from api.cli import create_user_cli
from api.router import user, device, auth, rule, message
from core.bootstrap import migrate

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", level=logging.INFO)

if __name__ == "__main__":
    parser = ArgumentParser(description='rIOT api cli.')
    parser.add_argument("-u", "--create-user", action="store_true")
    args = parser.parse_args()
    migrate(db_engine)

    if args.create_user:
        create_user_cli()
        sys.exit(0)

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
        tags=["rule"]
    )

    app.include_router(
        message.router,
        prefix="/device",
        tags=["message"]
    )
    uvicorn.run(app, host=config.server.host, port=config.server.port)
