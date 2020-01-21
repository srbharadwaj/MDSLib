from mdslib.connection_manager.errors import CLIError
from .vsan import Vsan, VsanNotPresent
from . import constants
from .nxapikeys import zonekeys
import logging
import time

log = logging.getLogger(__name__)


class InvalidArgument(Exception):
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


class Zone(object):
    def __init__(self, switch, vsanobj, name):
        self.__swobj = switch
        self._vsanobj = vsanobj
        self._vsan = self._vsanobj.id
        if self._vsan is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        self._name = name
        self.__zones = None
        self.__rpc = None
        self.__method = u'cli_conf'

    @property
    def name(self):
        out = self.__show_zone_name()
        if out:
            return out[zonekeys.ZONE_NAME]

    @property
    def vsan(self):
        if self.name is not None:
            return self._vsanobj
        else:
            return None

    @property
    def members(self):
        out = self.__show_zone_name()
        if out:
            try:
                retout = out['TABLE_zone_member']['ROW_zone_member']
            except KeyError:
                return None
            if type(retout) is dict:
                # means there is only one member for the zone, so convert to list and return
                return [retout]
            return retout

    @property
    def mode(self):
        out = self.__show_zone_status()
        return out[zonekeys.ZONE_MODE]

    @mode.setter
    def mode(self, value):
        cmd = "terminal dont-ask ; zone mode " + constants.ENHANCED + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == constants.ENHANCED:
            self.__send_zone_cmds(cmd)
        elif value.lower() == constants.BASIC:
            cmd = cmd.replace("zone mode", "no zone mode")
            self.__send_zone_cmds(cmd)
        else:
            raise InvalidArgument(
                "Invalid zone mode " + value + " . Valid values are: " + constants.BASIC + "," + constants.ENHANCED)

    @property
    def default_zone(self):
        out = self.__show_zone_status()
        return out[zonekeys.ZONE_DEFAULT_ZONE]

    @default_zone.setter
    def default_zone(self, value):
        cmd = "terminal dont-ask ; zone default-zone " + constants.PERMIT + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == constants.PERMIT:
            self.__send_zone_cmds(cmd)
        elif value.lower() == constants.DENY:
            cmd = cmd.replace("zone default-zone", "no zone default-zone")
            self.__send_zone_cmds(cmd)
        else:
            raise CLIError("No cmd sent",
                           "Invalid default-zone value " + value + " . Valid values are: " + constants.PERMIT + "," + constants.DENY)

    @property
    def smart_zone(self):
        out = self.__show_zone_status()
        return out[zonekeys.ZONE_SMART_ZONE]

    @property
    def locked(self):
        out = self.__show_zone_status()
        self._lock_details = out[zonekeys.ZONE_SESSION]
        if "none" in self._lock_details:
            return False
        else:
            return True

    def clear_lock(self):
        cmd = "terminal dont-ask ; clear zone lock vsan  " + str(self._vsan) + " ; no terminal dont-ask"
        out = self.__swobj.config(cmd)
        if out is not None:
            msg = out['msg']
            if msg:
                if "Zone database not locked" in msg:
                    log.debug(msg)
                elif "No pending info found" in msg:
                    log.debug(msg)
                else:
                    log.error(msg)
                    raise CLIError(cmd, msg)

    def __show_zone_name(self):
        log.debug("Executing the cmd show zone name <> vsan <> ")
        cmd = "show zone name " + self._name + " vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out

    def __show_zone_status(self):
        log.debug("Executing the cmd show zone status vsan <> ")
        cmd = "show zone status vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out['TABLE_zone_status']['ROW_zone_status']

    def __send_zone_cmds(self, cmd):
        if self.locked:
            raise CLIError("ERROR!! Zone lock is acquired. Lock details are: " + self._lock_details)
        out = self.__swobj.config(cmd)
        log.debug(out)
        if out is not None:
            msg = out['msg']
            if msg:
                if "Current zoning mode same as specified zoning mode" in msg:
                    log.debug(msg)
                elif "Set zoning mode command initiated. Check zone status" in msg:
                    log.debug(msg)
                elif "Enhanced zone session has been created" in msg:
                    log.debug(msg)
                elif "No zone policy change" in msg:
                    log.debug(msg)
                else:
                    log.error(msg)
                    self.__clear_lock_if_enhanced()
                    raise CLIError(cmd, msg)
        time.sleep(5)
        self.__commit_config_if_locked()

    def __clear_lock_if_enhanced(self):
        if self.mode == constants.ENHANCED:
            self.clear_lock()

    def __commit_config_if_locked(self):
        time.sleep(2)
        if self.locked:
            cmd = "zone commit vsan " + str(self._vsan)
            log.debug("Executing the cmd " + cmd)
            try:
                o = self.__swobj.config(cmd)
                if o is not None:
                    msg = o['msg']
                    if msg:
                        if "Commit operation initiated. Check zone status" in msg:
                            return
                        else:
                            log.error(msg)
                            raise CLIError(cmd, msg)
            except CLIError as c:
                msg = c.message
                if "No pending info found" in msg:
                    return
                else:
                    raise CLIError(cmd, msg)
