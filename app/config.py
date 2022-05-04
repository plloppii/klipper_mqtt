from pydantic import BaseSettings
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

class Settings(BaseSettings):
    MOSQUITTO_MQTT_BROKER_HOST:str 
    MOSQUITTO_MQTT_BROKER_PORT:int
    MOSQUITTO_MQTT_BROKER_USERNAME:str 
    MOSQUITTO_MQTT_BROKER_PASSWORD:str 

    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_HOST:str
    POSTGRES_SCHEMA:str

    class Config:
        env_file = "config/dev.env"