# In this example file we will try to demonstrate the basics of the mdslib library, its APIs and how to use them
# Specifically we will talk about
# Switch
# Fc
# Vsan
# DeviceAlias

from mdslib.devicealias import DeviceAlias
from mdslib.fc import Fc
# First lets import Switch/Fc/DeviceAlias/Vsan classes
from mdslib.switch import Switch
from mdslib.vsan import Vsan


# Lets set the basic switch inputs
user = 'admin'
pw = 'nbv!2345'
ipaddr = '10.126.94.104'
port = 8443

# ######################################################
# ############# SWITCH SECTION #########################
# Initialize the switch object
sw = Switch(
    ip_address=ipaddr,
    username=user,
    password=pw,
    connection_type='https',
    port=port,
    timeout=30,
    verify_ssl=False)
cmd = "show hardware internal errors all "
try:
    out = sw.show(cmd, raw_text=False)
    print(out)
except Exception as e:
    print("EXCEPTION!!!")
    # print(e.args)
    out = sw.show(cmd, raw_text=False)
    print(out)

sshcode = """
def ssh():
    sw._ssh_handle.show("show version")
"""
nxapishow = """
def nxapi():
    sw.show("show version")
"""
nxapiapi = """
def nxapi():
    sw.version
"""
nxapishowrawtext = """
def nxapi():
    sw.show("show version",raw_text=True)
"""

# def nxapi():
#     o = sw.show("show version")
#     print(o)
# def nxapi():
#     o = sw.show("show version")
#     print(o)

import timeit

from datetime import datetime

now = datetime.now().time()
print("now =", now)
print(timeit.timeit(stmt=sshcode, globals=globals()))
now = datetime.now().time()
print("now =", now)
print(timeit.timeit(stmt=nxapiapi, globals=globals()))
now = datetime.now().time()
print("now =", now)

exit()
# Get basic information of the switch
print("ip    : " + sw.ipaddr)
print("name  : " + sw.name)
print("ver   : " + sw.version)
print("model : " + sw.model)
print(sw.__dict__)
print("Sw interfaces: ")
print(sw.interfaces)
print(sw.feature('analytics'))
sw.feature('analytics', True)
print(sw.feature('analytics'))
sw.feature('nxapi', False)
print(sw.feature('analytics'))
print(sw.cores)

exit()
# #######################################
# Output of the above prints are as follows
# #######################################
# ip    : 10.126.94.121
# name  : _sw-L16-Yushan-121.cisco.com
# ver   : 8.4(2u)
# model : MDS 9396T 96X32G FC (2 RU) Chassis
# #######################################

# Let us change the switchname
sw.name = "MyNewSwitch"

# Print the new switch name
print("name : " + sw.name)

# #######################################
# Output of the above print is as follows
# #######################################
# name : MyNewSwitch.cisco.com
# #######################################

# Let us change the switchname back to the old one
sw.name = "sw-L16-Yushan-121"

# Print the switch name
print("name : " + sw.name)

# #######################################
# Output of the above print is as follows
# #######################################
# name : _sw-L16-Yushan-121.cisco.com
# #######################################


# ######################################################
# ############# FC Interface SECTION ###################

# Lets create an FC interface object for fc127/1
fcint = Fc(sw, 'fc1/1')

# Get basic information of this FC interface
print("name : " + fcint.name)
print("mode : " + fcint.mode)
print("speed : " + fcint.speed)
print("trunk : " + fcint.trunk)
print("status : " + fcint.status)

# #######################################
# Output of the above prints are as follows
# #######################################
# name : fc127/1
# mode : TE
# speed : 32
# trunk : on
# status : trunking
# #######################################


# ####################################################
# ############# VSAN SECTION #########################
# Now let check how we can work with Vsans

# Here we are creating an object of vsan with id 2
v2 = Vsan(sw, 2)

# Now lets create the vsan on the switch
v2.create(name="TestVsan2")

# Lets get the basic info of this vsan
print("id    : " + str(v2.id))
print("name  : " + v2.name)
print("state : " + v2.state)

# #######################################
# Output of the above prints are as follows
# #######################################
# id    : 2
# name  : TestVsan2
# state : active
# #######################################

# Let us suspend the vsan
v2.suspend = True

# Lets get the basic info of this vsan
print("id    : " + str(v2.id))
print("name  : " + v2.name)
print("state : " + v2.state)

# #######################################
# Output of the above prints are as follows
# #######################################
# id    : 2
# name  : TestVsan2
# state : suspended
# #######################################

# Let us no-suspend the vsan
v2.suspend = False

# Lets get the basic info of this vsan
print("id    : " + str(v2.id))
print("name  : " + v2.name)
print("state : " + v2.state)

# #######################################
# Output of the above prints are as follows
# #######################################
# id    : 2
# name  : TestVsan2
# state : active
# #######################################

# Lets delete the vsan
v2.delete()

# ###########################################################
# ############# DEVICEALIAS SECTION #########################
# Now let check how we can work with DeviceAlias

# First lets create a devicealias object
d = DeviceAlias(sw)

# Lets get the basic info of device-alias
print("Device alias mode :         " + d.mode)
print("Device alias distribution : " + str(d.distribute))
print("Device alias locked? : " + str(d.locked))
print("Device alias entries : " + str(d.database))

# #######################################
# Output of the above prints are as follows
# #######################################
# Device alias mode :         Enhanced
# Device alias distribution : True
# Device alias locked? : False
# Device alias entries : {'t12': '50:06:01:01:0e:00:01:ff',
#                          'p1test': '10:00:10:10:10:10:00:00',
#                          'test1_add': '56:02:22:11:22:88:11:67',
#                          'test2_add': '65:22:22:11:22:22:11:0d',
#                                  .
#                                  .
#                                  . }
# #######################################

# Lets create a couple of new entries.....
# Define the new pairs in a dict format
newdapairs = {'t123': '60:66:61:01:0e:00:01:ff',
              'danewtest': '60:66:61:01:0e:00:01:fe'}
# Pass the dict to the create api
d.create(newdapairs)

# Lets delete an entry
# pass the alias name to be deleted to teh delete api
d.delete('t12')

# Lets rename an entry, by passing the oldname and newname
d.rename(oldname='test1_add', newname='test1_renamed')

# Lets get device-alias database
print("Device alias entries :  " + str(d.database))

# #######################################
# Output of the above prints are as follows
# #######################################
# Device alias entries :  {'p1test': '10:00:10:10:10:10:00:00',
#                          't123': '60:66:61:01:0e:00:01:ff',
#                          'danewtest': '60:66:61:01:0e:00:01:fe',
#                          'test1_renamed': '56:02:22:11:22:88:11:67',
#                          'test2_add': '65:22:22:11:22:22:11:0d',
#                                  .
#                                  .
#                                  . }
# #######################################

# As you can see above all the operation of create/delete/rename are done
