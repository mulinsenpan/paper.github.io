
# coding: utf-8

# In[ ]:


"""
Created on Tue May 10 12:26:06 2016

@author: CHI
"""
import sys
import os
import numpy as np
import scipy as sp
import pandas as pd

ACTIVITIES = []
BINSENSORS = []
CONTINUESENSORS = []

metalabel=['activities','bin_sensors','continue_sensors']
def LoadMeta(metalabel):
    metadata = [[] for i in range(3)]
    for i  in range(len(metalabel)):

        filename = "./data/" + metalabel[i] + ".txt"
        with open(filename) as infile:
            for line in infile:
                metadata[i].append(line.strip())
    return metadata


def ExtractActivities(filename):
    """
    获的每个行为的序列片段
    :return: activities
    """
    original_data = []
    with open(filename, 'r') as datafile:
        for line in datafile:
            list_line = line.strip().split()
            original_data.append(list_line)

    # little_data = original_data[0:1000]
    flages = []
    for i in range(len(original_data)):
        if len(original_data[i]) > 4:

            activity = original_data[i][4:][0].split('=')
            if len(activity) == 1:
                continue
            label, state = activity
            flages.append((i, label, state))
    flages_index = 0
    activities = []
    i = 0
    while flages_index < len(flages) - 1:
        original_indexs = range(flages[flages_index][0], flages[flages_index + 1][0])
        activity = [original_data[index][0:4] for index in original_indexs]

        activity.insert(0, flages[flages_index][1])

        flages_index += 2
        activities.append(activity)
    return activities

def GetSensors(acts):
    """
    获取所有的传感器标签
    :param acts:
    :return:
    """
    sensors = []
    binary_sensors = []
    continue_sensors = []
    for act in acts:
        for item in act[1:]:
            if item and item[2] not in sensors:
                sensors.append(item[2])
    # return sensors
    b_prefix = ['M0',"MA","D0","L0","LL"]
    battery = ["BA"]
    for sensor in sensors:
        if sensor[0:2] in b_prefix:
            binary_sensors.append(sensor)
        elif sensor[0:2] in battery:
            continue
        else:
            continue_sensors.append(sensor)
    return binary_sensors,continue_sensors


def GetActs(acts):
    """
    获取所有的行为标签
    :param acts:
    :return:
    """
    activities = []
    for act in acts:
        label = act[0]
        if label not in activities:
            activities.append(label)
    return activities


def Store(acts):
    """
    存储传感器标签、行为标签
    :param acts:
    :return:
    """

    binary_sensors,continue_sensors =GetSensors(acts=acts)
    binary = open("./data/bin_sensors.txt",'w')
    for item in sorted(binary_sensors):
        binary.write(item+'\n')
    binary.close()
    con = open("./data/continue_sensors.txt",'w')
    for item in sorted(continue_sensors):
        con.write(item + '\n')
    con.close()


    labels = GetActs(acts)
    activities = open("./data/activities.txt", 'w')
    for item in sorted(labels):
        activities.write(item + '\n')
    activities.close()


# acts = ExtractActivities('./data/ann.txt')
# Store(acts)
# for act in acts:
#     if act[0] == "Work":
#         print act


# ACTIVITIES,BINSENSORS,CONTINUESENSORS = LoadMeta(metalabel)

