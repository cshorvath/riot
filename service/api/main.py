import uvicorn
from fastapi import FastAPI

from core.util import parse_config_from_env

app = FastAPI()
config = parse_config_from_env("RIOT_API_CONFIG_FILE")

if __name__ == "__main__":
    uvicorn.run(app, host=config.server.host, port=config.server.port)
