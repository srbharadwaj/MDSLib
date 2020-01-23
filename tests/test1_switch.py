# from tests.enablelog import ScriptLog
# from tests.enablelog import banner
# import pprint

from .context import mdslib
from .enablelog import ScriptLog,banner
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
banner("ip, version, model, npv")
print("switch ip addr is   : " + sw.ipaddr)
print("switch version is   : " + sw.version)
print("switch model is     : " + sw.model)
print("switch npv state is : " + str(sw.npv))
banner("end")

banner("switch name ")
oldswname = sw.name
print("old switch name is  : " + oldswname)
print("### Change switch name to say 'swTest' ")
sw.name = 'swTest'
newname = sw.name
print("new switch name is  : " + newname)
print("### Change switch name back to old one ")
sw.name = 'sw-L16-Yushan-121'
print("switch name is  : " + sw.name)
banner("end")

banner("switch modules ")
mods = sw.modules
print("sw.modules returns.. ")
print(mods)
for eachmod in mods:
    print("mod status is    : " + eachmod.status)
    print("mod ports is     : " + str(eachmod.ports))
    print("mod modtype is   : " + eachmod.module_type)
    print("mod model is     : " + eachmod.model)
    print("mod modnumber is : " + str(eachmod.module_number))
    print("")
banner("end")

# modules = sw.modules
# print(vars(sw))
# for eachmod in modules:
#     print(eachmod.module_number, eachmod.model,eachmod.module_type,eachmod.ports,eachmod.status)
# #print(sw.modules)
#
# from mdslib.vsan import Vsan
# v = Vsan(sw,1)
# v.suspend= False
# print(v.state)
#
# #
# # out = sw.config("sh interface fc3/1 transceiver details")
# # print(out)
# # #
# # # banner("Device Alias section ")
#
# from mdslib.fc import Fc
#
# i = Fc(sw,"fc1/1")
# print(i.name)
# print(i.status)
# print(i.out_of_service)
# print(i.description)
#
#
#
#
#


#
# from mdslib.interface import Interface
# i = Interface(sw,"1/1")
# print(i)
# dah = DeviceAlias(sw)
# # facts = dah.__get_facts()

# # facts.pop('device_alias_entries')
# # pprint.pprint(facts)
# pprint.pprint("Mode: "+str(dah.mode))
# dah.mode = 'Enhanced'
# pprint.pprint("Mode: "+str(dah.mode))
# pprint.pprint("Distribute: "+str(dah.distribute))
# dah.distribute = True
# pprint.pprint("Distribute: "+str(dah.distribute))
# print("--- Creating DA with Suhas: 'aa:bb:cc:dd:ee:ff:00:11'")
# out = dah.create(name="Suhas", pwwn="aa:bb:cc:dd:ee:ff:00:11")
# print("Suhas is present? " + str(dah.is_device_alias_present(name="Suhas")))
# print("Suhas1 is present? " + str(dah.is_device_alias_present(name="Suhas1")))


# print("--- Renaming Suhas with Suhas1")
# dah.rename(oldname="Suhas", newname="Suhas1")
# print("Suhas is present? " + str(dah.is_device_alias_present(name="Suhas")))
# print("Suhas1 is present? " + str(dah.is_device_alias_present(name="Suhas1")))
#
# print("--- Deleting Suhas1")
# dah.delete(name="Suhas1")
# print("Suhas is present? " + str(dah.is_device_alias_present(name="Suhas")))
# print("Suhas1 is present? " + str(dah.is_device_alias_present(name="Suhas1")))
#
# facts = dah.__get_facts()
# facts.pop('device_alias_entries')
# pprint.pprint(facts)
# #
# # banner("Vsan section ")
# # v123 = Vsan(switch=sw,name=123)
# # print(v123.__get_facts())
# # err,errstr = v123.create()
# # if err:
# #     print("Creation of Vsan failed")
# #     print(errstr)
# #     exit()
# # v123.add_interfaces(['fc1/8','fc1/9','port-channel 49'])
# # time.sleep(2)
# # print(v123.__get_facts())

