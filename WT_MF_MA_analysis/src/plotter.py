#!/usr/local/bin/python


# plotter.py
# Combination of various plots

__author__      = "Pravein Govindan Kannan"
__copyright__   = "Copyright 2017, NUS"


import re, sys
import os
import logging
import socket
import time
import pickle, pprint

# Helper Methods
from Run import Run
import Sample
import re

# Create HeatMap
def createHeatMap(runFile, i):
    run = Run(runFile)
    run.loadRun(runFile)
    fileOP = re.split("/", runFile)
    file = fileOP[len(fileOP)-1]
    fileName = file.split(".")
    print runFile
    print fileName[0]
    run.createHeatMapRaw("HeatMap_"+fileName[0])


# Start Main

if 1 > len(sys.argv):
    print 'Usage : plotter <Input Files>  <Command heatmap/etc>'
    print "Input Files : \n" \
          " RunFile.csv,\n" \
          "...\n" \
          "...\n"
    sys.exit(1)
# Initialize some basic parameter files
inputFile = str(sys.argv[1])
command = str(sys.argv[2])



if command.lower() == 'heatmap':
    inF = open(inputFile, "r")
    batch = 1
    i = 1
    for line in inF.readlines():
        lineSplit = line.split(",")
        runFile = lineSplit[0].rstrip()
        createHeatMap(runFile, i)
        i+=1