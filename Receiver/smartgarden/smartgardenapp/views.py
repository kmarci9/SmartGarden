from django.shortcuts import render
from django.http import HttpResponse
from smartgardenapp.models import Espdata
import xml.etree.ElementTree as ET
import json
from urllib.request import Request, urlopen
from datetime import date
from django.conf import settings
import logging
import time
import threading
import RPi.GPIO as GPIO



# Create your views here.
"""
def home_view(request,*args, **kwargs):

    print (Espdata.objects.all()[0].temperature)
	obj = Espdata.objects.reverse()[:5].values('temperature')
	created = Espdata.objects.reverse()[:5].values('created')

	context = {
		'queryset': obj,
		'created': created
    }

    return render(request, "index.html", context)
    
"""    
def home_view(request,*args, **kwargs):
	# utolsó 20 rekord lekérdezése idő szerint
	temperature = Espdata.objects.all().order_by('-created')[:20].values('temperature');
	temperature = reversed(temperature)

	created = Espdata.objects.all().order_by('-created')[:20].values('created');
	created = reversed(created)

	soil = Espdata.objects.all().order_by('-created')[:20].values('soil');
	soil = reversed(soil)

	# contextbe írás
	context = {
		'temperature': temperature,
		'created': created,
		'soil' : soil

			
	}
	return render(request, "index.html", context)


def mode_view(request,*args, **kwargs):

	if (request.GET.get('mybtn')):
		print (int(request.GET.get('mytextbox')))

	context = setContext()

	return render(request, "modes.html", context)


def startwater(request):

	context = setContext()
	Startwatering(True)
	return render(request, "modes.html", context)

def stopwater(request):
	context = setContext()
	Startwatering(False)
	return render(request, "modes.html", context)

def setauto(request,path):
	writemode("AUTO")
	#context = setContext()
	#os.system("python3 AutoWatering.py --path " + path)
	#return render(request, "modes.html", context)

def setmanual(request):
	writemode("MANUAL")
	context = setContext()
	return render(request, "modes.html", context)


def setContext():
	mode = ""
	long = ""
	lat = ""
	path = str(settings.STATICFILES_DIRS[0]) +  '/' + 'mode.xml'
	print (path)
	tree = ET.parse(path)
	root = tree.getroot()
	for child in root:
		if child.tag == "mode":
			mode = child.text
		elif child.tag == "long":
			long = child.text
		elif child.tag == "lat":
			lat = child.text

	dict, sum = getprecipfromloc(float(long),float(lat))
	#print (sum)
	context = {
		'mode': mode,
		'long': long,
		'lat' : lat,
		'precip' : round(sum,2),
		'dict': dict,
	}
	return context


def autoClick(request):
    path = str(settings.STATICFILES_DIRS[0]) +  '/' + 'mode.xml'
    t1 = threading.Thread(target=autowater,name='watering',args=(path,))
    t2 = threading.Thread(target=setauto,name='django auto',args=(request,path,))
    t2.start()
    t2.join()
    t1.start()
    return render(request, "modes.html", setContext())


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
            soil = Espdata.objects.all().order_by('-created')[:3].values('soil');
            soil = list(reversed(soil))
            sum = 0
            for dicti in soil:# listaban levö dictionary
                for key in dicti: # dictionary itself
                    sum += (dicti[key])

            if ((sum/3) < 50):
                pass
				#locsolj
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



def writemode(ip_str):
	path = str(settings.STATICFILES_DIRS[0]) +  '/' + 'mode.xml'
	tree = ET.parse(path)
	root = tree.getroot()
	for child in root:
		if child.tag == "mode":
			child.text = ip_str
	tree.write(path)

def setlong(request):
	if (request.GET.get('mybtn')):
		try:
			long = float(str(request.GET.get('longtxtbox')))
			# writing long
			path = str(settings.STATICFILES_DIRS[0]) +  '/' + 'mode.xml'
			tree = ET.parse(path)
			root = tree.getroot()
			for child in root:
				if child.tag == "long":
					child.text = str(long)
			tree.write(path)
		except:
			pass




	context = setContext()
	return render(request, "modes.html", context)


def setlat(request):
	if (request.GET.get('mybtn')):
		try:
			lat = float(str(request.GET.get('lattxtbox')))
		except:
			# writing long
			path = str(settings.STATICFILES_DIRS[0]) +  '/' + 'mode.xml'
			tree = ET.parse(path)
			root = tree.getroot()
			for child in root:
				if child.tag == "lat":
					child.text = str(lat)
			tree.write(path)
			
	context = setContext()
	return render(request, "modes.html", context)


def getprecipfromloc(long,lat):
    # input float: long , float: lat
    #returns dict:including the days, float: sum precipation in mm

    urlstr = "https://api.met.no/weatherapi/locationforecast/2.0/compact.json?lat=" + str(lat) + "&lon=" + str(long)
    req = Request(urlstr)
    req.add_header('User-Agent', 'https://github.com/kmarci9/SmartGarden')
    content = urlopen(req).read()
    data = json.loads(content)

    list = ((data["properties"])["timeseries"])
    #print (data,indent = 4, sort_keys=True)
    #print(json.dumps(list, indent = 4, sort_keys=True))
    dict = {}
    cnt = 0
    try:
        for i in list:
            cnt = cnt + 1
            date = i.get('time')
            date = date[:date.find('T')] #stripping the date
            try:
                if date not in dict:
                    dict[date] = i['data']['next_1_hours']['details'].get('precipitation_amount')
                else:
                    dict[date] = dict.get(date) + i['data']['next_1_hours']['details'].get('precipitation_amount')
            except: #ha nem érhető el 1 órás akkor 6 órásat használunk
                try:
                    if date not in dict:
                        dict[date] = i['data']['next_6_hours']['details'].get('precipitation_amount')
                    else:
                        dict[date] = dict.get(date) + i['data']['next_6_hours']['details'].get('precipitation_amount')
                except:
                    break
    except:
        return None, 0
            
    sum = 0
    for key in dict:
        sum = dict[key] + sum
    return dict, sum


	
def Startwatering(bool):
	WATER_GPIO = 27
	GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
	GPIO.setup(WATER_GPIO, GPIO.OUT) # GPIO Assign mode
	if (bool):
		GPIO.output(WATER_GPIO, GPIO.LOW) # out
	else:
		GPIO.output(WATER_GPIO, GPIO.HIGH) # out
