#
# Copyright 2021 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
import random
import time
from flask import Flask
from flask import request

FLASK_PORT_NUM = 9005
app = Flask(__name__)

PREFIX_CONTROL = '/api/control'
PREFIX_DATA = '/api/data'
PREFIX_PERSONNEL_DATA = '/api/personnel_data'


def current_time():
    return time.strftime('%H:%M:%S')


def get_random_number():
    return random.randint(1, 30)


@app.route(PREFIX_CONTROL + '/start_robot')
def start_robot():
    jdf = """{
            "time": \"""" + str(current_time()) + """\",
            "command": "Starting Robot",
            "id": "1111",
            "Lname": "scott",
            "Age": "30"
            }
            """
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200


@app.route(PREFIX_CONTROL + '/stop_robot')
def stop_robot():
    jdf = """{
            "time": \"""" + str(current_time()) + """\",
            "command": "Stopping Robot",
            "id": "1111",
            "Lname": "scott",
            "Age": "30"
            }
            """
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200


@app.route(PREFIX_DATA + '/read_data')
def read_data():
    jdf = """{
            "time": \"""" + str(current_time()) + """\",
            "command": "Reading Robot Data",
            "serial_number": "1111",
            "left_arm_weight": "5kg",
            "right_arm_weight": "5kg",
            "sensors": "LDR",
            "Lname": "scott",
            "Age": "30"
            }
            """
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200


@app.route(PREFIX_PERSONNEL_DATA + '/get_safety_data')
def get_safety_data():
    production_sector = [get_random_number(), get_random_number()]
    production_sector += [production_sector[0] + production_sector[1]]

    non_production_sector = [get_random_number(), get_random_number()]
    non_production_sector += [non_production_sector[0] + non_production_sector[1]]

    full_area = [production_sector[i] + non_production_sector[i] for i in range(len(production_sector))]

    jdf = """{
            "time": \"""" + str(current_time()) + """\",
            "command": "getting safety data",
            "production_sector": {
                "with_helmet": \"""" + str(production_sector[0]) + """\",
                "without_helmet": \"""" + str(production_sector[1]) + """\",
                "total": \"""" + str(production_sector[2]) + """\"
            },
            "non_production_sector": {
                "with_helmet": \"""" + str(non_production_sector[0]) + """\",
                "without_helmet": \"""" + str(non_production_sector[1]) + """\",
                "total" : \"""" + str(non_production_sector[2]) + """\"
            },
            "full_area": {
                "with_helmet": \"""" + str(full_area[0]) + """\",
                "without_helmet": \"""" + str(full_area[1]) + """\",
                "total" : \"""" + str(full_area[2]) + """\"
            }
            }
            """
    # TODO: add more fields (some safety violation records?)
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200


@app.route(PREFIX_DATA + '/get_occupancy')
def get_occupancy():
    occupancy = get_random_number()
    jdf = """{
            "time": \"""" + str(current_time()) + """\",
            "command": "getting occupancy",
            "occupancy":""" + str(occupancy) + """
            }
            """
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200


app.run(port=FLASK_PORT_NUM, host='0.0.0.0')
