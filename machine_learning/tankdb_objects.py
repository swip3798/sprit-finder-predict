from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine, MetaData

DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
IP = os.getenv("MYSQL_IP")
PORT = os.getenv("MYSQL_PORT")

engine = create_engine('mysql+mysqlconnector://root:{}@{}:{}/tankdb'.format(DB_PASSWORD, IP, PORT), echo=False, pool_recycle=7200)

meta = MetaData(bind=engine, reflect=True)
traindata_table = meta.tables["train_data"]