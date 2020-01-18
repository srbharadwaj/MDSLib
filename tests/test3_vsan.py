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

# sw104 = Switch(
#     ip_address=ip_address,
#     username=user,
#     password=pw,
#     connection_type='https',
#     port=p,
#     timeout=30,
#     verify_ssl=False)

sw121 = Switch(
    ip_address=ip_address1,
    username=user,
    password=pw,
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

sw = sw121

from mdslib.vsan import Vsan

banner("Creating vsan 98 and 99")
v98 = Vsan(switch=sw, id=98)
v99 = Vsan(switch=sw, id=99)
v98.create("98thVsan")
v99.create("99thVsan")
banner("end")
print()

banner("Get info about vsan 98 and 99")
print("Vsan id    : " + str(v98.id))
print("Vsan name  : " + v98.name)
print("Vsan state : " + v98.state)
print("Vsan id    : " + str(v99.id))
print("Vsan name  : " + v99.name)
print("Vsan state : " + v99.state)
banner("end")
print()

banner("set suspend as True for vsan 98")
v98.suspend = True
print("Vsan id    : " + str(v98.id))
print("Vsan name  : " + v98.name)
print("Vsan state : " + v98.state)
banner("set suspend as False for vsan 98")
v98.suspend = False
print("Vsan id    : " + str(v98.id))
print("Vsan name  : " + v98.name)
print("Vsan state : " + v98.state)
banner("end")
print()

banner("Del vsan 98/99")
v98.delete()
print("Vsan id    : " + str(v98.id))
print("Vsan name  : " + str(v98.name))
print("Vsan state : " + str(v98.state))
v99.delete()
print("Vsan id    : " + str(v99.id))
print("Vsan name  : " + str(v99.name))
print("Vsan state : " + str(v99.state))
banner("end")
print()
