from turtle import color
from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.session import engine, get_db
from db.base import Base
from sqlalchemy.orm import Session
from db.models.salons import Salon
from db.models.hours import Hour
from db.models.amenities import Amenities
from db.models.services import Services

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request, hx_request: Optional[str] =  Header(None), db: Session = Depends(get_db)):
    #salons = [{'name': 'test', 'rating': 4, 'budget': '1-10', 'website': 'http', 'phone': '408', 'address': '123'}]
    salons = show_all_salons(db)
    context = {'request': request, 'salons': salons}
    if hx_request:
        return templates.TemplateResponse("components/table.html", context)
    return templates.TemplateResponse("index.html", context)

def show_all_salons(db):
    return db.query(Salon).all()

@app.get('/budget/')
def budget():
    return add_budget()

def add_budget():
    _budget = _budget + 1 if _budget != 4 else 1
    return '$' * _budget
# @app.get('/service/')
# def budget(budget_int):
#     # budget = budget_int
#     return budget

# @app.get('/query', response_class=HTMLResponse)
# def query(budget, request: Request, hx_request: Optional[str] =  Header(None), db: Session = Depends(get_db),
#  coloring='off', blowout='off'):

#     on_off = {'on': True, 'off': False}
#     budgets = {0: '1-10', 1: '11-30', 2: '31-50'}
#     o = db.query(Salon).select_from(Services).filter(Services.coloring == on_off[coloring])
#     # v = db.query(Services)
#     # o = join(s, v)
    
#     # output = output.filter(Salon.budget == budgets[int(budget)])

#     context = {'request': request, 'salons': o}
#     if hx_request:
#         return templates.TemplateResponse("components/table.html", context)
#     return templates.TemplateResponse("index.html", context)

@app.get('/query',)
def query(budget, request: Request, hx_request: Optional[str] =  Header(None), db: Session = Depends(get_db),
 coloring='off', blowout='off', hair_treatment='off', kids_haircut='off', bridal_service='off', hair_extension='off',
 hairsyling='off', makeup='off', mens_haircut='off', womens_haircut='off', mask_required='off', accepts_card='off',
 accepts_andriod='off', accepts_apple='off', good_for_kids='off', car_parking='off', bike_parking='off', free_wifi='off',
 wheelchair_access='off', restrooms='off', appointments='off'):

    on_off = {'on': True, 'off': False}
    budgets = {'0': '1-10', '1': '11-30', '2': '31-50'}
    
    q = db.query(Salon).filter(Services.coloring == on_off[coloring]).filter(Services.blowout == on_off[blowout])\
    .filter(Services.hair_treatment == on_off[hair_treatment]).filter(Services.kids_haircut == on_off[kids_haircut])\
    .filter(Services.bridal_service == on_off[bridal_service]).filter(Services.hair_extension == on_off[hair_extension])\
    .filter(Services.hairsyling == on_off[hairsyling]).filter(Services.makeup == on_off[makeup])\
    .filter(Services.mens_haircut == on_off[mens_haircut]).filter(Services.womens_haircut == on_off[womens_haircut])\
    .filter(Amenities.mask_required == on_off[mask_required]).filter(Amenities.accepts_card == on_off[accepts_card])\
    .filter(Amenities.accepts_andriod == on_off[accepts_andriod]).filter(Amenities.accepts_apple == on_off[accepts_apple])\
    .filter(Amenities.good_for_kids == on_off[good_for_kids]).filter(Amenities.car_parking == on_off[car_parking])\
    .filter(Amenities.bike_parking == on_off[bike_parking]).filter(Amenities.free_wifi == on_off[free_wifi])\
    .filter(Amenities.wheelchair_access == on_off[wheelchair_access]).filter(Amenities.restrooms == on_off[restrooms])\
    .filter(Amenities.appointments == on_off[appointments])\
    .filter(Salon.budget==budgets[budget]).join(Amenities, Salon.salon_id == Amenities.salon_id).join(Services, Salon.salon_id == Services.salon_id).all()

    context = {'request': request, 'salons': q}
    if hx_request:
        return templates.TemplateResponse("components/table.html", context)
    return templates.TemplateResponse("index.html", context)

# Salon.budget == budgets[budget], Services.coloring == on_off[coloring], 
#     Services.blowout == on_off[blowout], Services.hair_treatment == on_off[hair_treatment], 
#     Services.kids_haircut == on_off[kids_haircut], Services.bridal_service == on_off[bridal_service],
#     Services.hair_extension == on_off[hair_extension], Services.hair_styling == on_off[hairsyling],
#     Services.makeup == on_off[makeup], Services.mens_haircut == on_off[mens_haircut], 
#     Services.womens_haircut == on_off[womens_haircut])