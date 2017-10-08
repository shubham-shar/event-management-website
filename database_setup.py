from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class UserAccounts(Base):
    __tablename__ = 'user_accounts'

    username = Column(String(80), primary_key=True)
    password = Column(String(80), nullable=False)
    acc_type = Column(String(10), default="default")


class UserProfiles(Base):
    __tablename__ = 'user_profiles'

    f_name = Column(String(80), nullable=False)
    l_name = Column(String(80), nullable=False)
    dob = Column(String(20), nullable=False)
    mobile = Column(String(13))
    gender = Column(String(6), nullable=False)
    rollno = Column(String(20))
    username = Column(String(80), ForeignKey('user_accounts.username'),
                      primary_key=True)
    user_accounts = relationship(UserAccounts)
    email = Column(String(80), nullable=False)


class Events(Base):
    __tablename__ = 'events'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    type = Column(String(8), nullable=False)
    starts = Column(String(20), nullable=False)
    ends = Column(String(20), nullable=False)
    description = Column(Text)
    club = Column(String(20), nullable=False)
    post_date = Column(String(20), nullable=False)
    head = Column(String(80), ForeignKey('user_accounts.username'))
    user_accounts = relationship(UserAccounts)


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    team_head = Column(String(80), ForeignKey('user_accounts.username'))
    user_accounts = relationship(UserAccounts)
    event_id = Column(Integer, ForeignKey('events.id'))
    events = relationship(Events)


class ListItems(Base):
    __tablename__ = 'list_items'

    id = Column(Integer, primary_key=True)
    item = Column(String(80), nullable=False)
    done = Column(Boolean, default=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    teams = relationship(Teams)


class TeamMessages(Base):
    __tablename__ = 'team_messages'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    message = Column(Text)
    team_id = Column(Integer, ForeignKey('teams.id'))
    teams = relationship(Teams)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    message = Column(Text)
    time = Column(String(80))
    from_user = Column(String(80))
    username = Column(String(80), ForeignKey('user_accounts.username'),
                      nullable=False)
    user_accounts = relationship(UserAccounts)


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(Text)
    event_id = Column(Integer, ForeignKey('events.id'))
    events = relationship(Events)
    username = Column(String(80), ForeignKey(
        'user_accounts.username'), nullable=False)
    user_accounts = relationship(UserAccounts)
    post_date = Column(String(20), nullable=False)


class TeamMembers(Base):
    __tablename__ = 'team_members'

    team_id = Column(Integer, ForeignKey('teams.id'))
    teams = relationship(Teams)
    id = Column(Integer, primary_key=True)
    member = Column(String(80), ForeignKey('user_accounts.username'))
    user_accounts = relationship(UserAccounts)


engine = create_engine('sqlite:///event_database.sql')

Base.metadata.create_all(engine)
