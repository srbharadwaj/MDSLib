import logging
import re

from .connection_manager.errors import CLIError
from .constants import SHUTDOWN, NO_SHUTDOWN
from .interface import Interface
from .nxapikeys import interfacekeys
from .utility.allexceptions import InvalidAnalyticsType

log = logging.getLogger(__name__)


class Fc(Interface):

    def __init__(self, switch, name):
        super().__init__(switch, name)
        self.__swobj = switch

    # property for out_of_service
    def _set_out_of_service(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "terminal dont-ask ; interface " + self.name + " ; out-of-service force ; no terminal dont-ask "
        if value:
            # First shutdown the port then
            self.status = SHUTDOWN
            self.__swobj.config(cmd)
        else:
            cmd = cmd.replace("out-of-service", "no out-of-service")
            self.__swobj.config(cmd)
            self.status = NO_SHUTDOWN

    # out_of_service property
    out_of_service = property(fset=_set_out_of_service)

    @property
    def transceiver(self):
        return self.Transceiver(self)

    @property
    def analytics_type(self):
        is_scsi = False
        is_nvme = False
        pat = "analytics type fc-(.*)"
        cmd = "show running-config interface " + self.name + " | grep analytics "
        out, error = self.__swobj._ssh_handle.show(cmd)
        if len(error) != 0:
            raise CLIError(cmd, error)
        else:
            for eachline in out:
                newline = eachline.strip().strip("\n")
                m = re.match(pat, newline)
                if m:
                    type = m.group(1)
                    if type == 'scsi':
                        is_scsi = True
                    if type == 'nvme':
                        is_nvme = True
        if is_scsi:
            if is_nvme:
                return 'all'
            else:
                return 'scsi'
        elif is_nvme:
            return 'nvme'
        else:
            return None

    @analytics_type.setter
    def analytics_type(self, type):
        if type is None:
            cmd = "no analytics type fc-all"
        elif type == 'scsi':
            cmd = "no analytics type fc-all ; analytics type fc-scsi"
        elif type == 'nvme':
            cmd = "no analytics type fc-all ; analytics type fc-nvme"
        elif type == 'all':
            cmd = "analytics type fc-all"
        else:
            raise InvalidAnalyticsType(
                "Invalid analytics type '" + type + "'. Valid types are scsi,nvme,all,None(to disable analytics type)")

        cmdtosend = "interface " + self.name + " ; " + cmd
        out, error = self.__swobj._ssh_handle.config(cmdtosend)
        if len(error) != 0:
            raise CLIError(cmd, error)

    def _execute_transceiver_cmd(self):
        result = {}
        cmd = "show interface " + self.name + " transceiver detail"
        log.debug("Sending the cmd")
        log.debug(cmd)
        out = self.__swobj.config(cmd)['body']['TABLE_interface_trans']['ROW_interface_trans']['TABLE_calib'][
            'ROW_calib']
        if type(out) is list:
            for d in out:
                result.update(d)
        else:
            result = out
        log.debug(result)
        return result

    class Transceiver(object):
        def __init__(self, fcobj):
            self.__fcobj = fcobj

        @property
        def sfp_present(self):
            out = self.__fcobj._execute_transceiver_cmd()
            retout = out.get(interfacekeys.SFP)
            return ("sfp is present" in retout)

        @property
        def name(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.NAME, None)

        @property
        def part_number(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.PART_NUM, None)

        @property
        def cisco_id(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.CISCO_ID, None)

        @property
        def cisco_part_number(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.CISCO_PART_NUM, None)

        @property
        def cisco_product_id(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.CISCO_PRODUCT_ID, None)

        @property
        def bit_rate(self):
            out = self.__fcobj._execute_transceiver_cmd()
            return out.get(interfacekeys.BIT_RATE, None)

        @property
        def min_speed(self):
            out = self.__fcobj._execute_transceiver_cmd()
            supp_speed = out.get(interfacekeys.SUPP_SPEED, None)
            if supp_speed is not None:
                pat = "Min speed: (\d+) Mb/s, Max speed: (\d+) Mb/s"
                match = re.match(pat, supp_speed)
                if match:
                    return match.group(1)
            return None

        @property
        def max_speed(self):
            out = self.__fcobj._execute_transceiver_cmd()
            supp_speed = out.get(interfacekeys.SUPP_SPEED, None)
            if supp_speed is not None:
                pat = "Min speed: (\d+) Mb/s, Max speed: (\d+) Mb/s"
                match = re.match(pat, supp_speed)
                if match:
                    return match.group(2)
            return None

        @property
        def temperature(self):
            out = self.__fcobj._execute_transceiver_cmd()
            try:
                calibdetails = out['TABLE_calibration']['ROW_calibration']['TABLE_detail']['ROW_detail']
                return calibdetails.get(interfacekeys.TEMPERATURE, None)
            except KeyError:
                return None

        @property
        def voltage(self):
            out = self.__fcobj._execute_transceiver_cmd()
            try:
                calibdetails = out['TABLE_calibration']['ROW_calibration']['TABLE_detail']['ROW_detail']
                return calibdetails.get(interfacekeys.VOLTAGE, None)
            except KeyError:
                return None

        @property
        def current(self):
            out = self.__fcobj._execute_transceiver_cmd()
            try:
                calibdetails = out['TABLE_calibration']['ROW_calibration']['TABLE_detail']['ROW_detail']
                return calibdetails.get(interfacekeys.CURRENT, None)
            except KeyError:
                return None

        @property
        def tx_power(self):
            out = self.__fcobj._execute_transceiver_cmd()
            try:
                calibdetails = out['TABLE_calibration']['ROW_calibration']['TABLE_detail']['ROW_detail']
                return calibdetails.get(interfacekeys.TX_POWER, None)
            except KeyError:
                return None

        @property
        def rx_power(self):
            out = self.__fcobj._execute_transceiver_cmd()
            try:
                calibdetails = out['TABLE_calibration']['ROW_calibration']['TABLE_detail']['ROW_detail']
                return calibdetails.get(interfacekeys.RX_POWER, None)
            except KeyError:
                return None
