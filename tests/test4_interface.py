from tests.enablelog import ScriptLog
from tests.enablelog import banner
import time
import pprint
import logging

sl = ScriptLog("switch.log",consolelevel=logging.INFO)
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

from mdslib.fc import Fc
from mdslib.portchannel import PortChannel

fobj = Fc(sw, name="fc1/57")

banner("Get info about interface fc1/57")
print("Desc: " + fobj.description)
print("Mode: " + fobj.mode)
print("Name: " + fobj.name)
print("Speed: " + fobj.speed)
print("Status: " + fobj.status)
print("Trunk: " + fobj.trunk)
fobj.description = "Setting test interface desc via script"
fobj.status = "no shutdown"
fobj.trunk = "auto"
fobj.mode = "E"
fobj.speed = "auto"
time.sleep(2)
print("Desc: " + fobj.description)
print("Mode: " + fobj.mode)
print("Name: " + fobj.name)
print("Speed: " + fobj.speed)
print("Status: " + fobj.status)
print("Trunk: " + fobj.trunk)
# from mdslib.interface import Interface
# i = Interface(sw)



banner(" PortChannel section")
# Lets play with port-channel
pc22 = PortChannel(switch=sw,id=22)
pc22.create()
pc22.description = "This is a sample pc description"
banner("Get info about interface pc22")
print("Desc: " + pc22.description)
print("Mode: " + pc22.mode)
print("Name: " + pc22.name)
print("Speed: " + pc22.speed)
print("Status: " + pc22.status)
print("Trunk: " + pc22.trunk)
pc22.delete()