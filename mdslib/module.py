from mdslib.connection_manager.errors import CLIError
import logging
from mdslib.utility import nxapikeys

log = logging.getLogger(__name__)


class Module(object):
    def __init__(self, switch, mod_num, modinfo):
        self.__swobj = switch
        self.__modinfo = modinfo

        self.__mod_num = mod_num
        self.__mod_ports = self.__modinfo[nxapikeys.MOD_PORTS]
        self.__mod_modtype = self.__modinfo[nxapikeys.MOD_TYPE]
        self.__mod_model = self.__modinfo[nxapikeys.MOD_MODEL]
        self.__mod_status = self.__modinfo[nxapikeys.MOD_STATUS]

    @property
    def module_number(self):
        if self.__mod_num is None:
            self.__modinfo = self.__get_modinfo()
        self.__mod_num = self.__modinfo[nxapikeys.MOD_NUM]
        return int(self.__mod_num)

    @property
    def ports(self):
        if self.__mod_ports is None:
            self.__modinfo = self.__get_modinfo()
        self.__mod_ports = self.__modinfo[nxapikeys.MOD_PORTS]
        return int(self.__mod_ports)

    @property
    def module_type(self):
        if self.__mod_modtype is None:
            self.__modinfo = self.__get_modinfo()
        self.__mod_modtype = self.__modinfo[nxapikeys.MOD_TYPE]
        return self.__mod_modtype

    @property
    def model(self):
        if self.__mod_model is None:
            self.__modinfo = self.__get_modinfo()
        self.__mod_model = self.__modinfo[nxapikeys.MOD_MODEL]
        return self.__mod_model

    @property
    def status(self):
        self.__modinfo = self.__get_modinfo()
        self.__mod_status = self.__modinfo[nxapikeys.MOD_STATUS]
        return self.__mod_status

    def __get_modinfo(self):
        cmd = "show module " + str(self.__mod_num)
        out = self.__swobj.show(cmd)
        out = out['TABLE_modinfo']['ROW_modinfo']
        log.debug("Output of the cmd " + cmd)
        log.debug(out)
        return out
