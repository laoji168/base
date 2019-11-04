from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Users(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def from_item(self, it):
        self.name = it.name
        self.fullname = it.fullname
        return self


class Address (BaseModel):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey('users.id'))
    email_address = Column(String, nullable=False)
