import json
from datetime import date, datetime, timezone, timedelta, time
import os, time
from dateutil import tz

today = date.today()

def lambda_handler():
    json_data = json.loads(event["body"])
    route_id = json_data['route_id']
    # amount = json_data['amount']
    
    #temp
    # route_id = "Gray"
    # amount = 5

    EASTERN = tz.gettz('America/New_York')
    current = datetime.utcnow()
    current = current.replace(tzinfo = EASTERN)

    #print("HELLO"+str(current))
    
    route = get_shuttle(route_id)
    
    #number of stops
    num = sum(1 for line in open(route))
    num = num - 2

    mydict = {"route_id": route_id, "nums_stops": num}
    mydict["stops"] = []
    mystops = mydict["stops"]


    with open(route) as json_file:
        data = json.load(json_file)
        for s in data:
            l = convert_to_epoch_now(route, s, amount)
            mystops.append({"id": s, "times": l})

    
    output_json = json.dumps(mydict)
    #print("test")
    print(output_json) 
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'body': output_json
    }

def convert_one_to_epoch(time):
    t = datetime.strptime(time, '%H:%M %p').time()
    return datetime.combine(today, t).timestamp()


def get_shuttle(line):
    current = datetime.utcnow().timestamp()
    gray_late = convert_one_to_epoch("10:45 pm")
    red_early = convert_one_to_epoch("7:21 am")

    # TODO load times from a configuration file so that they can be updated from a GUI
    if today.weekday() == 5:
        return "json/Saturday.json"
    elif today.weekday() == 6:
        return "json/Sunday.json"
    elif line == "Breaks" or line == "ResLineBreaks":
        return "json/ResLineBreaks.json"
    else:
        if line == "Blue":
            return "json/Blue.json"
        elif line == "Gray":
            if gray_late > current:
                return "json/GrayLate.json"
            else:
                return "json/Gray.json"
        elif line == "Red":
            if red_early < current:
                return "json/RedEarly.json"
            else:
                return "json/Red.json"
        elif line == "Green":
            return "json/Green.json"
        else:
            return "Null"
            

def convert_to_epoch_now(line, my_stop, n):
    #current time
    current = datetime.utcnow().timestamp()
    #n counter
    counter = 0
    #list of next times
    result_list = []
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            #correct stop
            if s == my_stop:
                for stop in data[s]:
                    #bad data ignored
                    if "Drop" not in stop and "-" not in stop:
                        #remove AM/PM
                        stop_mod = stop.replace(".", "")
                        
                        #one day amount for rides at midnight
                        tomorrow = today + timedelta(days=1)
                        
                        #t = formatted version of (X)X:XX A.M/P.M
                        t = datetime.strptime(stop_mod, '%I:%M %p').time()
                        
                        #current timestamp
                        x = datetime.combine(today, t).timestamp()
                        #tomorrow with current time
                        tx = datetime.combine(tomorrow, t).timestamp()
                        # important piece
                        if (x > current and counter < n) or (counter > 0 and counter < n) :
                           # print("counter:"+ str(counter) + "    date today:" + str(datetime.fromtimestamp(x)) + "    date tmrw:" + str(datetime.fromtimestamp(tx))) 
                            if(x < current):
                                result_list.append(tx)
                                counter += 1
                            else:
                                result_list.append(x)
                                counter += 1
    return result_list


lambda_handler()