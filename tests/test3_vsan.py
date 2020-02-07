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
from mdslib.fc import Fc

banner("Creating vsan 98 and 99")
v98 = Vsan(switch=sw, id=98)
v99 = Vsan(switch=sw, id=99)
v98.create("98thVsan")
v99.create("99thVsan")
banner("end")
print()
v1 = Vsan(switch=sw, id=1)
print("Vsan 1 interfaces are..")
print(v1.interfaces)

# Lets create fc interface object for fc127/11,fc127/12,fc127/13
fc11 = Fc(switch=sw, name="fc127/11")
fc12 = Fc(switch=sw, name="fc127/12")
fc13 = Fc(switch=sw, name="fc127/13")
v98.add_interfaces([fc11])
v99.add_interfaces([fc12, fc13])

banner("Get info about vsan 98 and 99")
print("Vsan id    : " + str(v98.id))
print("Vsan name  : " + v98.name)
print("Vsan state : " + v98.state)
print("Vsan interfaces : ")
print(v98.interfaces)
print("Vsan id    : " + str(v99.id))
print("Vsan name  : " + v99.name)
print("Vsan state : " + v99.state)
print("Vsan interfaces : ")
print(v99.interfaces)
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
print(v99.interfaces)
banner("end")
print()
v99.add_interfaces(["asdsa"])
