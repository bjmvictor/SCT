import logging
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
LOG_FOLDER = os.path.join(script_dir, 'logs')
os.makedirs(LOG_FOLDER, exist_ok=True)

log_file = os.path.join(LOG_FOLDER, "logfile.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')