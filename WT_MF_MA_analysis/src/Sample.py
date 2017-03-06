#!/usr/bin/env python


# Sample
# Maintains Data for each Sample in a Batch (Run)

__author__      = "Pravein Govindan Kannan"
__copyright__   = "Copyright 2017, NUS"

import sys
import matplotlib.pyplot as plt

class Sample:

    def __init__(self, name):
        self.name = name
        self.lipids = {}
        self.normalizedToIS = {}
        self.lipidAbundance = {}
        self.lipidSum = 0

    def addLipid(self, lipidName, lipidVal):
        self.lipids[lipidName] = lipidVal

    def getLipidVal(self, lipidName):
        return self.lipids[lipidName]

    def toStr(self):
        return self.name +" : "+ str(self.lipids)

    def getName(self):
        return self.name

    def calcNormal(self, lipid1, lipid2, concetration):
        l1Val = self.lipids[lipid1]
        l2Val = self.lipids[lipid2]
        if l2Val == 0 :
            self.normalizedToIS[lipid1] = 0
            return
        normalized = float((l1Val/l2Val) * concetration)
        self.normalizedToIS[lipid1] = normalized
        #print "Normalized " + str(normalized)
        pass

    def getName(self):
        return self.name

    def getNormal(self):
        return self.normalizedToIS

    def getNormalHeading(self, lipidIndexMap):
        line = ""
        for i in range(0,len(lipidIndexMap)):
        #for l in self.normalizedToIS.iterkeys():
            line += lipidIndexMap[i]+","
        return line

    def calcLipidAbundance(self, lipidIndicator):
        for lipid  in lipidIndicator:
            if lipidIndicator[lipid] == 1 :
                self.lipidSum += self.normalizedToIS[lipid]
        for lipid in lipidIndicator:
            if lipidIndicator[lipid] == 1:
                self.lipidAbundance[lipid] = (self.normalizedToIS[lipid] / self.lipidSum) * 100

    def getLipidAbundance(self):
        return self.lipidAbundance


    def testPlot(self):
        lists = sorted(self.normalizedToIS.items())
        x, y = zip(*lists)
        plt.plot(x, y)
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.savefig('../test.pdf', bbox_inches='tight' )
