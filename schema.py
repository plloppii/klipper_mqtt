from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel

class Machine(BaseModel):
    bot_number:int
    mqtt_instance:str
    platform_type:str
    customer:Optional[str]

    class Config:
        orm_mode=True

class Print_History(BaseModel):
    machine_id:Optional[str]
    job_id:str
    file_name:str
    status:str
    start_time:datetime
    end_time:Optional[datetime]
    print_duration:int
    total_duration:int
    slicer_estimated_time:int
    filament_used:int
    file_size:Optional[int]
    slicer:Optional[str]
    material:Optional[str]
    nozzle_diameter:Optional[str]
    first_layer_height:Optional[str]
    first_layer_bed_temp:Optional[str]
    object_height:Optional[int]
    print_metadata:Optional[Dict]

    class Config:
        orm_mode=True


