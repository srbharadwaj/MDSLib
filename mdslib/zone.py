import logging
import re

import time

from .connection_manager.errors import CLIError
from .constants import ENHANCED, BASIC, PERMIT, DENY, PAT_WWN
from .fc import Fc
from .nxapikeys import zonekeys
from .portchannel import PortChannel
from .utility.allexceptions import InvalidZoneMemberType, InvalidZoneMode
from .vsan import VsanNotPresent

log = logging.getLogger(__name__)


class Zone(object):
    def __init__(self, switch, vsan_obj, name):
        self.__swobj = switch
        self._vsanobj = vsan_obj
        self._vsan = self._vsanobj.id
        if self._vsan is None:
            raise VsanNotPresent(
                "Vsan " + str(self._vsanobj._id) + " is not present on the switch. Please create the vsan first.")
        self._name = name
        self.__zones = None
        self.__rpc = None
        self.__method = u'cli_conf'

    @property
    def name(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_name()
        if out:
            return out[zonekeys.NAME]
        return None

    @property
    def vsan(self):
        if self.name is not None:
            return self._vsanobj
        return None

    @property
    def members(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
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
        return None

    @property
    def mode(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[zonekeys.MODE]

    @mode.setter
    def mode(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "terminal dont-ask ; zone mode " + ENHANCED + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == ENHANCED:
            self._send_zone_cmd(cmd)
        elif value.lower() == BASIC:
            cmd = cmd.replace("zone mode", "no zone mode")
            self._send_zone_cmd(cmd)
        else:
            raise InvalidZoneMode(
                "Invalid zone mode " + value + " . Valid values are: " + BASIC + "," + ENHANCED)

    @property
    def default_zone(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[zonekeys.DEFAULT_ZONE]

    @default_zone.setter
    def default_zone(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "terminal dont-ask ; zone default-zone " + PERMIT + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == PERMIT:
            self._send_zone_cmd(cmd)
        elif value.lower() == DENY:
            cmd = cmd.replace("zone default-zone", "no zone default-zone")
            self._send_zone_cmd(cmd)
        else:
            raise CLIError("No cmd sent",
                           "Invalid default-zone value " + value + " . Valid values are: " + PERMIT + "," + DENY)

    @property
    def smart_zone(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[zonekeys.SMART_ZONE]

    @smart_zone.setter
    def smart_zone(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zone smart-zoning enable vsan " + str(self._vsan)
        if value:
            # If True then enable smart zoning
            cmd = "terminal dont-ask ; " + cmd + " ; no terminal dont-ask"
        else:
            # If False then disable smart zoning
            cmd = "terminal dont-ask ; no " + cmd + " ; no terminal dont-ask"
        self._send_zone_cmd(cmd)

    def create(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zone name " + self._name + " vsan " + str(self._vsan)
        self._send_zone_cmd(cmd)

    def delete(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "no zone name " + self._name + " vsan " + str(self._vsan)
        self._send_zone_cmd(cmd)

    def add_members(self, members):
        self.__add_remove_members(members)

    def remove_members(self, members):
        self.__add_remove_members(members, remove=True)

    def __add_remove_members(self, members, remove=False):
        cmdlist = []
        cmdlist.append("zone name " + self._name + " vsan " + str(self._vsan))
        for eachmem in members:
            if (type(eachmem) is Fc) or (type(eachmem) is PortChannel):
                name = eachmem.name
                cmd = "member interface " + name
                if remove:
                    cmd = "no " + cmd
                cmdlist.append(cmd)
            elif type(eachmem) is str:
                m = re.match(PAT_WWN, eachmem)
                if m:
                    # zone member type is pwwn
                    cmd = "member pwwn " + eachmem
                    if remove:
                        cmd = "no " + cmd
                    cmdlist.append(cmd)
                else:
                    # zone member type is of device-alias
                    cmd = "member device-alias " + eachmem
                    if remove:
                        cmd = "no " + cmd
                    cmdlist.append(cmd)
            else:
                raise InvalidZoneMemberType(
                    "Invalid zone member type, currently we support member of type pwwn or device-alias or interface only")
        cmds_to_send = " ; ".join(cmdlist)
        self._send_zone_cmd(cmds_to_send)

    @property
    def locked(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        self._lock_details = out[zonekeys.SESSION]
        if "none" in self._lock_details:
            return False
        else:
            return True

    def clear_lock(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
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

    def _send_zone_cmd(self, cmd):
        if self.locked:
            raise CLIError("ERROR!! Zone lock is acquired. Lock details are: " + self._lock_details)
        try:
            out = self.__swobj.config(cmd)
            log.debug(out)
        except CLIError as c:
            if "Duplicate member" in c.message:
                return False, None
            log.error(c)
            raise CLIError(cmd, c.message)

        if out is not None:
            msg = out['msg'].strip()
            log.debug("------" + msg)
            if msg:
                if "Current zoning mode same as specified zoning mode" in msg:
                    log.debug(msg)
                elif "Set zoning mode command initiated. Check zone status" in msg:
                    log.debug(msg)
                elif "Enhanced zone session has been created" in msg:
                    log.debug(msg)
                elif "No zone policy change" in msg:
                    log.debug(msg)
                elif "Smart Zoning distribution initiated. check zone status" in msg:
                    log.debug(msg)
                elif "Smart-zoning is already enabled" in msg:
                    log.debug(msg)
                elif "Smart-zoning is already disabled" in msg:
                    log.debug(msg)
                elif "Duplicate member" in msg:
                    log.debug(msg)
                elif "Zoneset activation initiated" in msg:
                    log.debug(msg)
                elif "Specified zoneset already active and unchanged" in msg:
                    log.debug(msg)
                elif "Zoneset deactivation initiated" in msg:
                    log.debug(msg)
                else:
                    log.error(msg)
                    self.__clear_lock_if_enhanced()
                    raise CLIError(cmd, msg)
        self.__commit_config_if_locked()

    def __clear_lock_if_enhanced(self):
        time.sleep(2)
        if self.mode == ENHANCED:
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
