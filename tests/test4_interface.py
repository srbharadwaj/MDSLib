import logging

import time

from tests.enablelog import ScriptLog
from tests.enablelog import banner

sl = ScriptLog("switch.log", consolelevel=logging.INFO)
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

sw218 = Switch(
    ip_address="10.126.94.218",
    username=user,
    password=pw,
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

sw121 = Switch(
    ip_address=ip_address1,
    # ip_address='10.197.155.110',
    username=user,
    password=pw,
    # password='nbv_!2345*',
    connection_type='https',
    port=p,
    timeout=30,
    verify_ssl=False)

sw = sw121

from mdslib.fc import Fc

fobj = Fc(sw, name="fc1/1")
# fobj.description = "Desc test"
fobj.description = "123 Description of maximum 254 charactersDescription of maximum 254 charactersDescription of maximum 254 charactersDescription of maximum 254 charactersDescription of maximum 254 charactersDescription of maximum 254 charactersDescription of maximum 254 c"
print(fobj.description)
# time.sleep(1000000)
fobj.out_of_service = True
print(fobj.status)
fobj.out_of_service = False
print(fobj.status)
print(fobj.transceiver.sfp_present)
print(fobj.transceiver.bit_rate)
print(fobj.transceiver.min_speed)
print(fobj.transceiver.max_speed)
print(fobj.transceiver.name)
print(fobj.transceiver.part_number)
print(fobj.transceiver.voltage)
print(fobj.transceiver.current)
print(fobj.transceiver.temperature)
print(fobj.transceiver.tx_power)
print(fobj.transceiver.rx_power)

fobj1 = Fc(sw, name="fc1/4")
print(fobj1.counters)
print(fobj1.counters.brief)
print(fobj1.counters.total_stats)
print(fobj1.counters.congestion_stats)
print(fobj1.counters.link_stats)
print(fobj1.counters.loop_stats)
print(fobj1.counters.other_stats)

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


# banner(" PortChannel section")
# banner("Checking PC 22")
# # Lets play with port-channel
# pc22 = PortChannel(switch=sw, id=22)
# pc22.create()
# pc22.description = "This is a sample pc description"
# banner("Get info about interface pc22_218")
# print("Desc: " + pc22.description)
# print("Mode: " + pc22.mode)
# print("Name: " + pc22.name)
# print("Speed: " + pc22.speed)
# print("Status: " + pc22.status)
# print("Trunk: " + pc22.trunk)
# pc22.channel_mode = "active"
# print("Ch-Mode: " + pc22.channel_mode)
# pc22.channel_mode = "ON"
# print("Ch-Mode: " + pc22.channel_mode)
# #pprint.pprint(pc22_218.counters)
# pprint.pprint(pc22.members)
#
# fc11 = Fc(sw,name="fc127/53")
# pc22.add_members([fc11])
# fc11.status = constants.NO_SHUTDOWN
# pprint.pprint(pc22.members)
# #time.sleep(120)
# pc22.delete()
# fc11.status = constants.NO_SHUTDOWN
#
# banner("Checking PC 21")
# pc21 = PortChannel(switch=sw, id=21)
# print("Desc: " + pc21.description)
# print("Mode: " + pc21.mode)
# print("Name: " + pc21.name)
# print("Speed: " + pc21.speed)
# print("Status: " + pc21.status)
# print("Trunk: " + pc21.trunk)
# print("Ch-Mode: " + pc21.channel_mode)
# mem = pc21.members
# pprint.pprint(mem)
# for eachmem in mem:
#     print(eachmem.name)
