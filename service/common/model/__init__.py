from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# TODO
engine = create_engine('mysql+mysqldb://riot:riot@127.0.0.1/riot', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)

Base = declarative_base()
