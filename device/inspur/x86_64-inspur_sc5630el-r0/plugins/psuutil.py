#!/usr/bin/env python
#
# psuutil.py
#
# Platform-specific PSU utility for SONiC
#


# ----------------------------------------------------------------------------
# import modules
# ----------------------------------------------------------------------------
import os.path

try:
    from sonic_psu.psu_base import PsuBase
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")


# ----------------------------------------------------------------------------
# Class declaration
# ----------------------------------------------------------------------------
class PsuUtil(PsuBase):
    """Platform-specific PSUutil class"""

    def __init__(self):
        PsuBase.__init__(self)

        self.psu_path = "/sys/bus/i2c/devices/"
        self.psu_presence = {
            1: "/psu1_present",
            2: "/psu2_present",
        }
        self.psu_oper_status = {
            1: "/psu1_power_good",
            2: "/psu2_power_good",
        }
        self.psu_mapping = "101-0068"

    def get_num_psus(self):
        return len(self.psu_presence)

    def get_psu_status(self, index):
        if index is None:
            return False

        status = 0
        node = self.psu_path + self.psu_mapping+self.psu_oper_status[index]
        try:
            with open(node, 'r') as power_status:
                status = int(power_status.read())
        except IOError:
            return False

        return status == 1

    def get_psu_presence(self, index):
        if index is None:
            return False

        status = 0
        node = self.psu_path + self.psu_mapping + self.psu_presence[index]
        try:
            with open(node, 'r') as presence_status:
                status = int(presence_status.read())
        except IOError:
            return False
        
        if status == 0:
            status = 1
        else:
            status = 0


        return status == 1