'''
banner("Zone section ")
zobj = Zone(sw,vsan=v123.name)
print(zobj.__get_facts())
zobj.mode = 'enhanced'
print(zobj.__get_facts())
err,errstr = zobj.create(name="Zone1")
err,errstr = zobj.create(name="Zone2")
err,errstr =  zobj.add_members(name="Zone2",members=[
    {'device-alias': 'tieHost-77'},
    {'pwwn': '20:10:00:11:0d:6c:6a:00'}
])
print(zobj.zones)
print(zobj.zone_names)
print(zobj.__get_facts())
# err,errstr = zobj.delete(name="Zone1")
# print(zobj.__get_facts())
#zobj.add_members(members=['fc1/6','fc1/8'])


banner("Zoneset section ")
zonesetobj = ZoneSet(sw,vsan=v123.name)
print(zonesetobj.zonesets)
print(zonesetobj.zoneset_names)
print(zonesetobj.active_zoneset)
print(zonesetobj.active_zoneset_name)
zonesetobj.create(name="ZonesetScript")
zonesetobj.add_members(name="ZonesetScript",members=zobj.zone_names)
zonesetobj.activate(name="ZonesetScript")
print(zonesetobj.zonesets)
print(zonesetobj.zoneset_names)
print(zonesetobj.active_zoneset)
print(zonesetobj.active_zoneset_name)

'''

out = """
FC Topology for VSAN 1 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0xe7(231)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0xe7(231)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0xe7(231)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0xe7(231)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13 0x80(128)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31 0xe7(231)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0xe7(231)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0xe7(231)          fc17/42  10.126.94.175(sw175-Luke-18slot)
   port-channel47 0xe3(227)   port-channel47  10.126.94.217(sw217-Ishan-new-L14)

FC Topology for VSAN 10 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0x9f(159)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0x9f(159)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0x9f(159)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0x9f(159)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13  0x60(96)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31 0x9f(159)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0x9f(159)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0x9f(159)          fc17/42  10.126.94.175(sw175-Luke-18slot)
   port-channel47  0x10(16)   port-channel47  10.126.94.217(sw217-Ishan-new-L14)

FC Topology for VSAN 11 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7  0x47(71)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46  0x47(71)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1  0x47(71)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3  0x47(71)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13 0x92(146)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31  0x47(71)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41  0x47(71)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42  0x47(71)          fc17/42  10.126.94.175(sw175-Luke-18slot)
   port-channel47 0x73(115)   port-channel47  10.126.94.217(sw217-Ishan-new-L14)

FC Topology for VSAN 20 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0xee(238)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0xee(238)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0xee(238)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0xee(238)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/31 0xee(238)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0xee(238)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0xee(238)          fc17/42  10.126.94.175(sw175-Luke-18slot)
   port-channel47 0xef(239)   port-channel47  10.126.94.217(sw217-Ishan-new-L14)

FC Topology for VSAN 121 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0xde(222)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0xde(222)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0xde(222)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0xde(222)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13 0xca(202)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31 0xde(222)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0xde(222)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0xde(222)          fc17/42  10.126.94.175(sw175-Luke-18slot)

FC Topology for VSAN 221 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0xa9(169)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0xa9(169)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0xa9(169)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0xa9(169)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13 0x8e(142)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31 0xa9(169)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0xa9(169)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0xa9(169)          fc17/42  10.126.94.175(sw175-Luke-18slot)

FC Topology for VSAN 222 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0xc8(200)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0xc8(200)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0xc8(200)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0xc8(200)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/13 0x85(133)           fc1/57  10.126.94.121(sw-L16-Yushan-121)
           fc6/31 0xc8(200)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0xc8(200)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0xc8(200)          fc17/42  10.126.94.175(sw175-Luke-18slot)

FC Topology for VSAN 666 :
--------------------------------------------------------------------------------
       Interface  Peer Domain Peer Interface     Peer IP Address(Switch Name)
--------------------------------------------------------------------------------
            fc1/7 0x6a(106)          fc13/19  10.126.94.175(sw175-Luke-18slot)
           fc1/46 0x6a(106)          fc18/13  10.126.94.175(sw175-Luke-18slot)
            fc6/1 0x6a(106)          fc18/45  10.126.94.175(sw175-Luke-18slot)
            fc6/3 0x6a(106)          fc13/33  10.126.94.175(sw175-Luke-18slot)
           fc6/31 0x6a(106)           fc13/3  10.126.94.175(sw175-Luke-18slot)
           fc6/41 0x6a(106)          fc17/41  10.126.94.175(sw175-Luke-18slot)
           fc6/42 0x6a(106)          fc17/42  10.126.94.175(sw175-Luke-18slot) 

"""

#
# from mdslib.fabric import Fabric
#
# f = Fabric("new")
# swlist = f.discover_all_switches_in_fabric(seed_switch_ip='10.126.94.175',
#     username=user,
#     password=pw,
#     connection_type='https',
#     port=p,
#     timeout=30,
#     verify_ssl=False,
#     discover_npv=True)
#
# pprint.pprint(swlist)
