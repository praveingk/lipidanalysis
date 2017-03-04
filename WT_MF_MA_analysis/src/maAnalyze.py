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
from src.Run import Run
from src.Sample import Sample





# Start Main

if 4 > len(sys.argv):
    print 'Usage : maAnalyze <Input Files> <Output Directory> <Command Start/Stop/etc>'
    print "Input Files : \n" \
          " RunFile.csv, normalFile.csv\n" \
          "...\n" \
          "...\n"
    print 'Usage : maAnalyze <Run Files> <Normal File> <Command Start/Stop/etc>'
    sys.exit(1)

# Initialize some basic parameter files
inputFile = str(sys.argv[1])
outputDir = str(sys.argv[2])
command = str(sys.argv[3])
print command
if command.lower() == 'start':
    inF = open(inputFile, "r")
    for line in inF.readlines():
        lineSplit = line.split(",")
        runFile = lineSplit[0]
        normalFile = lineSplit[1]
        # Do this repeatedly
        run = Run(runFile)
        run.loadRun(runFile)
        run.processNormal(normalFile)
        run.exportNormalized(outputDir+"/putput.csv")
        run.calcRelAbundance()
        run.exportLipidAbundance(outputDir+"/abundance.csv")
