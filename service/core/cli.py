import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from core.model.model import Base

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine: Engine = create_engine('mysql+mysqldb://riot:riot@127.0.0.1/riot', convert_unicode=True)
db_session: scoped_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# user = User(
#     name="Foo",
#     password="boo",
#     admin=False
# )
#
#
# device = Device(
#     name="spider",
#     display_name="g",
#     description="sk"
# )
#
# user.devices.append(device)
#
# session.add_all([user, device])
# # session.commit()
#
# x: List[User] = session.query(User).all()
# d = x[0].devices[0]
