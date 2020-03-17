import logging
import re

from .constants import PAT_PC, PAT_FC
from .nxapikeys import interfacekeys

log = logging.getLogger(__name__)


class Interface(object):
    """
    Interface module

    :param switch: switch object on which vsan operations need to be executed
    :type switch: Switch
    :param name: name of the interface
    :type name: str

    .. warning:: Interface class is a Base class and cannot be instantiated, please use specific interface classes(Child/Derived class)
                like Fc,PortChannel etc.. to instantiate
    """

    def __init__(self, switch, name):
        self.__swobj = switch
        self._name = name

    # Interface is the base class for Fc and PortChannel.
    # So you cannot instantiate the base class(Interface), you have to instantiate the derived/child class (Fc,PortChannel)
    def __new__(cls, *args, **kwargs):
        if cls is Interface:
            raise TypeError(
                "Interface class is a Base class and cannot be instantiated, "
                "please use specific interface classes(Child/Derived class) like Fc,PortChannel etc.. to instantiate")
        return object.__new__(cls)

    @property
    def name(self):
        """

        :return:
        """
        return self._name

    @property
    def description(self):
        """
        Get the description of the interface
        :rtype: object
        :return: 
        """
        out = self.__swobj.show("show interface  " + self._name + " description")
        desc = out['TABLE_interface']['ROW_interface']['description']
        # IF the string is a big one then the return element is of type list
        if type(desc) is list:
            retval = ''.join(desc)
        else:
            retval = desc
        return retval

    @description.setter
    def description(self, value):
        """
        Set the description of the interface
        :param str value: Description string
        """
        cmd = "interface " + self._name + " ; switchport description  " + value
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
        cmd = "interface " + self._name + " ; switchport mode  " + value
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
        cmd = "interface " + self._name + " ; switchport speed  " + str(value)
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def trunk(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_ADMIN_TRUNK_MODE]
        return None

    @trunk.setter
    def trunk(self, value):
        cmd = "interface " + self._name + " ; switchport trunk mode  " + value
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def status(self):
        out = self.__parse_show_int_brief()
        if out is not None:
            return out[interfacekeys.INT_STATUS]
        return None

    @status.setter
    def status(self, value):
        cmd = "terminal dont-ask ; interface " + self._name + " ; " + value + " ; no terminal dont-ask "
        log.debug("Sending the cmd: " + cmd)
        out = self.__swobj.config(cmd)

    @property
    def counters(self):
        return self.Counters(self)

    def __parse_show_int_brief(self):
        log.debug("Getting sh int brief output")
        out = self.__swobj.show("show interface brief ")
        log.debug(out)
        # print(out)
        fcmatch = re.match(PAT_FC, self._name)
        pcmatch = re.match(PAT_PC, self._name)
        if fcmatch:
            out = out['TABLE_interface_brief_fc']['ROW_interface_brief_fc']
            for eachout in out:
                if eachout[interfacekeys.INTERFACE] == self._name:
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
                if eachout[interfacekeys.INTERFACE] == self._name:
                    return eachout
        return None

    def _execute_counters_detailed_cmd(self):
        cmd = "show interface " + self._name + " counters detailed"
        log.debug("Sending the cmd")
        log.debug(cmd)
        out = self.__swobj.config(cmd)
        return out['body']

    class Counters(object):
        def __init__(self, intobj):
            self.__intobj = intobj

        @property
        def brief(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            allkeys = list(out.keys())
            for k in allkeys:
                if k.startswith('TABLE'):
                    out.pop(k)
                if k.startswith('interface'):
                    out.pop(k)
            return out

        @property
        def total_stats(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            z = out['TABLE_counters']['ROW_counters']
            for k, v in z.items():
                if 'total' in k:
                    print(k, v)
            total = out.get('TABLE_total', None)
            if total is not None:
                return total.get('ROW_total', None)
            return None

        @property
        def link_stats(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_link', None)
            if total is not None:
                return total.get('ROW_link', None)
            return None

        @property
        def loop_stats(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_loop', None)
            if total is not None:
                return total.get('ROW_loop', None)
            return None

        @property
        def congestion_stats(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_congestion', None)
            if total is not None:
                return total.get('ROW_congestion', None)
            return None

        @property
        def other_stats(self):
            out = self.__intobj._execute_counters_detailed_cmd()
            total = out.get('TABLE_others', None)
            if total is not None:
                return total.get('ROW_others', None)
            return None
