from typing import List
from sqlalchemy.orm import Session
from . import models, schema

def get_all_print_history(db: Session):
    return db.query(models.Print_History).all()

def get_print_by_job_id(db: Session, job_id: str):
    return db.query(models.Print_History).filter(models.Print_History.job_id == job_id).first()

def create_print_history_item(db: Session, line_item: schema.Print_History):
    print(line_item.print_metadata)
    print_item = models.Print_History(
        machine_id = line_item.machine_id,
        job_id = line_item.job_id,
        file_name = line_item.file_name,
        file_size = line_item.file_size,
        status = line_item.status,
        start_time =line_item.start_time,
        end_time = line_item.end_time,
        print_duration = line_item.print_duration,
        total_duration = line_item.total_duration,
        slicer_estimated_time = line_item.print_duration,
        filament_used = line_item.filament_used,
        slicer = line_item.slicer,
        material = line_item.material,
        nozzle_diameter = line_item.nozzle_diameter,
        first_layer_height = line_item.first_layer_height,
        first_layer_bed_temp = line_item.first_layer_bed_temp,
        object_height = line_item.object_height,
        print_metadata = line_item.print_metadata
    )
    db.add(print_item)
    db.commit()

def create_machines(db:Session, machines:List[schema.Machine]):
    created=[]
    for m in machines:
        new_machine = models.Machine(
            bot_number=m.bot_number,
            mqtt_instance=m.mqtt_instance,
            platform_type=m.platform_type,
            customer=m.customer
        )
        created.append(new_machine)
        db.add(new_machine)
    db.commit()
    return created

def get_machine_by_id(db:Session, bot_number:int):
    return db.query(models.Machine).filter(models.Machine.bot_number == bot_number).first()

def get_machines(db:Session):
    return db.query(models.Machine).all()
    