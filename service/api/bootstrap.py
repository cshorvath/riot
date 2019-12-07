from core.bootstrap import get_db_engine, get_db_session
from core.util import parse_config_from_env

config = parse_config_from_env("RIOT_API_CONFIG_FILE")
SECRET_KEY = config.secret_key
ALGORITHM = "HS256"

db_engine = get_db_engine(
    host=config.db.host,
    port=config.db.port,
    user=config.db.user,
    password=config.db.password,
    db=config.db.database
)


def get_db():
    with get_db_session(db_engine) as session:
        yield session
