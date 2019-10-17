# TODO Translate into a class and then incorporate into https://github.com/Stevens-Shuttles/data
import datetime as datetime
import json
import pytz

today = datetime.date.today()


def get_shuttle(line):
    current = datetime.datetime.now().timestamp()
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


def convert_one_to_epoch(time):
    t = datetime.datetime.strptime(time, '%H:%M %p').time()
    return datetime.datetime.combine(today, t).timestamp()


def convert_to_epoch_whole_line(line):
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            for stop in data[s]:
                if "Drop" not in stop and "-" not in stop:
                    stop_mod = stop.replace(".", "")
                    t = datetime.datetime.strptime(stop_mod, '%H:%M %p').time()
                    data.append(datetime.datetime.combine(today, t).timestamp())
    return data


def convert_to_epoch_stop(line, my_stop):
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            # Important piece
            if s == my_stop:
                for stop in data[s]:
                    if "Drop" not in stop and "-" not in stop:
                        stop_mod = stop.replace(".", "")
                        t = datetime.datetime.strptime(stop_mod, '%H:%M %p').time()
                        data.append(datetime.datetime.combine(today, t).timestamp())
    return data


def convert_to_epoch_now(line, my_stop, n):
    current = datetime.datetime.now().timestamp()
    counter = 0
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            if s == my_stop:
                for stop in data[s]:
                    if "Drop" not in stop and "-" not in stop:
                        stop_mod = stop.replace(".", "")
                        t = datetime.datetime.strptime(stop_mod, '%I:%M %p').time()
                        x = datetime.datetime.combine(today, t).timestamp()
                        # important piece
                        if x > current and counter < n:
                            data.append(x)
                            counter += 1
    return data


def timezone(ts):
    tz = pytz.timezone('America/New_York')
    dt = datetime.datetime.fromtimestamp(tz)
    return dt


def print_times(arr):
    for i in arr:
        print(i)


# Example Usage #

# pick a line
myLine = get_shuttle("Green")

# returns in epoch all the times for any given stop
# print_times(convert_to_epoch_stop(myLine, "8th & Monroe"))

# returns in epoch all the times for any given route
# print_times(convert_to_epoch_whole_line(myLine))

# returns the next N times for any given stop
# print(convert_to_epoch_now(myLine, "8th & Monroe", 5))

# convert to local timezone (can be done when we figure out how exactly we will use this)
# timezone(convert_to_epoch_now(myLine, "8th & Monroe", 1)[0])
