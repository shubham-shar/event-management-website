from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database_setup import Base, UserAccounts, UserProfiles, Teams, ListItems, Messages, TeamMembers, Events, Comments

engine = create_engine('sqlite:///event_database.sql')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

user = UserAccounts(username="root",
                    password="root",
                    acc_type="master")
session.add(user)
session.commit()
