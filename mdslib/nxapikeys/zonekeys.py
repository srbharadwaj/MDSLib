# This file contains NXAPI keys for zone and zoneset
# show zone status vsan <>
# show zone name vsan <>
# show zoneset name vsan <>

NAME = 'name'
VSAN_ID = 'vsan_id'
DEFAULT_ZONE = 'default_zone'
DISTRIBUTE = 'distribute'
INTEROP = 'interop'
MODE = 'mode'
MERGE_CONTROL = 'merge_control'
SESSION = 'session'
SMART_ZONE = 'smart_zoning'
ZONE_DETAILS = 'zone_details'
FULLDB_SIZE = "fulldb_dbsize"
FULLDB_ZSC = "fulldb_zoneset_count"
FULLDB_ZC = "fulldb_zone_count"
ACTIVEDB_SIZE = "activedb_dbsize"
ACTIVEDB_ZSN = "activedb_zoneset_name"
ACTIVEDB_ZSC = "activedb_zoneset_count"
ACTIVEDB_ZC = "activedb_zone_count"
EFFDB_SIZE = "effectivedb_dbsize"
MAXDB_SIZE = "maxdb_dbsize"
EFFDB_PER = "percent_effectivedbsize"
STATUS = "status"

# ZONE_MEMBERS = ['TABLE_zone_member']['ROW_zone_member']
ZONE_MEMBER_TYPE = 'type'
ZONE_MEMBER_WWN = 'wwn'
ZONE_MEMBER_INTERFACE = 'intf_fc'
ZONE_MEMBER_DEVALIAS = 'dev_alias'
ZONE_MEMBER_IPADDR = 'ipaddr'
ZONE_MEMBER_SYMNODENAME = 'symnodename'
ZONE_MEMBER_FWWN = 'wwn'
ZONE_MEMBER_SWWN = 'wwn'
ZONE_MEMBER_FCID = 'fcid'
ZONE_MEMBER_INTERFACE_PC = 'intf_port_ch'
ZONE_MEMBER_FCALIAS = 'fcalias_name'
ZONE_MEMBER_FCALIAS_VSANID = 'fcalias_vsan_id'

# Valid zone members
VALID_MEMBERS = {
    'pwwn': 'wwn',
    'interface': 'intf',
    'device-alias': 'dev_alias',
    'ip-address': 'ipaddr',
    'symbolic-nodename': 'symnodename',
    'fwwn': 'wwn',
    'fcid': 'fcid',
    'fcalias': 'fcalias_name'
}
