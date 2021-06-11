import pandas as pd
from sqlalchemy.sql import select

from .tankdb_objects import engine, traindata_table

def load_dataframe(station_uuids):
    s = select([traindata_table]).where(traindata_table.c.station_uuid.in_(station_uuids))
    df = pd.read_sql_query(
        s,
        engine
    )
    return df