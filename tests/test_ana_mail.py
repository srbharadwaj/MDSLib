# First lets import Switch/Fc classes
from mdslib.fc import Fc
from mdslib.switch import Switch

# Lets set the basic switch inputs
user = 'admin'
pw = 'nbv!2345'
ipaddr = '10.126.94.129'
port = 8443

# ############# SWITCH SECTION #########################
# Initialize the switch object
sw129 = Switch(
    ip_address=ipaddr,
    username=user,
    password=pw,
    connection_type='https',
    port=port,
    timeout=30,
    verify_ssl=False)

# ############# FC SECTION #########################
# create an FC interface object for fc1/45
fcint = Fc(sw129, "fc1/45")

# set analytics type scsi on the port
fcint.analytics_type = 'scsi'

# print the analytics type of the port
# output of the below print cmd is
# scsi
print(fcint.analytics_type)

# ############# ANALYTICS SECTION #########################

# Lets create some sample profiles, profiles are simple dict variables
# with keys 'protocol', 'metrics', 'view'

# profile 1
scsi_profile = {
    'protocol': 'scsi',
    'metrics': [],  # default, which is all
    'view': 'port'
}

# profile 2
scsi_profile_few = {
    'protocol': 'scsi',
    'metrics': ['port', 'total_read_io_count', 'total_write_io_count'],
    'view': 'port'
}

# profile 3
nvme_profile = {
    'protocol': 'nvme',
    'metrics': [],
    'view': 'port'
}

# Now lets create ana query with some name for profile 1
# when you execute the below api, the cmd sent is
# analytics query "select all from fc-scsi.port" name port_query type periodic interval 30
# out = sw129.create_analytics_query(name="port_query", profile=scsi_profile)

# Now lets create another query with clear and diff options with profile 3
# when you execute the below api, the cmd sent is
# analytics query "select all from fc-nvme.port" name port_nvme_query type periodic interval 45 clear differential
# out = sw129.create_analytics_query(name="port_nvme_query", profile=nvme_profile, clear=True, differential=True,
#                                   interval=45)

# Now lets see the result for the 2 insalled query
# out_scsi = sw129.show_analytics_query(name="port_query")
# out_nvme = sw129.show_analytics_query(name="port_nvme_query")

# output of the below print cmd is
# {'1': {'port': 'fc1/48', 'scsi_target_count': '2', 'scsi_initiator_count': '0', 'io_app_count': '1',
# 'logical_port_count': '2', 'scsi_target_app_count': '2',
# print(out_scsi)

# output of the below print cmd is
# None
# because nvme was not enabled on the port
# print(out_nvme)

# Let us execute pullquery for profile 2
# cmd sent is
# show analytics query "select port,total_read_io_count,total_write_io_count from fc-scsi.port"
# output of the below print cmd is
# {'1': {'port': 'fc1/48', 'total_read_io_count': '54', 'total_write_io_count': '0', 'sampling_start_time': '1583251527',
# 'sampling_end_time': '1583258496'}, '2': {'port': 'fc1/1', 'total_read_io_count': '61', 'total_write_io_count': '0',
# 'sampling_start_time': '1583251527', 'sampling_end_time': '1583258496'}, '3': {'port': 'fc7/31', 'total_read_io_count':
# '23', 'total_write_io_count': '0', 'sampling_start_time': '1583128928', 'sampling_end_time': '1583258496'},
# '4': {'port': 'fc7/28', 'total_read_io_coun ....
# out = sw129.show_analytics(profile=scsi_profile_few)
# print(out)

# Now lets clear for all the 3 profiles
# sw129.clear_analytics(profile=scsi_profile)
# sw129.clear_analytics(profile=scsi_profile_few)
# sw129.clear_analytics(profile=nvme_profile)

# Now lets purge for all the 3 profiles
# sw129.purge_analytics(profile=scsi_profile)
# sw129.purge_analytics(profile=scsi_profile_few)
# sw129.purge_analytics(profile=nvme_profile)

# Let us delete the installed queries
# sw129.delete_analytics_query(name="port_query")
# sw129.delete_analytics_query(name="port_nvme_query")
#
# # Let us print analytics system load
# load = sw129.show_analytics_load()
# pprint.pprint(load)

anahand = sw129.analytics
# print(anahand.npu_load(1))
# print(anahand.npu_load(7))
# print(anahand.npu_load(1,'scsi'))
# print(anahand.npu_load(7,'scsi'))
# print(anahand.npu_load(1,'nvme'))
# print(anahand.npu_load(7,'nvme'))
print(anahand.targets())
print(anahand.targets(1))
print(anahand.targets(7))
print(anahand.targets(1, 'scsi'))
print(anahand.targets(7, 'scsi'))
print(anahand.targets(1, 'nvme'))
print(anahand.targets(7, 'nvme'))
# print(anahand.initiators())

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
