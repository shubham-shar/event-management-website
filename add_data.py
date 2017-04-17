from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database_setup import Base, UserAccounts, UserProfiles, Teams, ListItems, Messages, TeamMembers, Events, Comments

engine = create_engine('sqlite:///event_database.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

user=UserAccounts(username="skb1129", password="29nov1997", acc_type="master")

session.add(user)
session.commit()

userprof=UserProfiles(f_name="Surya Kant", l_name="Bansal", dob="29/11/1997", mobile="9814068029", gender="M", rollno="1510991666", email="skb1129@yahoo.com", user_accounts=user)

session.add(userprof)
session.commit()

event1=Events(title="Sample Event", type="ongoing", starts="21/04/2017", ends="23/04/2017", description="it is a good event. you will enjoy it.", contact="me", club="dexter's", post_date=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), head="skb1129")

session.add(event1)
session.commit()

print "all done"
