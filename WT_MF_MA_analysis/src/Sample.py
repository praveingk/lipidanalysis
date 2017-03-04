#!/usr/bin/env python


# Sample

import sys



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
        print "Normalized " + str(normalized)
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

    def calcRelAbundance(self, lipidIndicator):
        for lipid  in lipidIndicator:
            if lipidIndicator[lipid] == 1 :
                self.lipidSum += self.lipids[lipid]
        for lipid in lipidIndicator:
            if lipidIndicator[lipid] == 1:
                self.lipidAbundance[lipid] = (self.lipids[lipid] / self.lipidSum) * 100

    def getLipidAbundance(self):
        return self.lipidAbundance


