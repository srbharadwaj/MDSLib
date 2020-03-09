import logging
import re

from .utility.allexceptions import CommonException

log = logging.getLogger(__name__)


class InvalidProfile(CommonException):
    pass


# protocol: scsi
# metrics: [port, total_read_io_time, total_write_io_time] - - default[] all
# view: scsi_initiator_it_flow
#
# sw.create_analytics_query(
#     name=
#     profile =
# clear = False
# differential = False
# interval = 30)
#
# sw.delete_analytics_query(name=)
#
# sw.show_analytics_query(name=)
#
# sw.show_analytics(profile=)
# sw.clear_analytics(profile=)
# sw.purge_analytics(profile=)

# Be extra careful while changing the patterns or the keys of the patten
METRICS = 'metrics'
PROTOCOL = 'protocol'
VIEW = 'view'
VALID_PROTOCOLS = ['scsi', 'nvme']
MOD_PAT = "^\|\s+(?P<module>\d+)\s+\|\s+(?P<scsi_npu_load>\d+)\s+(?P<nvme_npu_load>\d+)\s+(?P<total_npu_load>\d+)\s+\|" \
          "\s+(?P<scsi_itls>\d+)\s+(?P<nvme_itns>\d+)\s+(?P<both_itls_itns>\d+)\s+\|" \
          "\s+(?P<scsi_initiators>\d+)\s+(?P<nvme_initiators>\d+)\s+(?P<total_initiators>\d+)\s+\|" \
          "\s+(?P<scsi_targets>\d+)\s+(?P<nvme_targets>\d+)\s+(?P<total_targets>\d+)\s+\|$"
MOD_PAT_COMP = re.compile(MOD_PAT)
TOTAL_PAT = "^\| Total  \| n\/a  n\/a  n\/a   \|\s+(?P<scsi_itls>\d+)\s+(?P<nvme_itns>\d+)\s+(?P<both_itls_itns>\d+)\s+\|" \
            "\s+(?P<scsi_initiators>\d+)\s+(?P<nvme_initiators>\d+)\s+(?P<total_initiators>\d+)\s+\|" \
            "\s+(?P<scsi_targets>\d+)\s+(?P<nvme_targets>\d+)\s+(?P<total_targets>\d+)\s+\|$"
TOTAL_PAT_COMP = re.compile(TOTAL_PAT)
TIME_PAT = "As of (?P<collected_at>.*)"
TIME_PAT_COMP = re.compile(TIME_PAT)


