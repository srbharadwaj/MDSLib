from .connection_manager.errors import CLIError
from .fc import Fc
from .portchannel import PortChannel
from .nxapikeys import vsankeys
from .constants import PAT_FC, PAT_PC
import re

import logging

log = logging.getLogger(__name__)


class VsanNotPresent(Exception):
    """

    """

    def __init__(self, message):
        """

        Args:
            message:
        """
        self.message = message.strip()

    def __repr__(self):
        """

        Returns:

        """
        return '%s: %s' % (self.__class__.__name__, self.message)

    __str__ = __repr__


class InvalidInterface(Exception):
    """

    """

    def __init__(self, message):
        """

        Args:
            message:
        """
        self.message = message.strip()

    def __repr__(self):
        """

        Returns:

        """
        return '%s: %s' % (self.__class__.__name__, self.message)

    __str__ = __repr__


class Vsan(object):
    def __init__(self, switch, id):
        self.__swobj = switch
        self._id = id

    @property
    def id(self):
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        vid = out[vsankeys.VSAN_ID]
        if type(vid) is str:
            return int(vid)
        else:
            return vid

    @property
    def name(self):
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        if out:
            return out.get(vsankeys.VSAN_NAME)
        return None

    @name.setter
    def name(self, name):
        self.create(name)

    @property
    def state(self):
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        if out:
            return out.get(vsankeys.VSAN_STATE)
        return None

    @property
    def interfaces(self):
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        cmd = "show vsan " + str(self._id) + " membership"
        out = self.__swobj.show(cmd)
        out = out['TABLE_vsan_membership']['ROW_vsan_membership']
        log.debug(out)
        allint = out.get('interfaces', None)
        if allint is None:
            return None
        else:
            retelements = []
            if type(allint) is str:
                allintnames = [allint]
            else:
                allintnames = allint
            for eachintname in allintnames:
                fcmatch = re.match(PAT_FC, eachintname)
                pcmatch = re.match(PAT_PC, eachintname)
                if fcmatch:
                    intobj = Fc(switch=self.__swobj, name=eachintname)
                elif pcmatch:
                    id = pcmatch.group(1)
                    intobj = PortChannel(switch=self.__swobj, id=int(id))
                else:
                    log.error(
                        "Unsupported interface " + eachintname + " , hence skipping it, this type of interface is not supported yet")
                retelements.append(intobj)
            return retelements

    # property for suspend
    def _set_suspend(self, value):
        cmd = "vsan database ; "
        if value:
            cmd = cmd + "vsan " + str(self._id) + " suspend"
        else:
            cmd = cmd + "no vsan " + str(self._id) + " suspend"

        self.__swobj.config(cmd)

    # suspend property
    suspend = property(fset=_set_suspend)

    def create(self, name=None):
        cmd = "vsan database ; vsan " + str(self._id)
        if name is not None:
            cmd = cmd + " name '" + name + "'"
        self.__swobj.config(cmd)

    def delete(self):
        try:
            cmd = "terminal dont-ask ; " \
                  "vsan database ; " \
                  "no vsan " + str(self._id)
            self.__swobj.config(cmd)
        except CLIError as c:
            cmddontask = "no terminal dont-ask"
            self.__swobj.config(cmddontask)
            log.error(c)
            raise CLIError(cmd, c.message)
        finally:
            cmd = "no terminal dont-ask"
            self.__swobj.config(cmd)

    def add_interfaces(self, interfaces):
        if self.id is None:
            raise VsanNotPresent("Vsan " + str(self._id) + " is not present on the switch.")
        else:
            cmdlist = []
            for eachint in interfaces:
                fcmatch = re.match(PAT_FC, eachint.name)
                pcmatch = re.match(PAT_PC, eachint.name)
                if fcmatch or pcmatch:
                    cmd = "vsan database ; vsan " + str(self._id) + " interface " + eachint.name
                    cmdlist.append(cmd)
                else:
                    raise InvalidInterface("Interface " + str(eachint.name) +
                                           " is not supported, and hence cannot be added to the vsan, "
                                           "supported interface types are 'fc' amd 'port-channel'")
            try:
                self.__swobj.config_list(cmdlist)
            except CLIError as c:
                if "membership being configured is already configured for the interface" in c.message:
                    return False, None
                log.error(c)
                raise CLIError(cmd, c.message)

    def __get_facts(self):
        shvsan = self.__swobj.show("show vsan")

        listofvsaninfo = shvsan["TABLE_vsan"]["ROW_vsan"]
        vsanlist = []
        for eachv in listofvsaninfo:
            vsanlist.append(str(eachv[vsankeys.VSAN_ID]))
        if str(self._id) not in vsanlist:
            raise VsanNotPresent("Vsan " + str(self._id) + " is not present on the switch.")

        shvsan_req_out = {}

        # Parse show vsan json output
        for eachele in listofvsaninfo:
            if str(eachele[vsankeys.VSAN_ID]) == str(self._id):
                shvsan_req_out = eachele
                break
        if not shvsan_req_out:
            log.debug("No info for vsan " + str(self._id))
            return None

        return dict(shvsan_req_out)

# TODO: Check vsan range during create/delete/addinterface etc..
# TODO: Interfaces
