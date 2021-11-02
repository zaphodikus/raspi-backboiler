# sample app to display the live values in the sensors table

import sys
import os
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from flasktest.raspberry.raspberry import is_raspberrypi, Stats
from dbaccess.sensors import DbSensorDatabase, DbSensor
from shared.sensor_config import SystemConfig

if __name__ == "__main__":
    if is_raspberrypi():
        db = DbSensorDatabase(db_root_path=SystemConfig.ramdisk_path)
    else:
        db = DbSensorDatabase()

    # load all sensor rows
    conn = db.get_connection()
    conn.