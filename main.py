import os

import uvicorn
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uuid

import crud
import database
import models
from models import City, Attraction, Type
from database import engine, SessionLocal
import imageio
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_cities(request: Request):
    with Session(engine) as session:
        cities = session.query(City).all()
        return templates.TemplateResponse("index1.html", {"request": request, "cities": cities})

@app.get("/city/{city_id}", response_class=HTMLResponse)
async def read_city(request: Request, city_id: int):
    with Session(engine) as session:
        city = session.query(City).filter(City.id == city_id).first()
        attractions = session.query(Attraction).filter(Attraction.id_city == city_id).all()
        return templates.TemplateResponse("city.html", {"request": request, "city": city, "attractions": attractions})

@app.get("/attraction/{attraction_id}", response_class=HTMLResponse)
async def read_attraction(request: Request, attraction_id: int):
    with Session(engine) as session:
        attraction = session.query(Attraction).filter(Attraction.id == attraction_id).first()
        return templates.TemplateResponse("attraction.html", {"request": request, "attraction": attraction})

@app.post("/cities/add")
def add_city(request: Request, name: str = Form(...), description: str = Form(...), map_url: str = Form(...), db: Session = Depends(
    database.get_db)):
    city = crud.create_city(db, name, description, map_url)
    return templates.TemplateResponse("city_added.html", {"request": request, "city": city})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="The file is empty.")

    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[-1]}"
    img_path = f"uploads/{filename}"
    full_path = f"static/{img_path}"

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(contents)

    file_url = f"/static/{img_path}"
    print(file_url)
    return JSONResponse(status_code=200, content={"file_url": file_url})


@app.post("/attractions/add")
def add_attraction(request: Request, city_id: int = Form(...), name: str = Form(...), img: str = Form(...), latitude: float = Form(...), longitude: float = Form(...), type_id: int = Form(...), db: Session = Depends(
    database.get_db)):
    attraction = crud.create_attraction(db, city_id, name, img, latitude, longitude, type_id)
    return templates.TemplateResponse("attraction_added.html", {"request": request, "attraction": attraction})

# Маршрут для страницы добавления города
@app.get("/cities/add")
def get_add_city_form(request: Request):
    return templates.TemplateResponse("add_city.html", {"request": request})

# Маршрут для страницы добавления достопримечательности
@app.get("/attractions/add")
def get_add_attraction_form(request: Request, db: Session = Depends(database.get_db)):
    cities = db.query(City).all()  # Получаем список городов
    types = db.query(Type).all()  # Получаем список типов
    return templates.TemplateResponse("add_attraction.html", {"request": request, "cities": cities, "types": types})

# Маршрут для отображения страницы после добавления города
@app.get("/city_added")
def city_added(request: Request):
    return templates.TemplateResponse("city_added.html", {"request": request})

# Маршрут для отображения страницы после добавления достопримечательности
@app.get("/attraction_added")
def attraction_added(request: Request):
    return templates.TemplateResponse("attraction_added.html", {"request": request})

@app.get("/attractions")
def show_attractions(request: Request, city_id: int = None, type_id: int = None, search: str = None, db: Session = Depends(
    database.get_db)):
    cities = db.query(City).all()
    types = db.query(Type).all()
    attractions = crud.get_attractions(db, city_id=city_id, type_id=type_id, search=search)
    return templates.TemplateResponse("attractions1.html", {"request": request, "attractions": attractions, "cities": cities, "types": types, "search": search, "city_id": city_id, "type_id": type_id})

@app.get("/types/add")
def get_add_type_form(request: Request):
    return templates.TemplateResponse("add_type.html", {"request": request})

# Маршрут для обработки данных формы и добавления нового типа
@app.post("/types/add")
def add_type(request: Request, name: str = Form(...), db: Session = Depends(database.get_db)):
    type = crud.create_type(db, name)
    return templates.TemplateResponse("type_added.html", {"request": request, "name": type.name})

if __name__ == "__main__":
    database.create_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000)
