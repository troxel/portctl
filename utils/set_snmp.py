from pysnmp.hlapi import *

import pprint
pp = pprint.PrettyPrinter(indent=2)

g = setCmd(SnmpEngine(),
           CommunityData('Bayview_SNMP_1234$', mpModel=1),
           UdpTransportTarget(('130.46.87.137', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus', 2),2))

pp.pprint(next(g))


errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('Bayview_SNMP_1234$', mpModel=1),
           UdpTransportTarget(('130.46.87.137', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', 2)))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
