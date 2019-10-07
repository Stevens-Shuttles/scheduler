import datetime as dt
import json
today = dt.date.today()
darr = []

with open('scheduler/json/Blue.json') as json_file:
	data = json.load(json_file)
	for s in data:
		for stop in data[s]:
			if "Drop" not in stop and "-" not in stop:
				stop_mod = stop.replace(".","")
				print(stop_mod)
				time = dt.datetime.strptime(stop_mod, '%H:%M %p').time()
				darr.append(dt.datetime.combine(today, time).timestamp())

for i in darr:
	print(i)