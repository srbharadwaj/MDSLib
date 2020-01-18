from .interface import Interface
from .constants import CHANNEL_MODE
from .connection_manager.errors import CLIError
import logging

log = logging.getLogger(__name__)


class InvalidChannelMode(Exception):
    def __init__(self, value):
        Exception.__init__(self, "Invalid channel mode (" + str(value) + "), channel mode must be one of (" + ', '.join(
            CHANNEL_MODE) + ")")



class PortChannel(Interface):
    def __init__(self, switch, id):
        self._id = id
        name = "port-channel" + str(self._id)
        super().__init__(switch, name)
        self.__swobj = switch

    @property
    def id(self):
        return self._id

    @property
    def channel_mode(self):
        raise NotImplementedError
        #NXAPI not yet available

    @channel_mode.setter
    def channel_mode(self,mode):
        if mode not in CHANNEL_MODE:
            raise InvalidChannelMode(mode)
        else:
            raise NotImplementedError

    def create(self):
        cmd = "interface port-channel " + str(self._id)
        self.__swobj.config(cmd)

    def delete(self):
        cmd = "no interface port-channel " + str(self._id)
        self.__swobj.config(cmd)
        # try:
        #     cmd = "terminal dont-ask ; " \
        #           "vsan database ; " \
        #           "no vsan " + str(self._id)
        #     self.__swobj.config(cmd)
        # except CLIError as c:
        #     cmd = "no terminal dont-ask"
        #     self.__swobj.config(cmd)
        #     log.error(c)
        #     raise CLIError(cmd, c.message)
        # finally:
        #     cmd = "no terminal dont-ask"
        #     self.__swobj.config(cmd)
