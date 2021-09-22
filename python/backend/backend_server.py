#
# (C) Copyright IBM Corp. 2019
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

    full_area = [get_random_number(), get_random_number()]
    full_area += [full_area[0] + full_area[1]]

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
