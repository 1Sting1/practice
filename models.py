from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    map_url = Column(String)
    attractions = relationship("Attraction", back_populates="city")

class Attraction(Base):
    __tablename__ = 'attractions'
    id = Column(Integer, primary_key=True, index=True)
    id_city = Column(Integer, ForeignKey('cities.id'))
    name = Column(String, nullable=False)
    img = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    type_id = Column(Integer, ForeignKey('types.id'))
    type = relationship("Type", back_populates="attractions")
    city = relationship("City", back_populates="attractions")

class Like(Base):
    __tablename__ = 'likes'
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)
    value = Column(Integer)

class Comment(Base):
    __tablename__ = 'comments'
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)
    rating = Column(Integer)
    date = Column(Date)
    comment = Column(String)

class Attendance(Base):
    __tablename__ = 'attendance'
    attraction_id = Column(Integer, ForeignKey('attractions.id'), primary_key=True)
    monday = Column(Integer)
    tuesday = Column(Integer)
    wednesday = Column(Integer)
    thursday = Column(Integer)
    friday = Column(Integer)
    saturday = Column(Integer)
    sunday = Column(Integer)

class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attractions = relationship("Attraction", back_populates="type")
