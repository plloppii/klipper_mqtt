from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel,Json
from sqlalchemy.orm import Session
from typing import Optional,List
from .database import SessionLocal
from . import models, schema, crud
from . import mqtt as mymqtt

import paho.mqtt.client as mqtt

app=FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

client=mymqtt.MyClient(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

@app.get('/')
def index():
    return {'message': 'Hello World'}

@app.get('/print_history',response_model=List[schema.Print_History],status_code=200)
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_print_history(db)

@app.get('/print_history/{job_id}',response_model=schema.Print_History,status_code=status.HTTP_200_OK)
def get_an_item(job_id: str, db: Session = Depends(get_db)):
    return crud.get_print_by_job_id(db, job_id)

@app.get('/fetch/print_history', status_code=status.HTTP_200_OK)
def fetch_print_history(db:Session=Depends(get_db)):
    client.fetch_all_print_history()
    return {"message": "Fetched Print History"}

@app.post('/machine', response_model=List[schema.Machine], status_code=status.HTTP_201_CREATED)
def create_machine(new_machines: List[schema.Machine], db:Session=Depends(get_db)):
    non_existing_machines = []
    for m in new_machines:
        existing_machine=crud.get_machine_by_id(db, m.bot_number)
        if not existing_machine: non_existing_machines.append(m)
    if not non_existing_machines:
        raise HTTPException(status_code=400,detail="All requested machines already exists")
    created_machines = crud.create_machines(db, non_existing_machines)
    return created_machines

# @app.get('/machine/fetch', response_model=schema.Machine, status_code=status.HTTP_201_CREATED)
# def fetch_machines(db: Session = Depends(get_db)):
#     return "Fetch machines endpoint"


@app.post('/items',response_model=schema.Print_History, status_code=status.HTTP_201_CREATED)
def create_an_item(item:schema.Print_History):
    db_item=db.query(models.Print_History).filter(models.Print_History.name==item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=400,detail="Print_History already exists")
    new_item=models.Print_History(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )
    db.add(new_item)
    db.commit()

    return new_item

@app.put('/item/{item_id}',response_model=schema.Print_History,status_code=status.HTTP_200_OK)
def update_an_item(item_id:int,item:schema.Print_History):
    item_to_update=db.query(models.Print_History).filter(models.Print_History.id==item_id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description
    item_to_update.on_offer=item.on_offer

    db.commit()

    return item_to_update

@app.delete('/item/{item_id}')
def delete_item(item_id:int):
    item_to_delete=db.query(models.Print_History).filter(models.Print_History.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()

    return item_to_delete