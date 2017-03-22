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
        weightFile = lineSplit[2].rstrip()
        fileOP = re.split("/", runFile)
        file = fileOP[len(fileOP) - 1]
        runF = file.split(".")[0]
        sampleFilter = ""
        if (len(lineSplit) > 3) :
            sampleFilter = lineSplit[3].rstrip()

        # Do this repeatedly
        run = Run(runFile)
        run.loadRun(runFile)
        run.setSampleFiler(sampleFilter)
        print "##################################################"
        print "Processing "+line.rstrip()
        run.processNormal(normalFile)
        run.exportNormalized(outputDir+"/Normalized_"+ runF+".csv")
        print "Normalized!"
        run.processWeights(weightFile)
        run.exportLipidWeightNormalization(outputDir+"/WeightNormalized_"+ runF+".csv")
        print "Weight Normalization Done!"
        run.calcLipidAbundance()
        run.exportLipidAbundance(outputDir+"/Abundance_"+runF+".csv")
        print "Lipid Relative Abundance Done!"

        run.performQualityCheck()
        print "Quality Check Done!"
        run.exportLipidAbundanceQC(outputDir+"/AbundanceQC_"+runF+".csv")


        run.exportLipidWeightNormalizationQC(outputDir+"/WeightNormalizedQC_"+runF+".csv")
        #run.getHeatMapLipidvsSamples("HeatMap_Batch"+ str(batch)+"_"+str(time.ctime()))
        #print "HeatMap Done!"
        #print "Visit : https://plot.ly/ to your account to view the results!!"
    print "##################################################"
    pass
elif command.lower() == 'normal':
    inF = open(inputFile, "r")
    batch = 1
    for line in inF.readlines():
        lineSplit = line.split(",")
        runFile = lineSplit[0].rstrip()
        normalFile = lineSplit[1].rstrip()

        fileOP = re.split("/", runFile)
        file = fileOP[len(fileOP) - 1]
        runF = file.split(".")[0]
        # Do this repeatedly
        run = Run(runFile)
        run.loadRun(runFile)
        #print normalFile
        print "Processing "+line.rstrip()
        run.processNormal(normalFile)
        run.exportNormalized(outputDir+"/Normalized"+ runF+".csv")
        print "Normalized!"
    pass