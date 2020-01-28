from tests.enablelog import ScriptLog
from tests.enablelog import banner
import pprint

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

from mdslib import zone, vsan
from mdslib.constants import BASIC, ENHANCED, PERMIT, DENY

v1 = vsan.Vsan(sw, 1)
z1 = zone.Zone(sw, v1, "zonejdsu")
print("Zone name is : " + z1.name)
print("Zone vsan obj is : " + str(z1.vsan))
print("Zone vsan id is : " + str(z1.vsan.id))
print("Zone members are : ")
print(z1.members)
print("Zone mode is : " + z1.mode)

# print("Zone defzone is : " + z1.default_zone) #BUG
print("Zone defzone is : ")
while True:
    o = z1.default_zone
    print(o)
    if type(o) is str:
        break

print("Zone smartzone is : " + z1.smart_zone)
print("Zone locked is : " + str(z1.locked))
print("Clearing the lock..")
z1.clear_lock()

print("Set mode to basic...")
z1.mode = BASIC
print("Zone name is : " + z1.name)
print("Zone mode is : " + z1.mode)

print("Set mode to enhanced...")
z1.mode = ENHANCED
print("Zone name is : " + z1.name)
print("Zone mode is : " + z1.mode)

print("Set mode to invalid value...")
try:
    z1.mode = "ASADSDASD"
except Exception as e:
    print("Caught correct exception zone mode")
    print(e.args)

print("Set defzone to deny...")
z1.default_zone = DENY
print("Zone name is : " + z1.name)
print("Zone defzone is : ")
while True:
    o = z1.default_zone
    print(o)
    if type(o) is str:
        break

print("Set defzone to permit...")
z1.default_zone = PERMIT
import time;

time.sleep(1)
print("Zone name is : " + z1.name)
print("Zone defzone is : ")
while True:
    o = z1.default_zone
    print(o)
    if type(o) is str:
        break

print("Set defzone to deny...")
z1.default_zone = DENY
print("Zone name is : " + z1.name)
print("Zone defzone is : ")
while True:
    o = z1.default_zone
    print(o)
    if type(o) is str:
        break

print("Set defzone to invalid value...")
try:
    z1.default_zone = "asdasd"
except Exception as e:
    print("Caught correct exception for defzone")
    print(e.args)
    s = ""
