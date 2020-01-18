from mdslib.connection_manager.errors import CLIError
from mdslib.utility import nxapikeys

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
        vid = out[nxapikeys.VSAN_ID]
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
            return out.get(nxapikeys.VSAN_NAME)
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
            return out.get(nxapikeys.VSAN_STATE)
        return None

    @property
    def interfaces(self):
        raise NotImplementedError
        out = self.__get_facts()
        if type(out) is not dict:
            return None
        else:
            try:
                return out['vsan_interfaces']
            except KeyError:
                return None

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
            cmd = "no terminal dont-ask"
            self.__swobj.config(cmd)
            log.error(c)
            raise CLIError(cmd, c.message)
        finally:
            cmd = "no terminal dont-ask"
            self.__swobj.config(cmd)

    def add_interfaces(self, interfaces):
        raise NotImplementedError
        # cmd = "vsan database ; vsan " + str(self.name) + " interface " + ','.join(interfaces)
        cmdlist = []
        for eachint in interfaces:
            cmd = "vsan database ; vsan " + str(self._id) + " interface " + eachint
            cmdlist.append(cmd)
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
            vsanlist.append(str(eachv[nxapikeys.VSAN_ID]))
        if str(self._id) not in vsanlist:
            raise VsanNotPresent("Vsan " + str(self._id) + " is not present on the switch.")

        shvsan_req_out = {}

        # Parse show vsan json output
        for eachele in listofvsaninfo:
            if str(eachele[nxapikeys.VSAN_ID]) == str(self._id):
                shvsan_req_out = eachele
                break
        if not shvsan_req_out:
            log.debug("No info for vsan " + str(self._id))
            return None

        return dict(shvsan_req_out)

    def __get_facts_sh_vsan_mem(self):
        shvsanmem_req_out = {}
        shvsanmem = self.__swobj.show("show vsan membership")

        # Parse show vsan membership json output
        try:
            details = shvsanmem["TABLE_vsan_membership"]["ROW_vsan_membership"]

            if type(details) is dict:
                members = details['interface']
            else:
                members = [eachdetails['interface'] for eachdetails in details]
            shvsanmem_req_out = {'vsan_interfaces': members}
            if not shvsanmem_req_out:
                return None
        except KeyError:
            return None

        return shvsanmem_req_out

# TODO: Check vsan range during create/delete/addinterface etc..
# TODO: Interfaces
