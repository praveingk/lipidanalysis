#!/usr/bin/env python


# Lipid

import sys



class Lipid:

    def __init__(self, port1, port2):
        self.vPorts = []
        self.pSwitchPorts = []
        self.vPorts.append(port1)
        self.vPorts.append(port2)
