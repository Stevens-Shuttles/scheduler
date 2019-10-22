import datetime as datetime
import json
import pytz

today = datetime.date.today()


def getShuttle(line):
    current = datetime.datetime.now().timestamp()
    grayLate = convertOneToEpoch("10:45 pm")
    redEarly = convertOneToEpoch("7:21 am")

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
            if grayLate > current:
                return "json/GrayLate.json"
            else:
                return "json/Gray.json"
        elif line == "Red":
            if redEarly < current:
                return "json/RedEarly.json"
            else:
                return "json/Red.json"
        elif line == "Green":
            return "json/Green.json"
        else:
            return "Null"


def convertOneToEpoch(time):
    t = datetime.datetime.strptime(time, '%H:%M %p').time()
    return datetime.datetime.combine(today, t).timestamp()


def convertToEpochWholeLine(line):
    darr = []
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            for stop in data[s]:
                if "Drop" not in stop and "-" not in stop:
                    stop_mod = stop.replace("#           # .", "")
                    t = datetime.datetime.strptime(stop_mod, '%I:%M %p').time()
                    darr.append(datetime.datetime.combine(today, t).timestamp())
    return darr


def convertToEpochStop(line, myStop):
    darr = []
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            # Important piece
            if s == myStop:
                for stop in data[s]:
                    if "Drop" not in stop and "-" not in stop:
                        stop_mod = stop.replace(".", "")
                        t = datetime.datetime.strptime(stop_mod, '%I:%M %p').time()
                        darr.append(datetime.datetime.combine(today, t).timestamp())
    return darr


def convertToEpochN(line, myStop, n):
    current = datetime.datetime.now().timestamp()
    counter = 0
    darr = []
    with open(line) as json_file:
        data = json.load(json_file)
        for s in data:
            if s == myStop:
                for stop in data[s]:
                    if "Drop" not in stop and "-" not in stop:
                        stop_mod = stop.replace(".", "")
                        t = datetime.datetime.strptime(stop_mod, '%I:%M %p').time()
                        x = datetime.datetime.combine(today, t).timestamp()
                        # important piece
                        if x > current and counter < n:
                            darr.append(x)
                            counter += 1
    return darr


def timezone(ts):
    tz = pytz.timezone('America/New_York')
    dt = datetime.datetime.fromtimestamp(tz)
    return dt


def printTimes(arr):
    for i in arr:
        print(i)


# Example Usage #

# pick a line
myLine = getShuttle("Green")

# returns in epoch all the times for any given stop
# printTimes(convertToEpochStop(myLine, "8th & Monroe"))

# returns in epoch all the times for any given route
# printTimes(convertToEpochWholeLine(myLine))

# returns the next N times for any given stop
# print(convertToEpochN(myLine, "8th & Monroe", 5))

# convert to local timezone (can be done when we figure out how exactly we will use this)
# timezone(convertToEpochN(myLine, "8th & Monroe", 1)[0])

#           #
