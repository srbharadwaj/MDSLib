from tests.enablelog import ScriptLog, banner

sl = ScriptLog("switch.log")
# sl.consoleHandler.setLevel(logging.DEBUG)
log = sl.log

log.info("Starting Test...")

from mdslib.switch import Switch

user = 'admin'
pw = 'nbv!2345'
ip_address = '10.126.94.104'
ip_address1 = '10.126.94.185'

p = 8443

# sw104 = Switch(
#     ip_address=ip_address,
#     username=user,
#     password=pw,
#     connection_type='https',
#     port=p,
#     timeout=30,
#     verify_ssl=False)

sw = Switch(
    ip_address=ip_address,
    username=user,
    password=pw,
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

from mdslib.devicealias import DeviceAlias
from mdslib import constants

banner(sw.ipaddr)
d = DeviceAlias(sw)

print("Check if invalid mode raises exception")
try:
    d.mode = "asdsa"
except Exception as e:
    print("Caught correct exception")
    print(e.args)

print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))

print("Setting Device alias distribution to False...")
d.distribute = False
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))

print("Setting Device alias distribution to True...")
d.distribute = True
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))

# print("Deleting device alias entries...")
# d.delete("tieHost-1052-Suhas-Rename")
# d.delete("tieHost-1052")

# print("Rename device alias entries...")
# # oldName already present
# d.rename('tieHost-1053', 'tieHost-1052')
# # newName already present
# d.rename('tieHost-1053', 'tieHost-1052')
# # correct rename
# d.rename('tieHost-1053', 'tieHost-1052-Suhas-Rename')

# d.clear_lock()
# d.distribute = 1234
# d.clear_database()
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))

d.distribute = True
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))

print("Creating new pairs...entries...")
newdapairs = {'t123123': '60:67:62:01:0e:00:01:ff',
              'danewtest': '60:66:61:01:0e:00:01:fe'}
# Pass the dict to the create api
d.create(newdapairs)

# print("Clear device alias database...")
# d.clear_database()
# print("Device alias mode :          " + d.mode)
# print("Device alias distribution :  " + str(d.distribute))
# print("Device alias locked? :  " + str(d.locked))
# print("Device alias entries :  " + str(d.database))
print("Adding device alias entries...")
da = {'^!@h189-dell-windell-windows9-dell--wbottom-p2': '21:01:00:1b:32:aa:ff:4a',
      'h189-dell-windows-bottom-p3': '21:02:00:1b:32:ca:ff:4a',
      'h189-dell-windows-bottom-p4': '21:03:00:1b:32:ea:ff:4a'}
# da = {'t12': '50:06:01:01:0e:00:01:ff', 'p1test': '10:00:10:10:10:10:00:00', 'test1_add': '56:02:22:11:22:88:11:67', 'test2_add': '65:22:22:11:22:22:11:0d'}
d.create(da)

print("Setting Device alias distribution to True....")
d.distribute = True
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
print("Device alias entries :  " + str(d.database))

# print("Setting Device alias mode to Basic")
# d.mode = constants.BASIC
# print("Device alias mode :          " + d.mode)
# print("Device alias distribution :  " + str(d.distribute))

print("Setting Device alias mode to Enhanced....")
d.mode = constants.ENHANCED
print("Device alias mode :          " + d.mode)
print("Device alias distribution :  " + str(d.distribute))
print("Device alias locked? :  " + str(d.locked))
print("Device alias entries :  " + str(d.database))
# d.mode = constants.BASIC
# print(d.mode)
