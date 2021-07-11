import pandas as pd
from sqlalchemy.sql import select
import sqlite3
import logging

def load_dataframe_sqlite3(station_uuids):
    con = sqlite3.connect("tankdb/tank.db")
    placeholder_string = "({})".format(",".join(["?" for i in station_uuids]))
    res = con.execute("""SELECT * FROM train_data WHERE station_uuid in {} """.format(placeholder_string), station_uuids).fetchall()
    df = pd.DataFrame(res, columns=["lat","lng","station_uuid","hour","dom","month","year","dow","e5","e10","diesel"])
    return df

from .tankdb_objects import engine, traindata_table

def load_dataframe(station_uuids):
    s = select([traindata_table]).where(traindata_table.c.station_uuid.in_(station_uuids))
    df = pd.read_sql_query(
        s,
        engine
    )
    return df