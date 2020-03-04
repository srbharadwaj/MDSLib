import logging

log = logging.getLogger(__name__)

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

METRICS = 'metrics'
PROTOCOL = 'protocol'
VIEW = 'view'


def _validate_profile(profile):
    # TODO
    # LIMITATIONS:
    # Need to do validation for profiles
    # Does not support where clause for now

    return True


def _get_select_query_string(profile):
    metrics = profile.get(METRICS, None)
    if (metrics is None) or (len(metrics) == 0):
        selq = "select all from fc-" + profile.get(PROTOCOL) + "." + profile.get(VIEW)
    else:
        allmetrics = ','.join(metrics)
        selq = "select " + allmetrics + " from fc-" + profile.get(PROTOCOL) + "." + profile.get(VIEW)
    return selq


def create_analytics_query(sw, name, profile, clear=False, differential=False, interval=30):
    if _validate_profile(profile):
        selq = _get_select_query_string(profile)
        cmd = 'analytics query "' + selq + '" name ' + name + " type periodic interval " + str(interval)
        if clear:
            if differential:
                cmd = cmd + " clear differential"
            else:
                cmd = cmd + " clear"
        elif differential:
            cmd = cmd + " differential"
        log.info("Cmd to be sent is " + cmd)
        return sw._ssh_handle.config(cmd)


def delete_analytics_query(sw, name):
    cmd = "no analytics name " + name
    log.info("Cmd to be sent is " + cmd)
    return sw._ssh_handle.config(cmd)


def show_analytics_query(sw, name):
    cmd = "show analytics query name " + name + " result"
    log.info("Cmd to be sent is " + cmd)
    return sw._ssh_handle.show(cmd)


def show_analytics(sw, profile, clear=False, differential=False):
    if _validate_profile(profile):
        selq = _get_select_query_string(profile)
        cmd = 'show analytics query "' + selq + '"'
        if clear:
            cmd = cmd + " clear "
            if differential:
                cmd = cmd + " differential "
        elif differential:
            cmd = cmd + " differential "
        log.info("Cmd to be sent is " + cmd)
        return sw._ssh_handle.show(cmd)


def clear_analytics(sw, profile):
    if _validate_profile(profile):
        selq = _get_select_query_string(profile)
        cmd = 'clear analytics query "' + selq + '"'
        log.info("Cmd to be sent is " + cmd)
        return sw._ssh_handle.config(cmd)


def purge_analytics(sw, profile):
    if _validate_profile(profile):
        selq = _get_select_query_string(profile)
        purgecmd = 'purge analytics query "' + selq + '"'
        cmd = "terminal dont-ask ; " + purgecmd + " ; no terminal dont-ask"
        log.info("Cmd to be sent is " + cmd)
        return sw._ssh_handle.config(cmd)
