from dotenv import load_dotenv
load_dotenv()
try:
    import os
    os.makedirs("log")
except:
    pass
import logging
import logging.handlers
import sys
logging.basicConfig(format='%(levelname)s [%(asctime)s]:%(message)s', level=logging.INFO, handlers=[
    logging.handlers.RotatingFileHandler("log/TankAnalysis.log", encoding="utf-8", maxBytes = 1024 * 512, backupCount = 10),
    logging.StreamHandler(sys.stdout)
])
from rest_api import app

#app.run(host='0.0.0.0', port=8080, server="gunicorn")