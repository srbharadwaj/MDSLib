import logging
import pprint

import time

from mdslib import constants
from mdslib.fc import Fc
from mdslib.portchannel import PortChannel
from mdslib.switch import Switch
from tests.enablelog import ScriptLog
from tests.enablelog import banner

sl = ScriptLog("switch.log", consolelevel=logging.INFO)
log = sl.log
log.info("Starting Test...")

user = 'admin'
pw = 'nbv!2345'
ip_address = '10.126.94.218'
ip_address1 = '10.126.94.121'
p = 8443

sw218 = Switch(
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

banner(" PortChannel section")
banner("Create PC22 in sw121")
# Lets play with port-channel
pc22_121 = PortChannel(switch=sw121, id=22)
pc22_121.create()

pc22_121.description = "This is a sample pc description"
banner("Get info about interface pc22_121")
print("Desc: " + pc22_121.description)
print("Mode: " + pc22_121.mode)
print("Name: " + pc22_121.name)
print("Speed: " + pc22_121.speed)
print("Status: " + pc22_121.status)
print("Trunk: " + pc22_121.trunk)
pc22_121.channel_mode = "active"
print("Ch-Mode: " + pc22_121.channel_mode)
pc22_121.channel_mode = "ON"
print("Ch-Mode: " + pc22_121.channel_mode)
print("PC Members:..")
pprint.pprint(pc22_121.members)

fc153 = Fc(sw121, name="fc1/53")
pc22_121.add_members([fc153])
print("PC Members:..")
pprint.pprint(pc22_121.members)

banner("Create PC22 in sw218")
# Lets play with port-channel
pc22_218 = PortChannel(switch=sw218, id=22)
pc22_218.create()
pc22_218.description = "This is a sample pc description"
banner("Get info about interface pc22_218")
print("Desc: " + pc22_218.description)
print("Mode: " + pc22_218.mode)
print("Name: " + pc22_218.name)
print("Speed: " + pc22_218.speed)
print("Status: " + pc22_218.status)
print("Trunk: " + pc22_218.trunk)
pc22_218.channel_mode = "active"
print("Ch-Mode: " + pc22_218.channel_mode)
pc22_218.channel_mode = "ON"
print("Ch-Mode: " + pc22_218.channel_mode)
print("PC Members:..")
pprint.pprint(pc22_218.members)

fc1 = Fc(sw218, name="fc1/27")
fc2 = Fc(sw218, name="fc1/28")
pc22_218.add_members([fc1, fc2])
pprint.pprint(pc22_218.members)

fc153.status = constants.NO_SHUTDOWN
fc1.status = constants.NO_SHUTDOWN
time.sleep(10)

banner("Print status now")
banner("Get info about interface pc22_121")
print("Desc: " + pc22_121.description)
print("Mode: " + pc22_121.mode)
print("Name: " + pc22_121.name)
print("Speed: " + pc22_121.speed)
print("Status: " + pc22_121.status)
print("Trunk: " + pc22_121.trunk)
pc22_121.channel_mode = "active"
print("Ch-Mode: " + pc22_121.channel_mode)
pc22_121.channel_mode = "ON"
print("Ch-Mode: " + pc22_121.channel_mode)
# pprint.pprint(pc22_218.counters)
pprint.pprint(pc22_121.members)
banner("Get info about interface pc22_218")
print("Desc: " + pc22_218.description)
print("Mode: " + pc22_218.mode)
print("Name: " + pc22_218.name)
print("Speed: " + pc22_218.speed)
print("Status: " + pc22_218.status)
print("Trunk: " + pc22_218.trunk)
pc22_218.channel_mode = "active"
print("Ch-Mode: " + pc22_218.channel_mode)
pc22_218.channel_mode = "ON"
print("Ch-Mode: " + pc22_218.channel_mode)
# pprint.pprint(pc22_218.counters)
pprint.pprint(pc22_218.members)

banner("Now remove the PC members")
pc22_121.remove_members([fc153])
pc22_218.remove_members([fc1])

fc153.status = constants.NO_SHUTDOWN
fc1.status = constants.NO_SHUTDOWN

pprint.pprint(pc22_218.members)
pprint.pprint(pc22_121.members)

pc22_121.delete()
pc22_218.delete()

fc153.status = constants.NO_SHUTDOWN
fc1.status = constants.NO_SHUTDOWN
time.sleep(30)

print(fc153.status)
print(fc1.status)

print(pc22_121.status)
print(pc22_218.status)
