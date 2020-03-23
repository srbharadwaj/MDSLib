import logging
import re

from .connection_manager.errors import CLIError
from .constants import PAT_FC, PAT_PC
from .fc import Fc
from .nxapikeys import vsankeys
from .portchannel import PortChannel
from .utility.allexceptions import VsanNotPresent, InvalidInterface

log = logging.getLogger(__name__)


class Vsan(object):
    """

    Vsan module

    :param switch: switch object on which vsan operations need to be executed
    :type switch: Switch
    :param id: vsan id
    :type id: int

    :example:
        >>> vsan_obj = Vsan(switch=switch_obj, id=2)

    .. warning:: id must be within range 1-4094 (4079,4094 are reserved)

    """

    def __init__(self, switch, id):
        self.__swobj = switch
        self._id = id

    @property
    def id(self):
        """
        Get vsan id

        :return: id of the vsan if vsan is present on the switch, otherwise returns None
        :rtype: int
        :range: 1 to 4094

        """

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
        """
        Get the name of the vsan or
        Set the name of the vsan

        :getter:
        :return: name of the vsan,
                 returns None if vsan is not present on the switch
        :rtype: str
        :example:
            >>> print(vsan_obj.name)
            "VSAN0001"
            >>>

        :setter:
        :param name: name of the vsan
        :type name: str

        :example:
            >>> vsan_obj.name = "vsan_2"

        """

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
        """
        Get the state of the vsan

        :return: state of the vsan
                 returns None if vsan is not present on the switch
        :values: return values are either 'active' or 'suspended'

        """

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
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "vsan database ; "
        if value:
            cmd = cmd + "vsan " + str(self._id) + " suspend"
        else:
            cmd = cmd + "no vsan " + str(self._id) + " suspend"

        self.__swobj.config(cmd)

    # suspend property
    suspend = property(fset=_set_suspend)
    """
    Set the state of the vsan

    :setter:
    :param value: if true suspends the vsan, else does a 'no suspend' 
    :type value: bool
    :raises TypeError: If the passed value is not of type bool

    :example:
        >>> vsan_obj.suspend = True

    """

    def create(self, name=None):
        """
        Creates vsan on the switch

        :param name: name of vsan (optional parameter, defaults to 'VSAN<vsan-id>' if passed as None)
        :type name: str or None
        :return: None

        :example:
            >>> vsan_obj.create("vsan_2")

        """

        cmd = "vsan database ; vsan " + str(self._id)
        if name is not None:
            cmd = cmd + " name '" + name + "'"
        self.__swobj.config(cmd)

    def delete(self):
        """Deletes the vsan on the switch

        :param: None
        :return: None
        :raises VsanNotPresent: if vsan is not present on the switch

        :example:
            >>> vsan_obj.delete()

        """

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
        """Add interfaces to the vsan

        :param interfaces: interfaces to be added to the vsan
        :type interfaces: list(Fc or PortChannel)
        :raises VsanNotPresent: if vsan is not present on the switch
        :raises InvalidInterface: if the interface is not among supported interface types (‘fc’ and ‘port-channel’)
        :raises CLIError: if the switch raises a error for the cli command passed
        :return: None

        :example:
            >>> fc = Fc(switch,"fc1/1")
            >>> pc = PortChannel(switch,1)
            >>> vsan_obj.add_interfaces([fc,pc])
            >>> vsan_obj.add_interfaces(fc)
            Traceback (most recent call last):
            ...
            TypeError: Fc object is not iterable

        """

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
                    return
                else:
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
