from pysnmp.hlapi import *
from pprint import pprint

t = ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', 3))


errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           #CommunityData('Bayview_SNMP_1234$', mpModel=0),
           CommunityData('Bayview_SNMP_1234$', mpModel=1),
           UdpTransportTarget(('130.46.87.137', 161)),
           ContextData(),
           #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
           #ObjectType(ObjectIdentity('IF-MIB', 'ifDescr', 0)))
           ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', 2)),
           ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', 1)),
           t
           )
)


if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:

        
        print(varBind)
        #print(varBind.prettyPrint())
               
        #print(' = '.join([x.prettyPrint() for x in varBind]))