class Analytics():
    def __init__(self, sw):
        self.sw = sw

    def _show_analytics_system_load(self):

        """
        Sample output of this proc is as follows
        """
        """
        sw129-Luke(config-if)# show analytics system-load 
         n/a - not applicable
         ----------------------------------- Analytics System Load Info -------------------------------
         | Module | NPU Load (in %) | ITLs   ITNs   Both  |        Hosts        |       Targets       |
         |        | SCSI NVMe Total | SCSI   NVMe   Total | SCSI   NVMe   Total | SCSI   NVMe   Total |
         ----------------------------------------------------------------------------------------------
         |   1    | 0    43   43    | 0      15     15    | 0      10     10    | 0      1      1     |
         |   7    | 0    8    8     | 0      5      5     | 0      5      5     | 0      0      0     |
         | Total  | n/a  n/a  n/a   | 0      20     20    | 0      15     15    | 0      1      1     |
         ----------------------------------------------------------------------------------------------

        As of Fri Mar  6 17:12:22 2020
        sw129-Luke(config-if)# 

        [{'both_itls_itns': 15,
          'module': '1',
          'nvme_initiators': 10,
          'nvme_itns': 15,
          'nvme_npu_load': '43',
          'nvme_targets': 1,
          'scsi_initiators': 0,
          'scsi_itls': 0,
          'scsi_npu_load': '0',
          'scsi_targets': 0,
          'total_initiators': 0,
          'total_npu_load': '43',
          'total_targets': 15},
         {'both_itls_itns': 8,
          'module': '7',
          'nvme_initiators': 8,
          'nvme_itns': 8,
          'nvme_npu_load': '8',
          'nvme_targets': 5,
          'scsi_initiators': 0,
          'scsi_itls': 0,
          'scsi_npu_load': '0',
          'scsi_targets': 0,
          'total_initiators': 8,
          'total_npu_load': '8',
          'total_targets': 5},
         {'both_itls_itns': '20',
          'nvme_initiators': '15',
          'nvme_itns': '20',
          'nvme_targets': '1',
          'scsi_initiators': '0',
          'scsi_itls': '0',
          'scsi_targets': '0',
          'total_initiators': '15',
          'total_targets': '1'},
         {'collected_at': 'Fri Mar  6 17:12:22 2020'}]
        """

        all = []
        out, error = self.sw._ssh_handle.config("show analytics system-load")
        for eachout in out:
            eachout = eachout.strip()
            if any(char.isdigit() for char in eachout):
                print(eachout)
                result_mod = MOD_PAT_COMP.match(eachout)
                if result_mod:
                    # print(result_mod.group())
                    d = result_mod.groupdict()
                    all.append(d)
                    continue
                result_tot = TOTAL_PAT_COMP.match(eachout)
                if result_tot:
                    d = result_tot.groupdict()
                    all.append(d)
                    continue
                result_time = TIME_PAT_COMP.match(eachout)
                if result_time:
                    d = result_time.groupdict()
                    all.append(d)
                    continue
        if len(all) == 0:
            return None
        else:
            return all

    def _validate_profile(profile):
        # TODO
        # LIMITATIONS:
        # Need to do validation for profiles
        # Does not support where clause for now
        proto = profile.get(PROTOCOL, None)
        metrics = profile.get(PROTOCOL, None)
        view = profile.get(PROTOCOL, None)
        if proto is None:
            raise InvalidProfile(
                "'" + PROTOCOL + "' key is missing from the profile, this is mandatory and it needs to one of " + ",".join(
                    VALID_PROTOCOLS))
        if metrics is None:
            raise InvalidProfile(
                "'" + METRICS + "' key is missing from the profile, this is mandatory. A blank list represents 'all'")
        if view is None:
            raise InvalidProfile("'" + VIEW + "' key is missing from the profile, this is mandatory")
        if proto not in VALID_PROTOCOLS:
            raise InvalidProfile("'" + PROTOCOL + "' key needs to one of " + ",".join(VALID_PROTOCOLS))

        return True

    def _get_select_query_string(profile):
        metrics = profile.get(METRICS, None)
        if (metrics is None) or (len(metrics) == 0):
            selq = "select all from fc-" + profile.get(PROTOCOL) + "." + profile.get(VIEW)
        else:
            allmetrics = ','.join(metrics)
            selq = "select " + allmetrics + " from fc-" + profile.get(PROTOCOL) + "." + profile.get(VIEW)
        return selq

    def create_query(self, name, profile, clear=False, differential=False, interval=30):
        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile)
            cmd = 'analytics query "' + selq + '" name ' + name + " type periodic interval " + str(interval)
            if clear:
                if differential:
                    cmd = cmd + " clear differential"
                else:
                    cmd = cmd + " clear"
            elif differential:
                cmd = cmd + " differential"
            log.info("Cmd to be sent is " + cmd)
            return self.sw._ssh_handle.config(cmd)

    def delete_query(self, name):
        cmd = "no analytics name " + name
        log.info("Cmd to be sent is " + cmd)
        return self._ssh_handle.config(cmd)

    def show_query(self, name=None, profile=None, clear=False, differential=False):
        if (name is not None) and (profile is not None):
            raise TypeError()
        if name is None:
            # Profile is set so its a pull query
            if self._validate_profile(profile):
                selq = self._get_select_query_string(profile)
                cmd = 'show analytics query "' + selq + '"'
                if clear:
                    cmd = cmd + " clear "
                    if differential:
                        cmd = cmd + " differential "
                elif differential:
                    cmd = cmd + " differential "
                log.info("Cmd to be sent is " + cmd)
                return self.sw._ssh_handle.show(cmd)
        else:
            # Name is set, so its an install query
            cmd = "show analytics query name " + name + " result"
            log.info("Cmd to be sent is " + cmd)
            return self.sw._ssh_handle.show(cmd)

    def clear(self, profile):
        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile)
            cmd = 'clear analytics query "' + selq + '"'
            log.info("Cmd to be sent is " + cmd)
            return self.sw._ssh_handle.config(cmd)

    def purge(self, profile):
        if self._validate_profile(profile):
            selq = self._get_select_query_string(profile)
            purgecmd = 'purge analytics query "' + selq + '"'
            cmd = "terminal dont-ask ; " + purgecmd + " ; no terminal dont-ask"
            log.info("Cmd to be sent is " + cmd)
            return self.sw._ssh_handle.config(cmd)

    def npu_load(self, module, protocol=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if mod_str == str(module):
                if protocol == 'scsi':
                    return eachrow.get('scsi_npu_load')
                if protocol == 'nvme':
                    return eachrow.get('nvme_npu_load')
                if protocol is None:
                    return eachrow.get('total_npu_load')

    def itls(self, module=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if module is None:
                if mod_str is None:
                    return eachrow.get('scsi_itls')
            else:
                if mod_str == str(module):
                    return eachrow.get('scsi_itls')

    def itns(self, module=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if module is None:
                if mod_str is None:
                    return eachrow.get('nvme_itns')
            else:
                if mod_str == str(module):
                    return eachrow.get('nvme_itns')

    def itls_itns(self, module=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if module is None:
                if mod_str is None:
                    return eachrow.get('both_itls_itns')
            else:
                if mod_str == str(module):
                    return eachrow.get('both_itls_itns')

    def initiators(self, module=None, protocol=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if module is None:
                if mod_str is None:
                    if protocol == 'scsi':
                        return eachrow.get('scsi_initiators')
                    if protocol == 'nvme':
                        return eachrow.get('nvme_initiators')
                    if protocol is None:
                        return eachrow.get('total_initiators')
            else:
                if mod_str == str(module):
                    if protocol == 'scsi':
                        return eachrow.get('scsi_initiators')
                    if protocol == 'nvme':
                        return eachrow.get('nvme_initiators')
                    if protocol is None:
                        return eachrow.get('total_initiators')

    def targets(self, module=None, protocol=None):
        out = self._show_analytics_system_load()
        if out is None:
            return None
        for eachrow in out:
            mod_str = eachrow.get('module', None)
            if module is None:
                if mod_str is None:
                    if protocol == 'scsi':
                        return eachrow.get('scsi_targets')
                    if protocol == 'nvme':
                        return eachrow.get('nvme_targets')
                    if protocol is None:
                        return eachrow.get('total_targets')
            else:
                if mod_str == str(module):
                    if protocol == 'scsi':
                        return eachrow.get('scsi_targets')
                    if protocol == 'nvme':
                        return eachrow.get('nvme_targets')
                    if protocol is None:
                        return eachrow.get('total_targets')
