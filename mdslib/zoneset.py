import logging

import time

from .connection_manager.errors import CLIError
from .nxapikeys import zonekeys
from .utility.allexceptions import VsanNotPresent
from .zone import Zone

log = logging.getLogger(__name__)


class ZoneSet(object):
    def __init__(self, switch, vsan_obj, name):
        self.__swobj = switch
        self._vsanobj = vsan_obj
        self._vsan = self._vsanobj.id
        if self._vsan is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        self._name = name
        # Create a dummy zone obj, DO NOT use create method with it
        log.debug("Creating a dummy zone object for the zoneset with name " + self._name)
        self.__zoneObj = Zone(self.__swobj, self._vsanobj, name=None)

    @property
    def name(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zoneset_name()
        if out:
            out = out.get('TABLE_zoneset').get('ROW_zoneset')
            return out[zonekeys.NAME]
        return None

    @property
    def vsan(self):
        if self.name is not None:
            return self._vsanobj
        return None

    @property
    def members(self):
        retlist = {}
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zoneset_name()
        if out:
            zonesetdata = out.get('TABLE_zoneset', None).get('ROW_zoneset', None)
            if zonesetdata is not None:
                zonedata = zonesetdata.get('TABLE_zone', None)
                if zonedata is not None:
                    zdb = zonedata.get('ROW_zone', None)
                    if type(zdb) is dict:
                        zname = zdb[zonekeys.NAME]
                        retlist[zname] = Zone(self.__swobj, self._vsanobj, zname)
                    else:
                        for eachzdb in zdb:
                            zname = eachzdb[zonekeys.NAME]
                            retlist[zname] = Zone(self.__swobj, self._vsanobj, eachzdb)
                    return retlist
        return None

    def create(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def delete(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "no zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def add_members(self, members):
        self.__add_remove_members(members)

    def remove_members(self, members):
        self.__add_remove_members(members, remove=True)

    def activate(self, action=True):
        time.sleep(1)
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        if self.name is not None:
            if action:
                cmd = "terminal dont-ask ; zoneset activate name " + self._name + " vsan " + str(
                    self._vsan) + " ; no terminal dont-ask"
            else:
                cmd = "terminal dont-ask ; no zoneset activate name " + self._name + " vsan " + str(
                    self._vsan) + " ; no terminal dont-ask"
            try:
                self.__zoneObj._send_zone_cmd(cmd)
            except CLIError as c:
                if "Fabric unstable" in c.message:
                    log.error("Fabric is currently unstable, executing activation after few secs")
                    time.sleep(5)
                    self.__zoneObj._send_zone_cmd(cmd)

    def is_zoneset_active(self):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "show zoneset active vsan " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        if out:
            azsdetails = out['TABLE_zoneset']['ROW_zoneset']
            azs = azsdetails[zonekeys.NAME]
            if azs == self._name:
                return True
        return False

    def __add_remove_members(self, members, remove=False):
        cmdlist = []
        cmdlist.append("zoneset name " + self._name + " vsan " + str(self._vsan))
        for eachmem in members:
            name_of_zone = eachmem.name
            if name_of_zone is not None:
                if remove:
                    cmd = "no member " + name_of_zone
                else:
                    cmd = "member " + name_of_zone
                cmdlist.append(cmd)
        cmds_to_send = " ; ".join(cmdlist)
        self.__zoneObj._send_zone_cmd(cmds_to_send)

    def __show_zoneset_name(self):
        log.debug("Executing the cmd show zone name <> vsan <> ")
        cmd = "show zoneset name " + self._name + " vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out
