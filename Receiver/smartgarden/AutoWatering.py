
import argparse
import xml.etree.ElementTree as ET
import time
import datetime
from datetime import date
import logging
import sys
import threading

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='modes.XML fullpath', type=str, required=True)
args = parser.parse_args()
path = args.path

def autowater(path):
    print("autowater function started" + path)
    # path ->  /home/pi/planter/django/smartgarden/static/mode.xml

    logging.basicConfig(filename="watering.log",
                                filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%Y/%m/%d-%H:%M:%S',
                                level=logging.DEBUG)
    logging.info("STARTED FUNCTION")

    wateringtime = 6000 # in seconds
    today = date.today()
    currentmode = ""
    lastwateringday = ""
    while (True):
        print("while true fut")
        tree = ET.parse(path)
        root = tree.getroot()

        for child in root:
            if (child.tag == "mode"):
                currentmode = child.text
        if (currentmode != "AUTO"):
            print ("currentmode != AUTO Quiting")
            logging.info("currentmode is not AUTO quiting")
            break
        else:
            if ((lastwateringday == "") or (lastwateringday != today.strftime("%m/%d/%Y"))):
                lastwateringday = today.strftime("%m/%d/%Y")
                logging.info("Watering at " + lastwateringday)
                print ("Watering at " + lastwateringday)
                # LOCSOLÁS MEGHIVÁSA
                time.sleep(1) # 10 percet locsol

                #locsolás abbahagyása meghivása
        time.sleep(5)

    logging.info("EXITED " + lastwateringday)
    print ("EXITED FROM APPLICATION")

t = threading.Thread(target=autowater,name='wateringagent',args=(path,))
#t.daemon = True
t.start()
print("thread started")