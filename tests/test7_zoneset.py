from mdslib import constants
from tests.enablelog import ScriptLog

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

from mdslib.zoneset import ZoneSet
from mdslib.vsan import Vsan
from mdslib.zone import Zone
from mdslib.fc import Fc

int14 = Fc(sw, "fc1/4")
int15 = Fc(sw, "fc1/5")

v = Vsan(switch=sw, id=456)
v.create()
v.add_interfaces([int14, int15])

z1 = Zone(sw, v, "zonetemp")
z2 = Zone(sw, v, "zonetemp_int")
z1.mode = constants.ENHANCED
z1.create()
z2.create()
z1.add_members(["somename", "11:22:33:44:55:66:77:88"])
z2.add_members([int14, int15])

zs = ZoneSet(switch=sw, vsan_obj=v, name="scriptZoneset")
zs.create()
print(zs.vsan)
print(zs.name)
print("Members before - no mem:")
print(zs.members)
zs.add_members([z1])

print("Members before - after one add:")
print(zs.members)
print("Members before - after second add:")
zs.add_members([z2])
print(zs.members)
print("Is the zs active?should be False")
print(zs.is_active())
print("Activating ZS")
zs.activate()
print("Is the zs active?should be True")
print(zs.is_active())
print("Deactivating ZS")
zs.activate(action=False)
print("Is the zs active?should be False")
print(zs.is_active())
zs.delete()
print(zs.name)

v.delete()
