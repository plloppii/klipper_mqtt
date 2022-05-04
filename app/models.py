from sqlite3 import Date
from sqlalchemy.orm import declarative_base
from sqlalchemy import String,Boolean,Integer,Column,Text,JSON,DateTime
from sqlalchemy.sql import func

Base=declarative_base()

class Machine(Base):
    __tablename__='machine'
    id=Column(Integer, primary_key=True)
    bot_number=Column(Integer, unique=True)
    mqtt_instance=Column(String,unique=True)
    platform_type=Column(String)
    customer=Column(String)

class Print_History(Base):
    __tablename__='print_history'
    id=Column(Integer,primary_key=True)
    machine_id=Column(String(255),nullable=True)
    job_id = Column(String, unique=True)
    file_name=Column(Text)
    file_size=Column(Integer)
    status=Column(Text)
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    print_duration=Column(Integer)
    total_duration=Column(Integer)
    slicer_estimated_time=Column(Integer)
    filament_used=Column(Integer)
    slicer=Column(Text)
    material= Column(Text)
    nozzle_diameter = Column(Text)
    first_layer_height= Column(Text)
    first_layer_bed_temp = Column(Text)
    object_height = Column(Integer)
    print_metadata=Column(JSON)
    created_on=Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Print History Line Item name={self.file_name}"