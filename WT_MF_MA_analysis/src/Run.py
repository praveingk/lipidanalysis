#!/usr/bin/env python


# Run
# Pravein, 2017
# Class for storing data of different runs. Each run will have similar structured data. AKA Batch

__author__      = "Pravein Govindan Kannan"
__copyright__   = "Copyright 2017, NUS"

import sys,os
import numpy as np
from Sample import Sample
from scipy import stats


import plotly.plotly as py
import plotly.graph_objs as go


class Run:

    def __init__(self, name):
        self.name = name
        self.lipidIndexMap = {}
        self.lipidIndexRevMap = {}
        self.Samples = []
        self.lipidIndicator = {}
        self.qualityLipids = {}
        self.qualifiedLipids = []
        self.filterSamples = []
        self.sampleFilter = ""
        self.qualityCheck = "QC"

    def setSampleFiler(self, sampleFilter):
        self.sampleFilter = sampleFilter

    def loadLipidIndices(self, lineSplit):
        i = 1
        for lipid in lineSplit:
            if i == len(lineSplit):
                break
            lipid = lineSplit[i].rstrip()
            self.lipidIndexMap[i - 1] = lipid
            self.lipidIndexRevMap[lipid] = i - 1
            #print str(i - 1) + "," + lipid
            i = i + 1

    def loadSamples(self, lineSplit):
        i = 0
        for item in lineSplit:
            if i == 0:
                S = Sample(item)
                self.Samples.append(S)
                #print "Creating " + S.toStr()
            else:
                S.addLipid(self.lipidIndexMap[i-1], float(item))
            i = i + 1
        #print S.toStr()

    def loadRun(self, runFile):
        if not os.path.exists(runFile):
            print "Run File not Found!!!"
            return 1
        runF = open(runFile, "r")
        firstLine = True
        for line in runF.readlines():
            lineSplit = line.split(",")
            if firstLine:
                self.loadLipidIndices(lineSplit)
                firstLine = False
            else:
                self.loadSamples(lineSplit)
        runF.close()
        pass

    def processNormal(self, normalFile):
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
            abundance = int(lineSplit[3])
            #print lipid
            lipidIndex = self.lipidIndexRevMap[lipid]
            stdIndex = self.lipidIndexRevMap[std]
            self.lipidIndicator[lipid] = abundance
            for s in self.Samples:
                s.calcNormal(lipid, std, concentration)
            normal.close()
        pass

    def exportNormalized(self, outputFile ):
        normalized = open(outputFile, "w")
        firstTime = True

        for s in self.Samples:
            if firstTime == True:
                firstTime = False
                line = "Sample, " + s.getNormalHeading(self.lipidIndexMap)
                normalized.write(line + "\n")
            line = s.getName() + ","
            normalLipids = s.getNormal()
            for i in range(0, len(self.lipidIndexMap)):
                line = line + str(normalLipids[self.lipidIndexMap[i]]) + ","
            normalized.write(line + "\n")
        normalized.close()
        pass
    def calcLipidAbundance(self):
        for s in self.Samples:
            s.calcLipidAbundance(self.lipidIndicator)
        pass

    def exportLipidAbundance(self, outputFile):
        abundance = open(outputFile,"w")
        line = "Sample, "
        for i in range(0, len(self.lipidIndexMap)):
            if self.lipidIndicator[self.lipidIndexMap[i]] == 1:
                line = line + self.lipidIndexMap[i]+","
        abundance.write(line + "\n")
        for s in self.Samples:
            line = s.getName() + ","
            labun = s.getLipidAbundance()
            for i in range(0, len(self.lipidIndexMap)):
                if self.lipidIndicator[self.lipidIndexMap[i]] == 1:
                    line = line + str(labun[self.lipidIndexMap[i]]) +","
            abundance.write(line +"\n")
        abundance.close()

    def performQualityCheck(self):
        for i in range(0, len(self.lipidIndexMap)):
            lipid = self.lipidIndexMap[i]
            if self.lipidIndicator[lipid] == 0:
                continue
            lipidVals = []
            for s in self.Samples:
                normal = s.getNormal()
                if self.qualityCheck in s.getName():
                    lipidVals.append(normal[lipid])
            #print lipidVals
            std  = np.std(lipidVals)
            avg = np.mean(lipidVals)
            #print std
            #print avg
            variance = 100
            if avg != 0:
                variance = (std/avg) * 100

            #print variance
            if variance < 20 :
                self.qualityLipids[lipid] = 1
                self.qualifiedLipids.append(lipid)
            else :
                self.qualityLipids[lipid] = 0

        print "Quality Analysis :" + str(self.qualityLipids)

    def exportLipidAbundance(self, outputFile):
        abundance = open(outputFile,"w")
        line = "Sample, "
        for i in range(0, len(self.lipidIndexMap)):
            if self.lipidIndicator[self.lipidIndexMap[i]] == 1:
                line = line + self.lipidIndexMap[i]+","
        abundance.write(line + "\n")
        for s in self.Samples:
            line = s.getName() + ","
            labun = s.getLipidAbundance()
            for i in range(0, len(self.lipidIndexMap)):
                if self.lipidIndicator[self.lipidIndexMap[i]] == 1:
                    line = line + str(labun[self.lipidIndexMap[i]]) +","
            abundance.write(line +"\n")
        abundance.close()

    def exportLipidAbundanceQC(self, outputFile):
        abundance = open(outputFile,"w")
        line = "Sample, "
        for i in range(0, len(self.lipidIndexMap)):
            lipid = self.lipidIndexMap[i]
            if self.lipidIndicator[lipid] == 0:
                continue
            if self.qualityLipids[lipid] == 1:
                line = line + lipid+","
        abundance.write(line + "\n")
        for s in self.Samples:
            line = s.getName() + ","
            labun = s.getLipidAbundance()
            for i in range(0, len(self.lipidIndexMap)):
                lipid = self.lipidIndexMap[i]
                if self.lipidIndicator[lipid] == 0:
                    continue
                if self.qualityLipids[lipid] == 1 :
                    line = line + str(labun[lipid]) +","
            abundance.write(line +"\n")
        abundance.close()

    #This may change as per spec
    def filterSampleNames(self):
        filteredSamples = []
        for s in self.Samples:
            if self.sampleFilter in s.getName():
                filteredSamples.append(s.getName())
                self.filterSamples.append(s)
        return filteredSamples

    def getHeatMapLipidvsSamples(self, outputFile):
        sortedLipids = sorted(self.qualifiedLipids)
        #print sortedLipids
        #x = sortedLipids
        samples =  self.filterSampleNames()

        #print samples

        lipidVals = []
        for lipid in sortedLipids:
            lipidinternal = []
            for s in self.filterSamples:
                labun = s.getLipidAbundance()
                lipidinternal.append(labun[lipid])
            zscoreLipids = stats.zscore(lipidinternal)

            #print lipidinternal
            #print zscoreLipids

            lipidVals.append(zscoreLipids)

        #print lipidVals
        #
        # print len(lipidVals)
        # print len(self.filterSamples)
        # for lp in lipidVals:
        #     print len(lp)
        # print len(sortedLipids)
        data = [
            go.Heatmap(
                z=lipidVals,
                y=sortedLipids,
                x=samples
            )
        ]

        layout = go.Layout(
            autosize=False,
            width=1500,
            height=1500,
            margin=go.Margin(
                l=180,
                r=180,
                b=180,
                t=100,
                pad=4
            ),
        )
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename=outputFile, auto_open=False)