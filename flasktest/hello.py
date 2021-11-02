import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from .raspberry.raspberry import is_raspberrypi, Stats
from dbaccess.sensors import DbSensorDatabase, DbSensor
from shared.sensor_config import SystemConfig


app = Flask(__name__)
if is_raspberrypi():
    db = DbSensorDatabase(db_root_path=SystemConfig.ramdisk_path)
else:
    db = DbSensorDatabase()


@app.route('/')
def home():
    return "Hello Flask Homepage"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sensors')
def about():
    temp_table = ""
    for sensor in
    return render_template('sensors.html', temperatures=temp_table)


@app.route('/system')
def system():
    cpu = Stats.get_cpu()
    hw_system = Stats.get_system()
    free, used = Stats.get_disk_space()
    memory = Stats.get_free_memory()
    average = Stats.get_average_cpu()
    return render_template('system.html',
                           cpu=cpu, system=hw_system, free=free,
                           used=used, memory=memory, average=average)

