import logging
import re

from .. import constants
from ..fc import Fc
from ..nxapikeys import interfacekeys
from ..portchannel import PortChannel

log = logging.getLogger(__name__)


class SwitchUtils:

    @property
    def interfaces(self):
        retlist = []
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
                retlist.append(fcobj)

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
                    retlist.append(pcobj)
        return retlist

    @property
    def vsans(self):
        retlist = []
        cmd = "show vsan"
        out = self.show(cmd)
        print(out['TABLE_vsan']['ROW_vsan'])

    @property
    def zones(self):
        pass
