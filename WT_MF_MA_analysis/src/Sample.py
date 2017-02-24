#!/usr/bin/env python


# Sample

import sys



class Sample:

    def __init__(self, name):
        self.name = name
        self.lipids = []
        self.normalizedToIS = {}

    def addLipid(self, lipidVal):
        self.lipids.append(lipidVal)

    def getLipidVal(self, index):
        return self.lipids[index]

    def toStr(self):
        return self.name +" : "+ str(self.lipids)

    def calcNormal(self, lipid1Index, lipid2Index, concetration):
        l1Val = self.lipids[lipid1Index]
        l2Val = self.lipids[lipid2Index]
        if l2Val == 0 :
            self.normalizedToIS[lipid1Index] = 0
            return
        normalized = float((l1Val/l2Val) * concetration)
        self.normalizedToIS[lipid1Index] = normalized
        print "Normalized " + str(normalized)
        pass

    def getName(self):
        return self.name

    def getNormal(self):
        return self.normalizedToIS.itervalues()