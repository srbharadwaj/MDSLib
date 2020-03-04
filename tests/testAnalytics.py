# In this example file we will try to demonstrate the basics of the mdslib library, its APIs and how to use them
# Specifically we will talk about
# Switch
# Fc
# Vsan
# DeviceAlias
from tests.enablelog import ScriptLog

sl = ScriptLog("switch.log")
# sl.consoleHandler.setLevel(logging.DEBUG)
log = sl.log

log.info("Starting Test...")

# First lets import Switch/Fc/DeviceAlias/Vsan classes
from mdslib.switch import Switch
from mdslib.fc import Fc
import time

# Lets set the basic switch inputs
user = 'admin'
pw = 'nbv!2345'
ipaddr = '10.126.94.129'
port = 8443

# ######################################################
# ############# SWITCH SECTION #########################
# Initialize the switch object
sw = Switch(
    ip_address=ipaddr,
    username=user,
    password=pw,
    connection_type='https',
    port=port,
    timeout=30,
    verify_ssl=False)

print(time.asctime())
fcint = Fc(sw, "fc1/45")
ana = fcint.analytics_type
print(ana)
fcint.analytics_type = None
ana = fcint.analytics_type
print(ana)
fcint.analytics_type = 'scsi'
ana = fcint.analytics_type
print(ana)
fcint.analytics_type = 'all'
ana = fcint.analytics_type
print(ana)
fcint.analytics_type = 'nvme'
ana = fcint.analytics_type
print(ana)
print(time.asctime())

scsi_profile = {
    'protocol': 'scsi',
    'metrics': [],
    'view': 'port'
}

scsi_profile_few = {
    'protocol': 'scsi',
    'metrics': ['port', 'total_read_io_count', 'total_write_io_count'],
    'view': 'port'
}

nvme_profile = {
    'protocol': 'nvme',
    'metrics': [],
    'view': 'port'
}

out = sw.create_analytics_query(name="port_query", profile=scsi_profile)
print(out)
out = sw.create_analytics_query(name="port_query_nvme_c_d", profile=nvme_profile, clear=True, differential=True,
                                interval=45)
print(out)
out = sw.show_analytics_query(name="port_query")
print(out)
out = sw.show_analytics_query(name="port_query_nvme_c_d")
print(out)
print(type(out))
# out = sw.delete_analytics_query(name="port_query")
# print(out)
out = sw.show_analytics(profile=scsi_profile_few)
# out = sw.show_analytics(profile=nvme_profile)
print(out)
print(type(out))
out = sw.clear_analytics(profile=nvme_profile)
print(out)
out = sw.purge_analytics(profile=nvme_profile)
print(out)
