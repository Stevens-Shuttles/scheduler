import json
from datetime import date, datetime, timezone
today = date.today()

test = json.dumps({"route_id": "Gray", "stop_ids": "11th & Park","amount": 3})



def lambda_handler(event, context):
    # TODO implement
    json_data = json.loads(event)
    route_id = json_data['route_id']
    stop_ids = json_data['stop_ids']
    amount = json_data['amount']
    route = get_shuttle(route_id)
    l = convert_to_epoch_now(route, stop_ids, amount)
    
    output = {
        "route_id": route_id,
        "stops" : [
            { "id": stop_ids, "times": l }
        ]
    }
    
    
    output_json = json.loads(output)
    
    print(output_json)
    # return {
    #     'isBase64Encoded': False,
    #     'statusCode': 200,
    #     'body': output_json
    # }

def convert_one_to_epoch(time):
    t = datetime.strptime(time, '%H:%M %p').time()
    return datetime.combine(today, t).timestamp()


def get_shuttle(line):
    current = datetime.now(timezone.utc).timestamp()
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
    current = datetime.now().timestamp()
    counter = 0
    result_list = []
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            if s == my_stop:
                for stop in data[s]:
                    if "Drop" not in stop and "-" not in stop:
                        stop_mod = stop.replace(".", "")
                        t = datetime.strptime(stop_mod, '%I:%M %p').time()
                        x = datetime.combine(today, t).timestamp()
                        # important piece
                        if x > current and counter < n:
                            result_list.append(x)
                            counter += 1
    return result_list



lambda_handler(test, 0)
