from sqlalchemy import MetaData, create_engine, select, insert, Column, Integer,String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column, relationship



metadata = MetaData()
engine = create_engine("sqlite:///db.db",echo=True)
sess = sessionmaker(engine)

def create_tables():
    engine.echo = False
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship('Project', secondary='project_users', back_populates='users')


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship('User', secondary='project_users', back_populates='projects')


class ProjectUser(Base):
    __tablename__ = "project_users"

    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

create_tables()

with sess() as session:
    usr1 = User(name="bob")
    session.add(usr1)

    
    usr2 = User(name="alice")
    session.add(usr2)

    session.commit()

    # add projects
    prj1 = Project(name="Project 1")
    session.add(prj1)

    prj2 = Project(name="Project 2")
    session.add(prj2)

    session.commit()

    # map users to projects
    prj1.users = [usr1, usr2]
    prj2.users = [usr2]

    session.commit()

