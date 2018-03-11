#!/usr/bin/python
import os
import sys
from numpy import array, dot, argsort
from numpy.linalg import norm
INPUT_FILE_NAME = "2015taiwan.txt"
OUTPUT_FILE_NAME = "out.txt"
DATA_LIST = list()
KNN_LIST = list()


def run():
    global INPUT_FILE_NAME, DATA_LIST, OUTPUT_FILE_NAME
    with open(INPUT_FILE_NAME, 'r') as file:
        for i, line in enumerate(file):
            # skip first line
            if i == 0:
                continue
            data = line.strip().split(',')
            state = data[2]
            if state == "PM2.5":
                DATA_LIST.append(data)
    avg()
    with open(OUTPUT_FILE_NAME, 'w') as file:
        for data in DATA_LIST:
            string = ",".join(str(x) for x in data)
            file.write(string + "\n")
    K_NN()
    while True:
        userInput()


def avg():
    tempData = [0 for x in range(24)]
    errList = list()
    pdata = None
    count = 0
    for data in DATA_LIST:
        if pdata != data[1] and pdata is not None:
            # calculate avg
            for i in range(len(tempData)):
                tempData[i] = round(float(tempData[i]) / float(count), 2)
            # change error data
            for errdata in errList:
                for i in range(len(tempData)):
                    errdata[i + 3] = tempData[i]
            tempData = [0 for x in range(24)]
            errList = list()
            count = 0
        total = 0
        for i in range(len(tempData)):
            try:
                val = int(data[i + 3])
            except ValueError:
                if data not in errList:
                    errList.append(data)
                continue
            total += val
            tempData[i] += val
        if total == 0:
            if data not in errList:
                    errList.append(data)
        count += 1
        pdata = data[1]
    # calculate avg for last group
    for i in range(len(tempData)):
        tempData[i] = round(float(tempData[i]) / float(count), 2)
    # change error data for last group
    for errdata in errList:
        for i in range(len(tempData)):
            errdata[i + 3] = tempData[i]


def K_NN(index=0, k=5):
    global DATA_LIST, KNN_LIST
    KNN_LIST = list()
    sdata = array(map(int, DATA_LIST[index][3:]))
    print "Target: "
    print ",".join(DATA_LIST[index])
    print
    for i, data in enumerate(DATA_LIST):
        if i == index:
            continue
        tdata = array(map(int, data[3:]))
        euclidean_dist = norm(sdata - tdata)
        cos_sim = dot(sdata, tdata) / (norm(sdata) * norm(tdata))
        newdata = list()
        newdata.extend(data)
        newdata.extend((euclidean_dist, cos_sim))
        KNN_LIST.append(newdata)
    KNN_LIST = array(KNN_LIST)
    # sort by eu
    KNN_LIST = KNN_LIST[argsort(KNN_LIST[:, 27])]
    print "Top 5 closesd(euclidean distence):"
    for i, data in enumerate(KNN_LIST):
        if i >= k:
            break
        print ",".join(x for x in data[:-2])
    # sort by cos_sim
    KNN_LIST = KNN_LIST[argsort(KNN_LIST[:, 28])]
    print
    print "Top 5 closesd(cosine simularity):"
    for i, data in enumerate(reversed(KNN_LIST)):
        if i >= k:
            break
        print ",".join(x for x in data[:-2])


def userInput():
    match = False
    index = None
    try:
        inputstr = raw_input("\nPlease input date, place, and k value: ")
    except KeyboardInterrupt:
        print
        sys.exit(0)
    inputstr = inputstr.strip().split(',')
    date = inputstr[0]
    place = inputstr[1]
    try:
        k = int(inputstr[2])
    except ValueError:
        print "Plese input correct k value!"
        return
    for i, data in enumerate(DATA_LIST):
        if data[0] == date and data[1] == place:
            match = True
            index = i
            break
    if match:
        K_NN(index, k)
    else:
        print "No data that match the search!"


if __name__ == "__main__":
    os.system('clear')
    run()
