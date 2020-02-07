from .interface import Interface
from .constants import ON,ACTIVE, PAT_FC, PAT_PC, VALID_PC_RANGE
from .fc import Fc
from .nxapikeys import portchanelkeys
import logging
import re

log = logging.getLogger(__name__)


class InvalidChannelMode(Exception):
    def __init__(self, value):
        Exception.__init__(self, "Invalid channel mode (" + str(value) + "), Valid values are: " + ON + "," + ACTIVE)


class PortChannelNotPresent(Exception):
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


class InvalidPortChannelRange(Exception):
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


class PortChannel(Interface):
    def __init__(self, switch, id):
        if id not in VALID_PC_RANGE:
            raise InvalidPortChannelRange("Port channel id " + str(id) + " is invalid, id should range from " + str(
                VALID_PC_RANGE[0]) + " to " + str(VALID_PC_RANGE[-1]))
        self._id = id
        name = "port-channel" + str(self._id)
        super().__init__(switch, name)
        self.__swobj = switch

    @property
    def id(self):
        return self._id

    @property
    def channel_mode(self):
        if not self.__is_pc_present():
            return None
        detailout = self.__get_pc_facts()
        self.__admin_ch_mode = detailout[portchanelkeys.ADMIN_CHN_MODE]
        memdetail = detailout.get('TABLE_port_channel_member_detail', None)
        if memdetail is None:
            return self.__admin_ch_mode
        else:
            allmem = memdetail['ROW_port_channel_member_detail']
            if type(allmem) is dict:
                # it means there is only one port member in the port-channel
                return allmem[portchanelkeys.OPER_CHN_MODE]
            else:
                # it means there is more than one member in the port-channel
                # get the one of the member in the port-channel and return its channel mode
                onemem = allmem[0]
                return onemem[portchanelkeys.OPER_CHN_MODE]

    @channel_mode.setter
    def channel_mode(self, mode):
        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel " + str(self._id) + " is not present on the switch, please create the PC first")
        mode = mode.lower()
        cmd = "interface port-channel " + str(self._id)
        if mode == ACTIVE:
            cmd = cmd + " ; channel mode active"
        elif mode == ON:
            cmd = cmd + " ; no channel mode active"
        else:
            raise InvalidChannelMode(mode)
        self.__swobj.config(cmd)

    @property
    def members(self):
        if not self.__is_pc_present():
            return None
        detailout = self.__get_pc_facts()
        memdetail = detailout.get('TABLE_port_channel_member_detail', None)
        if memdetail is None:
            return None
        else:
            allintnames = []
            allmem = memdetail['ROW_port_channel_member_detail']
            if type(allmem) is dict:
                # it means there is only one port member in the port-channel
                allintnames.append(allmem[portchanelkeys.PORT])
            else:
                # it means there is more than one member in the port-channel
                # get the one of the member in the port-channel and return its channel mode
                for eachmem in allmem:
                    allintnames.append(eachmem[portchanelkeys.PORT])
        retelements = []
        for eachintname in allintnames:
            fcmatch = re.match(PAT_FC, eachintname)
            if fcmatch:
                intobj = Fc(switch=self.__swobj, name=eachintname)
                retelements.append(intobj)
            else:
                log.error(
                    "Unsupported interface " + eachintname + " , hence skipping it, this type of interface is not supported yet")

        return retelements

    def create(self):
        cmd = "interface port-channel " + str(self._id)
        self.__swobj.config(cmd)

    def delete(self):
        if self.__is_pc_present():
            cmd = "no interface port-channel " + str(self._id)
            self.__swobj.config(cmd)

    def add_members(self, interfaces):
        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel " + str(self._id) + " is not present on the switch, please create the PC first")

        for eachint in interfaces:
            cmd = "interface " + eachint.name + " ; channel-group " + str(self._id) + " force "
            out = self.__swobj.config(cmd)

    def remove_members(self, interfaces):
        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel " + str(self._id) + " is not present on the switch, please create the PC first")

        for eachint in interfaces:
            cmd = "interface " + eachint.name + " ; no channel-group " + str(self._id)
            out = self.__swobj.config(cmd)

    def __get_pc_facts(self):
        cmd = "show port-channel database detail interface port-channel " + str(self._id)
        out = self.__swobj.show(cmd)
        log.debug(out)
        detailoutput = out['TABLE_port_channel_database']['ROW_port_channel_database']
        return detailoutput

    def __is_pc_present(self):
        cmd = "show port-channel database"
        out = self.__swobj.show(cmd)
        log.debug(out)
        if out:
            # There is atleast one PC in the switch
            pcdb = out['TABLE_port_channel_database']['ROW_port_channel_database']
            if type(pcdb) is dict:
                # There is only PC in the switch
                pcdblist = [pcdb]
            else:
                # There are multiple PC in the switch
                pcdblist = pcdb
            for eachpc in pcdblist:
                pcname = eachpc[portchanelkeys.INT]
                pcmatch = re.match(PAT_PC, pcname)
                if pcmatch:
                    pcid = pcmatch.group(1).strip()
                    if int(pcid) == self._id:
                        return True
            return False
        else:
            # There are no PC in the switch
            return False
