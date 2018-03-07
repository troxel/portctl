#!/usr/bin/python 

# Turns off Ethernet ports when a alarm (switch closure detected via GPIO)
# Port numbers and GPIO pins are defined in a json configuration file
# When a switch closure is detected there is a configurable delay before turning off the ports

from pysnmp.hlapi import *
import json
import time
import os.path
import signal
import subprocess
import sys

import pprint
pp = pprint.PrettyPrinter(indent=2)

# Raspberry pi modules
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#----------------------------------    
# Command Line Options... 
#----------------------------------    
import argparse
parser = argparse.ArgumentParser(description='Ethernet Port Control')
parser.add_argument("-v",help="Run with standard output",action="store_true")
args = parser.parse_args()
if args.v: print("Verbose Mode Selected")

#----------------------------------    
# Configuration... 
#----------------------------------    
conf_file = 'portctl_conf.json'
Community = open('./community_str.txt','r').read().rstrip()
loop_timer = 10
delay_off_timer = 300

with open(conf_file) as data_file:  
    pconf = json.load(data_file)

if args.v: pp.pprint(pconf)
if args.v: print("Community: {}".format(Community))
#----------------------------------    
# Define Functions... 
#----------------------------------    

#-- Only one one instance of this script to run at a time 
def stop_other_procs():
   
   plst = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
   out,err = plst.communicate()

   pid_self = os.getpid()
   for line in out.splitlines():
      if os.path.basename(sys.argv[0]) in line:
          parts = line.split()
          if int(parts[0]) == pid_self: continue
          os.kill(int(parts[0]), signal.SIGKILL)

#-- Uses SNMP to turn Ether Ports on/off 
def set_ports(pconf,onoff): 
    cmdint = {'off': 2, 'on':1 }
    
    for sw_set in pconf:
      
        for port_set in sw_set['ports']:

           print("Setting port {} => {}".format(port_set,cmdint[onoff]))

           gen_rtn = setCmd(SnmpEngine(),
                      CommunityData(Community, mpModel=1),
                      UdpTransportTarget((sw_set['ip'], 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus', port_set),cmdint[onoff]))

           # The snmp lib creates a 'generator' so use a next to get the return values 
           errorIndication, errorStatus, errorIndex, varBinds = next(gen_rtn)

           if errorIndication: print(errorIndication)
           elif errorStatus: print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
           else:
                print("{} {}".format(sw_set['ip'],varBinds[0].prettyPrint()))
  
#----------------------------------    
# Setup... 
#----------------------------------    
state = {}

#-- stop other process so we can cron this once a day
stop_other_procs()

#-- setup the GPIO ports
for pin in pconf:
    GPIO.setup(int(pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("PIN {} configured as Input".format(pin))
    state[pin] = ''

#----------------------------------    
# Loop Forever...
#----------------------------------    
cnt=0
while(1):
      
    for pin in pconf:
        
        # Pin high (true) means the switch is opened 
        if GPIO.input(int(pin)) and state[pin] != 'on':
            set_ports(pconf[pin],'on')
            state[pin] = 'on'
            
        # Pin low (false) means the switch is closed 
        elif not GPIO.input(int(pin)) and state[pin] != 'off':
            
           # We wait before turning ports off 
           if args.v: print("Detected Closure on GPIO {}".format(pin))
           print "Delaying {} Seconds before shutting down".format(delay_off_timer)
           time.sleep(delay_off_timer)
            
           set_ports(pconf[pin],'off')
           state[pin] = 'off'
    
    if (args.v ): print "loop {}".format(cnt)
    time.sleep(loop_timer)
    cnt = cnt + 1
