#!/usr/local/bin/python


# maAnalyze.py
# Analysis of Mouse Atlas

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



# Start Main

if 4 > len(sys.argv):
    print 'Usage : maAnalyze <Input Files> <Output Directory> <Command Start/Stop/etc>'
    print "Input Files : \n" \
          " RunFile.csv, normalFile.csv\n" \
          "...\n" \
          "...\n"
    sys.exit(1)

# Initialize some basic parameter files
inputFile = str(sys.argv[1])
outputDir = str(sys.argv[2])
command = str(sys.argv[3])
print command
if command.lower() == 'start':
    inF = open(inputFile, "r")
    batch = 1
    for line in inF.readlines():
        lineSplit = line.split(",")
        runFile = lineSplit[0].rstrip()
        normalFile = lineSplit[1].rstrip()
        # Do this repeatedly
        run = Run(runFile)
        run.loadRun(runFile)
        print "##################################################"
        print "Processing "+line.rstrip()
        run.processNormal(normalFile)
        run.exportNormalized(outputDir+"/Normalized"+ str(batch)+".csv")
        print "Normalized!"
        run.calcLipidAbundance()
        run.exportLipidAbundance(outputDir+"/abundance"+str(batch)+".csv")
        print "Lipid Relative Abundance Done!"
        run.performQualityCheck()
        run.exportLipidAbundanceQC(outputDir+"/abundanceQC"+str(batch)+".csv")
        print "Quality Check Done!"
        run.getHeatMapLipidvsSamples()
        print "HeatMap Done!"
        print "Visit : https://plot.ly/dashboard/praveingk:6/present"
    print "##################################################"
    pass
elif command.lower() == 'normal':
    inF = open(inputFile, "r")
    batch = 1
    for line in inF.readlines():
        lineSplit = line.split(",")
        runFile = lineSplit[0].rstrip()
        normalFile = lineSplit[1].rstrip()
        # Do this repeatedly
        run = Run(runFile)
        run.loadRun(runFile)
        #print normalFile
        print "Processing "+line.rstrip()
        run.processNormal(normalFile)
        run.exportNormalized(outputDir+"/Normalized"+ str(batch)+".csv")
        print "Normalized!"
    pass