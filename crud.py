from sqlalchemy.orm import Session, joinedload
from models import City, Attraction, Type


def create_city(db: Session, name: str, description: str, map_url: str):
    city = City(name=name, description=description, map_url=map_url)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city

def create_attraction(db: Session, city_id: int, name: str, img: str, latitude: float, longitude: float, type_id: int):
    attraction = Attraction(id_city=city_id, name=name, img=img, latitude=latitude, longitude=longitude, type_id=type_id)
    db.add(attraction)
    db.commit()
    db.refresh(attraction)
    return attraction

def get_attractions(db: Session, city_id: int = None, type_id: int = None, search: str = ""):
    query = db.query(Attraction).options(joinedload(Attraction.type))
    if city_id:
        query = query.filter(Attraction.id_city == city_id)
    if type_id:
        query = query.filter(Attraction.type_id == type_id)
    if search:
        query = query.filter(Attraction.name.ilike(f"%{search}%"))
    return query.all()

def create_type(db: Session, name: str):
    a_type = Type(name=name)
    db.add(a_type)
    db.commit()
    db.refresh(a_type)
    return a_type