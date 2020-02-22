import logging
import re

from .. import constants
from ..fc import Fc
from ..nxapikeys import interfacekeys, vsankeys, zonekeys
from ..portchannel import PortChannel
from ..vsan import Vsan
from ..zone import Zone

log = logging.getLogger(__name__)


class SwitchUtils:

    @property
    def interfaces(self):
        retlist = {}
        cmd = "show interface brief"
        out = self.show(cmd)
        log.debug(out)

        # Get FC related data
        fcout = out.get('TABLE_interface_brief_fc', None)
        if fcout is not None:
            allfc = fcout['ROW_interface_brief_fc']
            if type(allfc) is dict:
                allfc = [allfc]
            for eacfc in allfc:
                fcname = eacfc[interfacekeys.INTERFACE]
                fcobj = Fc(switch=self, name=fcname)
                retlist[fcname] = fcobj

        # Get PC related data
        pcout = out.get('TABLE_interface_brief_portchannel', None)
        if pcout is not None:
            allpc = pcout['ROW_interface_brief_portchannel']
            if type(allpc) is dict:
                allpc = [allpc]
            for eacpc in allpc:
                pcname = eacpc[interfacekeys.INTERFACE]
                match = re.match(constants.PAT_PC, pcname)
                if match:
                    pcid = int(match.group(1))
                    pcobj = PortChannel(switch=self, id=pcid)
                    retlist[pcname] = pcobj
        return retlist

    @property
    def vsans(self):
        retlist = {}
        cmd = "show vsan"
        out = self.show(cmd)['TABLE_vsan']['ROW_vsan']
        for eachele in out:
            id = eachele.get(vsankeys.VSAN_ID)
            vobj = Vsan(switch=self, id=id)
            retlist[id] = vobj
        return retlist

    @property
    def zones(self):
        retlist = {}
        cmd = "show zone"
        out = self.show(cmd)
        if out:
            allzones = out['TABLE_zone']['ROW_zone']
            if type(allzones) is dict:
                allzones = [allzones]
            log.warning("There are a total of " + str(
                len(allzones)) + " zones across vsans. Please wait while we get the zone info...")
            for eachzone in allzones:
                vsanid = eachzone.get(zonekeys.VSAN_ID)
                vobj = Vsan(switch=self, id=vsanid)
                zname = eachzone.get(zonekeys.NAME)
                zobj = Zone(switch=self, vsan_obj=vobj, name=zname)
                listofzones = retlist.get(vsanid, None)
                print(vsanid)
                print(zname)
                if listofzones is None:
                    listofzones = [zobj]
                else:
                    listofzones.append(zobj)
                retlist[vsanid] = listofzones
            return retlist
        return None
