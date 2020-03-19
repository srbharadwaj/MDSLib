from tests.enablelog import ScriptLog
from tests.enablelog import banner

sl = ScriptLog("switch.log")
log = sl.log

log.info("Starting Test...")

from mdslib.switch import Switch

user = 'admin'
pw = 'nbv!2345'
ip_address = '10.126.94.104'
ip_address1 = '10.126.94.121'

p = 8443

sw104 = Switch(
    ip_address=ip_address,
    username=user,
    password=pw,
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

sw121 = Switch(
    ip_address=ip_address1,
    username=user,
    password=pw,
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

sw = sw121

from mdslib import zone, vsan, fc, portchannel

# v1 = vsan.Vsan(sw, 1)
# z1 = zone.Zone(sw, v1, "zonejdsu")
# print("Zone name is : " + z1.name)
# print("Zone vsan obj is : " + str(z1.vsan))
# print("Zone vsan id is : " + str(z1.vsan.id))
# print("Zone members are : ")
# print(z1.members)
# print("Zone mode is : " + z1.mode)
# time.sleep(10000)
#
# # print("Zone defzone is : " + z1.default_zone) #BUG
# print("Zone defzone is : ")
# while True:
#     o = z1.default_zone
#     print(o)
#     if type(o) is str:
#         break
#
# print("Zone smartzone is : " + z1.smart_zone)
# print("Zone locked is : " + str(z1.locked))
# print("Clearing the lock..")
# z1.clear_lock()
#
# print("Set mode to basic...")
# z1.mode = BASIC
# print("Zone name is : " + z1.name)
# print("Zone mode is : " + z1.mode)
#
# print("Set mode to enhanced...")
# z1.mode = ENHANCED
# print("Zone name is : " + z1.name)
# print("Zone mode is : " + z1.mode)
#
# print("Set mode to invalid value...")
# try:
#     z1.mode = "ASADSDASD"
# except Exception as e:
#     print("Caught correct exception zone mode")
#     print(e.args)
#
# print("Set defzone to deny...")
# z1.default_zone = DENY
# print("Zone name is : " + z1.name)
# print("Zone defzone is : ")
# while True:
#     o = z1.default_zone
#     print(o)
#     if type(o) is str:
#         break
#
# print("Set defzone to permit...")
# z1.default_zone = PERMIT
# import time;
#
# time.sleep(1)
# print("Zone name is : " + z1.name)
# print("Zone defzone is : ")
# while True:
#     o = z1.default_zone
#     print(o)
#     if type(o) is str:
#         break
#
# print("Set defzone to deny...")
# z1.default_zone = DENY
# print("Zone name is : " + z1.name)
# print("Zone defzone is : ")
# while True:
#     o = z1.default_zone
#     print(o)
#     if type(o) is str:
#         break
#
# print("Set defzone to invalid value...")
# try:
#     z1.default_zone = "asdasd"
# except Exception as e:
#     print("Caught correct exception for defzone")
#     print(e.args)
#     s = ""
# print(z1.members)
#


banner("Checking a new vsan's zone")
v = vsan.Vsan(sw, id=456)
v.create()
int12 = fc.Fc(sw, "fc1/2")
int13 = fc.Fc(sw, "fc1/3")
pc1 = portchannel.PortChannel(sw, 1)
pc1.create()
z1 = zone.Zone(sw, v, "zonetemp")
z1.clear_lock()
if z1.name is None:
    print("Zone name is None")
else:
    print("Zone name is " + z1.name)
print("Zone vsan obj is : " + str(z1.vsan))
print("Zone def zone is : " + str(z1.default_zone))
print("Zone mode is : " + str(z1.mode))
print("Zone smartzone is : " + z1.smart_zone)
print("Zone locked is : " + str(z1.locked))
print("Zone members are : ")
print(z1.members)
z1.smart_zone = True
print("Zone smartzone is : " + z1.smart_zone)
z1.smart_zone = False
print("Zone smartzone is : " + z1.smart_zone)

#######################################################
# Create zone
z1.create()
z1.add_members([int12, int13, "somename", "11:22:33:44:55:66:77:88"])
print("Zone members after adding as 'list' are : ")
print(z1.members)
z1.remove_members([int12, "somename", "11:22:33:44:55:66:77:88"])
print("Zone members after removing as 'list' are : ")
print(z1.members)
memlist = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
           {'pwwn': '50:08:01:60:08:9f:4d:01'},
           {'interface': int13.name},
           {'device-alias': 'hello'}, {'ip-address': '1.1.1.1'},
           {'symbolic-nodename': 'symbnodename'},
           {'fwwn': '11:12:13:14:15:16:17:18'}, {'fcid': '0x123456'},
           {'interface': pc1.name},
           {'symbolic-nodename': 'testsymnode'},
           {'fcalias': 'somefcalias'}]
z1.add_members(memlist)
print("Zone members are after adding as 'dict' are : ")
print(z1.members)
memlist = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
           {'pwwn': '50:08:01:60:08:9f:4d:01'},
           {'interface': int13.name},
           {'device-alias': 'hello'}, {'ip-address': '1.1.1.1'},
           {'symbolic-nodename': 'symbnodename'}]
z1.remove_members(memlist)
print("Zone members are after deleting as 'dict' are : ")
print(z1.members)

banner("Running all functions...")
print(z1.__dict__)
print([(name, getattr(z1, name)) for name in dir(z1)])
print(z1.activedb_size)
if z1.name is None:
    print("ERROR!!! Zone name is None, when it should not be none")
else:
    print("Zone name is " + z1.name)
print("Zone vsan obj is : " + str(z1.vsan))

# Delete zone
z1.delete()
if z1.name is None:
    print("Zone name is None")
else:
    print("ERROR!!! zone name should be none but Zone name is " + z1.name)
print("Zone vsan obj is : " + str(z1.vsan))

v.delete()
