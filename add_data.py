from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database_setup import Base, UserAccounts, UserProfiles, Teams, ListItems, Messages, TeamMembers, Events, Comments

engine = create_engine('sqlite:///event_database.sql')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

user = UserAccounts(username="johndoe1",
                    password="johndoe1")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe1@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe2",
                    password="johndoe2")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe2@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe3",
                    password="johndoe3")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe3@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe4",
                    password="johndoe4")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe4@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe5",
                    password="johndoe5")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe5@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe6",
                    password="johndoe6")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe6@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe7",
                    password="johndoe7")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe7@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe8",
                    password="johndoe8")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe8@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe9",
                    password="johndoe9")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe9@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe10",
                    password="johndoe10")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe10@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe11",
                    password="johndoe11")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe11@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe12",
                    password="johndoe12")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe12@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe13",
                    password="johndoe13")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe13@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe14",
                    password="johndoe14")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe14@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe15",
                    password="johndoe15")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe15@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe16",
                    password="johndoe16")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe16@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe17",
                    password="johndoe17")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe17@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe18",
                    password="johndoe18")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe18@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe19",
                    password="johndoe19")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe19@gmail.com")
session.add(profile)
session.add(user)
session.commit()

user = UserAccounts(username="johndoe20",
                    password="johndoe20")
profile = UserProfiles(f_name="John",
                       l_name="Doe",
                       dob="1997-01-01",
                       mobile="9632587410",
                       gender="M", rollno="1234567890",
                       user_accounts=user,
                       email="john.doe20@gmail.com")
session.add(profile)
session.add(user)
session.commit()

print "all done"
