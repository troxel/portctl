#!/usr/bin/python 

# Turns off Ethernet ports in a switch when a alarm (switch closure detected via GPIO)
# Port numbers and GPIO pins are defined in a json configuration file specified below
# 

from pysnmp.hlapi import *
import json

import RPi.GPIO as GPIO
import time

import pprint
pp = pprint.PrettyPrinter(indent=2)

GPIO.setmode(GPIO.BOARD)

#----------------------------------    
# Configuration... 
#----------------------------------    
conf_file = 'portctl_conf.json'
loop_timer = 20

with open(conf_file) as data_file:  
    pconf = json.load(data_file)

#----------------------------------    
# Define Functions... 
#----------------------------------    
def set_ports(pconf,onoff): 
    cmdint = {'off': 2, 'on':1 }
    
    for sw_set in pconf:
      
        for port_set in sw_set['ports']:
           print("Setting port {} => {}".format(port_set,cmdint[onoff]))
           g = setCmd(SnmpEngine(),
                      CommunityData('Bayview_SNMP_1234$', mpModel=1),
                      UdpTransportTarget((sw_set['ip'], 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus', port_set),cmdint[onoff]))

           errorIndication, errorStatus, errorIndex, varBinds = next(g)

           if errorIndication: print(errorIndication)
           elif errorStatus: print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
           else:
                print("{} {}".format(sw_set['ip'],varBinds[0].prettyPrint()))
  
#----------------------------------    
# Setup... 
#----------------------------------    
state = {}

print("Setup")
print("---------")
for pin in pconf:
    GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("PIN {} configured as Input".format(pin))
    state[pin] = ''
   
print("---------\n")

#----------------------------------    
# Loop
#----------------------------------    
cnt=0
while(1):
      
    for pin in pconf:
        
        # Pin high (true) means the switch is opened 
        if GPIO.input(int(pin)) and state[pin] != 'on':
            set_ports(pconf[pin],'on')
            state[pin] = 'on'
            
        # Pin low (false) means the switch is close 
        elif not GPIO.input(int(pin)) and state[pin] != 'off':
            set_ports(pconf[pin],'off')
            state[pin] = 'off'
    
    print "loop {}".format(cnt)
    time.sleep(loop_timer)
    cnt = cnt + 1
