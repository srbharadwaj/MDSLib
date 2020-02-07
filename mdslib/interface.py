from .nxapikeys import interfacekeys
from .constants import *
import logging
import re

log = logging.getLogger(__name__)

VALID_STATUS = [SHUTDOWN, NO_SHUTDOWN]
VALID_TRUNK_MODE = [AUTO, ON, OFF]
VALID_SPEED = [AUTO, 1000, 2000, 4000, 8000, 16000, 32000]
VALID_MODE = [AUTO, 'E', 'F', 'NP']


class InvalidStatus(Exception):
    def __init__(self, value):
        Exception.__init__(self, "Invalid status (" + str(value) + "), status must be one of (" + ', '.join(
            VALID_STATUS) + ")")


class InvalidTrunkMode(Exception):
    def __init__(self, value):
        Exception.__init__(self, "Invalid trunk mode (" + str(value) + "), trunk mode must be one of (" + ', '.join(
            VALID_TRUNK_MODE) + ")")


class InvalidSpeed(Exception):
    def __init__(self, value):
        Exception.__init__(self,
                           "Invalid speed (" + str(value) + "), speed must be one of (" + ', '.join(
                               str(x) for x in VALID_SPEED) + ")")


class InvalidMode(Exception):
    def __init__(self, value):
        Exception.__init__(self,
                           "Invalid mode (" + str(value) + "), mode must be one of (" + ', '.join(VALID_MODE) + ")")


class Interface(object):
    def __init__(self, switch, name):
        self.__swobj = switch
        self.name = name

    def __new__(cls, *args, **kwargs):
        if cls is Interface:
            raise TypeError(
                "Interface class(Base class) cannot be instantiated, please use specific interface classes(Child class) like Fc,PortChannel etc..")
        return object.__new__(cls)

    @property
    def description(self):
        out = self.__swobj.show("show interface  " + self.name + " description")
        desc = out['TABLE_interface']['ROW_interface']['description']
        return desc

    @description.setter
    def description(self, value):
        cmd = "interface " + self.name + " ; switchport description  " + value
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)
        log.debug(out)

    @property
    def mode(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_OPER_MODE]
        return None

    @mode.setter
    def mode(self, value):
        if value not in VALID_MODE:
            raise InvalidMode(value)
        else:
            cmd = "interface " + self.name + " ; switchport mode  " + value
            log.debug("Sending the cmd: " + cmd)
            out = self.__swobj.config(cmd)
            log.debug(out)

    @property
    def speed(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_OPER_SPEED]
        return None

    @speed.setter
    def speed(self, value):
        if value not in VALID_SPEED:
            raise InvalidSpeed(value)
        else:
            cmd = "interface " + self.name + " ; switchport speed  " + str(value)
            log.debug("Sending the cmd: " + cmd)
            out = self.__swobj.config(cmd)
            # print(out)

    @property
    def trunk(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_ADMIN_TRUNK_MODE]
        return None

    @trunk.setter
    def trunk(self, value):
        if value not in VALID_TRUNK_MODE:
            raise InvalidTrunkMode(value)
        else:
            cmd = "interface " + self.name + " ; switchport trunk mode  " + value
            log.debug("Sending the cmd: " + cmd)
            out = self.__swobj.config(cmd)
            # print(out)

    @property
    def status(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_STATUS]
        return None

    @status.setter
    def status(self, value):
        if value not in VALID_STATUS:
            raise InvalidStatus(value)
        else:
            cmd = "interface " + self.name + " ; " + value
            log.debug("Sending the cmd: " + cmd)
            out = self.__swobj.config(cmd)
            # print(out)

    @property
    def counters(self):
        cmd = "show interface " + self.name + " counters brief"
        out = self.__swobj.show(cmd)
        log.debug(out)
        briefoutput = out['TABLE_counters_brief']['ROW_counters_brief']
        # print(briefoutput)
        cmd = "show interface " + self.name + " counters detail"
        out = self.__swobj.show(cmd)
        log.debug(out)
        # detailoutput = out['TABLE_ifid_counters']['ROW_ifid_counters']
        detailoutput = out
        # print(detailoutput)
        concatoutput = {**briefoutput, **detailoutput}
        concatoutput.pop(interfacekeys.INTERFACE)
        # print(concatoutput)
        return concatoutput

    def __parse_show_int_brief(self):
        log.debug("Getting sh int brief output")
        out = self.__swobj.show("show interface brief ")
        log.debug(out)
        # print(out)
        fcmatch = re.match(PAT_FC, self.name)
        pcmatch = re.match(PAT_PC, self.name)
        if fcmatch:
            out = out['TABLE_interface_brief_fc']['ROW_interface_brief_fc']
            for eachout in out:
                if eachout[interfacekeys.INTERFACE] == self.name:
                    return eachout
        elif pcmatch:
            # Need to check if "sh int brief" has PC info
            pcinfo = out.get('TABLE_interface_brief_portchannel', None)
            if pcinfo is None:
                return None
            out = pcinfo['ROW_interface_brief_portchannel']
            if type(out) is dict:
                outlist = [out]
            else:
                outlist = out
            for eachout in outlist:
                if eachout[interfacekeys.INTERFACE] == self.name:
                    return eachout
        return None
