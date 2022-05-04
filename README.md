# klipper_mqtt
An API webserver designed to pull print data from klipper machine through mqtt

# uvicorn commands
uvicorn main:app --reload

# mosquitto mqtt commands
mosquitto_sub -v -u mqtt_username -P mqtt_password -t "#"

mosquitto_pub -v -u mqtt_username -P mqtt_password -t "Manitou/moonraker/status" -n -r