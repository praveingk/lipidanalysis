#!/usr/local/bin/python


# maAnalyze.py
# Analysis of Mouse Atlas


import re, sys
import os
import logging
import socket
import time
import pickle, pprint

# Helper Methods
from src.Sample import Sample


def loadLipidIndices(lineSplit):
    i = 1
    for lipid in lineSplit:
        if i == len(lineSplit):
            break
        lipid = lineSplit[i].rstrip()
        lipidIndexMap[i-1] = lipid
        lipidIndexRevMap[lipid] = i-1
        print str(i-1)+"," + lipid
        i=i+1

def loadSamples(lineSplit):
    i = 0
    for item in lineSplit:
        if i == 0:
            S = Sample(item)
            Samples.append(S)
            print "Creating "+ S.toStr()
        else:
            S.addLipid(float(item))
        i=i+1
    print S.toStr()

def loadThymus():
    if not os.path.exists(thymusFile):
        print "Thymus File not Found!!!"
        return 1
    thymus = open(thymusFile, "r")
    firstLine = True
    for line in thymus.readlines():
        lineSplit = line.split(",")
        if firstLine:
            loadLipidIndices(lineSplit)
            firstLine = False
        else :
            loadSamples(lineSplit)
    thymus.close()
    pass

def processNormal():
    if not os.path.exists(normalFile):
        print "Normal File not Found!!!"
        return 1
    normal = open(normalFile, "r")
    firstLine = True
    for line in normal.readlines():
        if firstLine:
            firstLine = False
            continue
        lineSplit = line.split(",")
        lipid = lineSplit[0]
        std = lineSplit[1]
        concentration = float(lineSplit[2])
        print lipid
        lipidIndex = lipidIndexRevMap[lipid]
        stdIndex = lipidIndexRevMap[std]

        for s in Samples:
            s.calcNormal(lipidIndex, stdIndex, concentration)
        normal.close()
    pass


def exportNormalized():
    normalized = open("Output.csv", "w")

    for s in Samples:
        line = s.getName()+","
        normalVals = s.getNormal()
        for n in normalVals:
            line = line + str(n)+","
        normalized.write(line+"\n")
        s.testPlot()
        break
    normalized.close()
    pass

# Start Main

if 4 > len(sys.argv):
    print 'Usage : maAnalyze <Thymus File> <Normal File> <Command Start/Stop/etc>'
    sys.exit(1)

# Initialize some basic parameter files
thymusFile = str(sys.argv[1])
normalFile = str(sys.argv[2])
command = str(sys.argv[3])
lipidIndexMap = {}
lipidIndexRevMap = {}
Samples = []
if command.lower() == 'start':
    loadThymus()
    print str(lipidIndexRevMap)
    processNormal()
    exportNormalized()
