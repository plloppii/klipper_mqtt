import paho.mqtt.client as mqtt
import json
from typing import List
from .database import SessionLocal
from .config import get_settings
from . import schema, crud
import time

config = get_settings()
db = SessionLocal()

TOPIC_INSTANCES=["manitou/", "sr-bot/", "vera/", "nrtl/", "austin/", "gulfcoast/"]
STATUS_TOPIC="klipper/status"
WILDCARD_TOPIC="#"
API_REQUEST_TOPIC="moonraker/api/request"
API_RESPONSE_TOPIC="moonraker/api/response"
JSONRPC_REQUEST= """
{
    "jsonrpc":"2.0",
    "method":"server.history.list",
    "params":{"limit": 500, "order":"asc"},
    "id":5656
}
"""

class MyClient(mqtt.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_pw_set(config.MOSQUITTO_MQTT_BROKER_USERNAME, config.MOSQUITTO_MQTT_BROKER_PASSWORD)
        self.connect_async(config.MOSQUITTO_MQTT_BROKER_HOST, config.MOSQUITTO_MQTT_BROKER_PORT, 60)
        self.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        all_machines = crud.get_machines(db)
        for m in all_machines:
            client.subscribe(m.mqtt_instance+"/"+API_RESPONSE_TOPIC)
        # client.subscribe(WILDCARD_TOPIC)

    def on_message(self, client, userdata, message):
        print("{}, {}".format(message.topic, message.payload))
        topic = message.topic.split("/")[0]
        payload = json.loads(message.payload.decode("utf-8"))
        if "result" in payload and "jobs" in payload["result"]:
            print_jobs = payload["result"]["jobs"]
            for line_item in print_jobs:
                job_id = '{}-{}'.format(topic, int(line_item["job_id"], 16))
                existing_print = crud.get_print_by_job_id(db, job_id)
                if existing_print:
                    print("Print job {} exists in db: {}".format(job_id, existing_print))
                    continue
                metadata = line_item.get("metadata", {})
                print_item = schema.Print_History(
                    machine_id = topic,
                    job_id = job_id,
                    file_name = line_item.get("filename"),
                    file_size = metadata.get("size"),
                    status = line_item.get("status"),
                    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(line_item.get("start_time"))),
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(line_item.get("end_time"))),
                    print_duration = line_item.get("print_duration"),
                    total_duration = line_item.get("total_duration"),
                    slicer_estimated_time = line_item.get("print_duration"),
                    filament_used = line_item.get("filament_used"),
                    slicer =  metadata.get("slicer") + " " + metadata.get("slicer_version") if metadata else None,
                    material = metadata.get("filament_name"),
                    nozzle_diameter = metadata.get("nozzle_diameter"),
                    first_layer_height = metadata.get("first_layer_height"),
                    first_layer_bed_temp = metadata.get("first_layer_bed_temp"),
                    object_height = metadata.get("object_height"),
                    print_metadata = metadata
                )
                crud.create_print_history_item(db, print_item)

    def fetch_all_print_history(self):
        all_machines = crud.get_machines(db)
        for machine in all_machines:
            self.publish(machine.mqtt_instance+"/"+API_REQUEST_TOPIC, JSONRPC_REQUEST)
    def subscribe_to_instances(self, machine_inst:List[schema.Machine]):
        for m in machine_inst:
            self.subscribe(m.mqtt_instance+"/"+API_RESPONSE_TOPIC)


mqtt_client = MyClient(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")