# noinspection PyUnresolvedReferences
from typing import List

from sqlalchemy.orm import sessionmaker

from common.model import Base, engine
from common.model.model import User, Device


import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
# session.commit()

x: List[User] = session.query(User).all()
d = x[0].devices[0]