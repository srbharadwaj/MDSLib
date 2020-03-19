__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import re

import requests
import time

from .analytics import Analytics
from .connection_manager.connect_nxapi import ConnectNxapi
from .connection_manager.errors import CLIError
from .connection_manager.ssh import SSHSession
from .nxapikeys import versionkeys
from .parsers.system.shtopology import ShowTopology
from .utility._switch_utility import SwitchUtils

log = logging.getLogger(__name__)


def log_exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
            # re-raise the exception
            raise

        return wrapper

    return decorator


class Switch(SwitchUtils):
    """

    Switch module

    :param ip_address: mgmt ip address of switch
    :type ip_address: str
    :param username: username
    :type id: str
    :param password: password
    :type password: str
    :param connection_type: connection type 'http' or 'https'(optional, default: 'https')
    :type connection_type: str
    :param port: port number (optional, default: 8443)
    :type port: int
    :param timeout: timeout period in seconds (optional, default: 30)
    :type timeout: int
    :param verify_ssl: SSL verification (optional, default: True)
    :type verify_ssl: bool

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)

    """

    def __init__(self, ip_address, username, password, connection_type='https', port=8443, timeout=30, verify_ssl=True):

        self.__ip_address = ip_address
        self.__username = username
        # self.__password = password
        self.connectiontype = connection_type
        self.port = port
        self.timeout = timeout
        self.__verify_ssl = verify_ssl

        log.info("Opening up a connection for switch with ip " + ip_address)
        self.__connection = ConnectNxapi(ip_address, username, password, transport=connection_type, port=port,
                                         verify_ssl=verify_ssl)

        self._ssh_handle = SSHSession(host=ip_address, username=username, password=password, timeout=timeout)
        self.can_connect = False
        # Get version of the switch and log it
        self.log_version()

    @log_exception(log)
    def log_version(self):
        """

        :return:
        """
        try:
            log.debug(self.version)
            self.can_connect = True
        except requests.exceptions.ConnectionError as e:
            msg = "ERROR!! Connection refused for the switch : " + self.ipaddr + \
                  " Verify that the switch has " + self.connectiontype + " configured with port " + str(self.port)
            log.error(msg)

    @property
    def ipaddr(self):
        """
        Get mgmt ip address of the switch

        :return: IP address of switch
        :rtype: str
        :example:
            >>> print(switch_obj.ipaddr)
            10.126.94.101
            >>>
        """

        return self.__ip_address

    @property
    def name(self):
        """
        get switchname or
        set switchname

        :getter:
        :return: switch name
        :rtype: str
        :example:
            >>> print(switch_obj.name)
            swTest
            >>>

        :setter:
        :param name: name of the switch that needs to be set
        :type name: str
        :example:
            >>> switch_obj.name = "yourswitchname"
            >>>

        .. warning:: Switch name must start with a letter, end with alphanumeric and contain alphanumeric and hyphen only. Max size 32.

        """

        return self.show("show switchname", raw_text=True).strip()

    @name.setter
    def name(self, swname):
        """

        :param swname:
        :return:
        """
        self.config("switchname " + swname)

    @property
    def npv(self):
        """
        Check if switch is in NPV mode

        :return: Returns True if switch is in NPV, else returns False
        :rtype: bool
        :example:
            >>> print(switch_obj.npv)
            False
            >>>
        """

        return self.__is_npv_switch()

    @property
    def version(self):
        """
        Get the switch software version

        :return: version
        :rtype: str
        :raises CLIError: Raises if there was a command error or some generic error due to which version could not be fetched
        :example:
            >>> print(switch_obj.version)
            8.4(1)
            >>>
        """

        out = self.show("show version")
        if not out:
            raise CLIError("show version",
                           'Unable to fetch the switch software version using show version command. Need to debug further')
        fullversion = out[versionkeys.VER_STR]
        ver = fullversion.split()[0]
        return ver

    @property
    def model(self):
        """
        Returns model of the switch

        :return: Returns model of the switch or returns None if model could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.model)
            MDS 9710 (10 Slot) Chassis
            >>>
            >>> print(switch2_obj.model)
            MDS 9396T 96X32G FC (2 RU) Chassis
            >>>
        """
        out = self.show("show version")
        if not out:
            return None
        return out[versionkeys.CHASSIS_ID]

    @property
    def form_factor(self):
        """
        Returns the form factor of the switch, i.e if its a 10 slot or 6 slot or 1RU or 2RU etc..

        :return: Returns form factor of the switch or returns None if form factor could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.form_factor)
            10 slot
            >>>
            >>> print(switch2_obj.form_factor)
            2 RU
            >>>
        """

        chassisid = self.model
        if chassisid is not None:
            pat = "MDS\s+(.*)\((.*)\)\s+Chassis"
            match = re.match(pat, chassisid)
            if match:
                ff = match.group(1).strip()
                type = match.group(2).strip()
                return ff
        return None

    @property
    def type(self):
        """
        Returns the type of the switch, i.e if its a 9710 or 9706 or 9396T etc..

        :return: Returns type of the switch or returns None if type could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.type)
            9710
            >>>
            >>> print(switch2_obj.type)
            9396T
            >>>

        """

        chassisid = self.model
        if chassisid is not None:
            pat = "MDS\s+(.*)\((.*)\)\s+Chassis"
            match = re.match(pat, chassisid)
            if match:
                ff = match.group(1).strip()
                type = match.group(2).strip()
                return type
        return None

    @property
    def image_string(self):
        """
        Returns the image's string that is specific to a particular platform example m9700-sf3ek9, m9100-s6ek9 etc..

        :return: Returns image string of the switch or returns None if image string could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.image_string)
            m9700-sf3ek9
            >>>
            >>> print(switch2_obj.image_string)
            m9300-s2ek9
            >>>

        """

        ff = self.form_factor
        if ff in ["9706", "9710", "9718"]:
            mods = self.modules
            for eachmod in mods:
                if "Supervisor Module-3" in eachmod.module_type:
                    return "m9700-sf3ek9"
                elif "Supervisor Module-4" in eachmod.module_type:
                    return "m9700-sf4ek9"
            return None
        elif "9132T" in ff:
            return "m9100-s6ek9"
        elif "9148S" in ff:
            return "m9100-s5ek9"
        elif "9148T" in ff:
            return "m9148-s6ek9"
        elif "9250i" in ff:
            return "m9250-s5ek9"
        elif "9396S" in ff:
            return "m9300-s1ek9"
        elif "9396T" in ff:
            return "m9300-s2ek9"
        else:
            return None

    @property
    def kickstart_image(self):
        """
        Returns the kickstart image of the switch

        :return: Returns kickstart image of the switch or returns None if kickstart image could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.kickstart_image)
            bootflash:///m9700-sf3ek9-kickstart-mz.8.4.1.bin
            >>>
            >>> print(switch2_obj.kickstart_image)
            bootflash:///m9300-s2ek9-kickstart-mz.8.4.1.bin
            >>>
        """

        out = self.show("show version")
        if not out:
            return None
        return out[versionkeys.KICK_FILE]

    @property
    def system_image(self):
        """
        Returns the system image of the switch

        :return: Returns system image of the switch or returns None if system image could not be fetched from the switch
        :rtype: str
        :example:
            >>> print(switch_obj.system_image)
            bootflash:///m9700-sf3ek9-mz.8.4.1.bin
            >>>
            >>> print(switch2_obj.system_image)
            bootflash:///m9300-s2ek9-mz.8.4.1.bin
            >>>
        """
        out = self.show("show version")
        if not out:
            return None
        return out[versionkeys.ISAN_FILE]

    @property
    def analytics(self):
        """
        Returns handler for analytics module, using which we could do analytics related operations

        :return: analytics handler
        :rtype: Analytics
        :example:
            >>> ana_handler = switch_obj.analytics
            >>>
        """

        return Analytics(self)

    def _cli_error_check(self, command_response):
        error = command_response.get(u'error')
        if error:
            command = command_response.get(u'command')
            if u'data' in error:
                raise CLIError(command, error[u'data'][u'msg'])
            else:
                raise CLIError(command, 'Invalid command.')

        error = command_response.get(u'clierror')
        if error:
            command = command_response.get(u'input')
            raise CLIError(command, error)

    def _cli_command(self, commands, rpc=u'2.0', method=u'cli'):
        if not isinstance(commands, list):
            commands = [commands]

        conn_response = self.__connection.send_request(commands, rpc_version=rpc, method=method, timeout=self.timeout)
        log.debug("conn_response is")
        log.debug(conn_response)

        text_response_list = []
        if rpc is not None:
            for command_response in conn_response:
                self._cli_error_check(command_response)
                text_response_list.append(command_response[u'result'])
        else:
            text_response_list = []
            for command_response in conn_response:
                if 'ins_api' in command_response.keys():
                    retout = command_response['ins_api']['outputs']['output']
                    if type(retout) is dict:
                        fullout = [retout]
                    else:
                        fullout = retout
                    for eachoutput in fullout:
                        # print(eachoutput)
                        self._cli_error_check(eachoutput)
                        text_response_list.append(eachoutput[u'body'])
        return text_response_list

    def show(self, command, raw_text=False):
        """

        :param command: The command to send to the switch.
        :param raw_text: Whether to return raw text or structured data.
        :return: The output of the show command, which could be raw text or structured data.
        """

        commands = [command]
        list_result = self.show_list(commands, raw_text)
        if list_result:
            return list_result[0]
        else:
            return {}

    def show_list(self, commands, raw_text=False):
        """

        :rtype: object
        :param list commands:
        :param bool raw_text:
        :return:
        """
        return_list = []
        if raw_text:
            response_list = self._cli_command(commands, method=u'cli_ascii')
            for response in response_list:
                if response:
                    return_list.append(response[u'msg'].strip())
        else:
            response_list = self._cli_command(commands)
            for response in response_list:
                if response:
                    return_list.append(response[u'body'])

        log.debug("Show commands sent are :")
        log.debug(commands)
        log.debug("Result got was :")
        log.debug(return_list)

        return return_list

    def config(self, command, rpc=u'2.0', method=u'cli'):
        """

        :param command:
        :param rpc:
        :param method:
        :return:
        """
        """Send a configuration command.
        Args:
            command (str): The command to send to the device.
        Raises:
            CLIError: If there is a problem with the supplied command.
        """
        commands = [command]
        list_result = self.config_list(commands, rpc, method)
        return list_result[0]

    def config_list(self, commands, rpc=u'2.0', method=u'cli'):
        """Send a list of configuration commands.
        Args:
            commands (list): A list of commands to send to the device.
        Raises:
            CLIError: If there is a problem with one of the commands in the list.
        """
        return_list = self._cli_command(commands, rpc=rpc, method=method)

        log.debug("Config commands sent are :")
        log.debug(commands)
        log.debug("Result got was :")
        log.debug(return_list)

        return return_list

    def reload(self, module: int = None, timeout: int = 300, copyrs=True):

        if module is None:
            # Switch reload
            cmd = "terminal dont-ask ; reload"
            if copyrs:
                log.info("Reloading switch after copy running-config startup-config")
                crs = self.show("copy running-config startup-config", raw_text=True)
                if 'Copy complete' in crs:
                    log.info('copy running-config startup-config is successful')
                else:
                    log.error('copy running-config startup-config failed')
                    log.error(crs.split("\n")[-1])
                    return {'FAILED': crs}
            else:
                log.info("Reloading switch without copy running-config startup-config")

        else:
            # Module reload
            mod = str(module)
            cmd = "terminal dont-ask ; reload module " + mod
            if copyrs:
                log.info("Reloading the module " + mod + " after copy running-config startup-config")
                crs = self.show("copy running-config startup-config", raw_text=True)
                if 'Copy complete' in crs:
                    log.info('copy running-config startup-config is successful')
                else:
                    log.error('copy running-config startup-config failed')
                    log.error(crs.split("\n")[-1])
                    return {'FAILED': crs}
            else:
                log.info("Reloading the module " + mod + " without copy running-config startup-config")

        shmod_before = self.show("show module", raw_text=True).split("\n")
        shintb_before = self.show("show interface brief", raw_text=True).split("\n")
        log.info("Reloading please wait...")
        out = self.config(cmd)
        time.sleep(timeout)
        shmod_after = self.show("show module", raw_text=True).split("\n")
        shintb_after = self.show("show interface brief", raw_text=True).split("\n")

        shcores = self.show("show cores", raw_text=True).split("\n")
        if len(shcores) > 2:
            log.error(
                "Cores present on the switch, please check the switch and also the log file")
            log.error(shcores[2:])
            return {'FAILED': out}

        if shmod_before == shmod_after:
            log.info("'show module' is correct after reload")
        else:
            log.error(
                "'show module' output is different from before and after reload, please check the log file")
            log.debug("'show module' before reload")
            log.debug(shmod_before)
            log.debug("'show module' after reload")
            log.debug(shmod_after)

            bset = set(shmod_before)
            aset = set(shmod_after)
            bef = list(bset - aset)
            aft = list(aset - bset)
            log.debug("diff of before after reload")
            log.debug(bef)
            log.debug(aft)
            return {'FAILED': [bef, aft]}

        if shintb_before == shintb_after:
            log.info("'show interface brief' is correct after reload")
        else:
            log.error(
                "'show interface brief' output is different from before and after reload, please check the log file")
            log.debug("'show interface brief' before reload")
            log.debug(shintb_before)
            log.debug("'show interface brief' after reload")
            log.debug(shintb_after)

            bset = set(shintb_before)
            aset = set(shintb_after)
            bef = list(bset - aset)
            aft = list(aset - bset)
            log.debug("diff of before after reload")
            log.debug(bef)
            log.debug(aft)
            return {'FAILED': [bef, aft]}
        log.info("Reload was successful")
        return {'SUCESS': None}

    def __is_npv_switch(self):
        jsonoutput = True
        try:
            flist = self.show("show feature")
        except CLIError as c:
            if "cannot be parsed by the server" in c.message:
                jsonoutput = False
                flist = self.show("show feature", raw_text=True)
                log.debug(c)
            else:
                log.error(
                    "Could not discover the entire fabric, since 'show feature' could not be run on the switch " + self.ipaddr)

        if not jsonoutput:
            for eachline in flist.splitlines():
                if 'npv' in eachline:
                    if 'enabled' in eachline.lower():
                        return True
                    else:
                        return False
        else:
            flist = flist['TABLE_cfcFeatureCtrl2Table']['ROW_cfcFeatureCtrl2Table']
            # print(flist)
            for eachf in flist:
                if eachf['cfcFeatureCtrlName2'].strip() == 'npv':
                    if eachf['cfcFeatureCtrlOpStatus2'].strip().lower() == 'enabled':
                        return True
                    else:
                        return False
        return False

    def get_peer_switches(self):
        peer_sw_list = []
        shtopoout = self.show("show topology", raw_text=True)
        sh = ShowTopology(shtopoout.splitlines())
        for vsan, interfacelist in sh.parse_data.items():
            for eachinterface in interfacelist:
                peer_sw_ip = eachinterface['peer_ip']
                peer_sw_list.append(peer_sw_ip)
        peerlist = list(dict.fromkeys(peer_sw_list))
        log.debug("Peer NPIV list of switch : " + self.ipaddr + " are: ")
        log.debug(peerlist)
        return peerlist

    def get_peer_npv_switches(self):
        retout = []
        try:
            fcnsout = self.show("show fcns database detail")['TABLE_fcns_vsan']['ROW_fcns_vsan']
        except KeyError:
            return None
        if type(fcnsout) is dict:
            fcnsout = [fcnsout]
        for eachline in fcnsout:
            temp = eachline['TABLE_fcns_database']['ROW_fcns_database']
            # print(temp)
            if type(temp['fc4_types_fc4_features']) is str:
                if temp['fc4_types_fc4_features'].strip() == 'npv':
                    ip = temp['node_ip_addr']
                    retout.append(ip)
        peerlist = list(dict.fromkeys(retout))
        log.debug("Peer NPV list of switch : " + self.ipaddr + " are: ")
        log.debug(peerlist)
        return peerlist
