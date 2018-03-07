# portctl.py Port Control. 

Shutdown Ethernet ports on an Ethernet switch in response to a detected 
switch closure on GPIO pins on a Raspberry pi. Uses SNMP v2

The file portctl_conf.json is the file that maps GPIO pins to 
Ethernet Switch IP and ports. See example portctl_conf.json.sample
for an example. Support multiple Ethernet Switches and Ports per
GPIO pin. Remember JSON does not permit comments. 

An example systemd unit file is provided. This is configured to 
restart on failure. Modify as needed

On startup the script kills any other instances running. This allows
a restart in a cron. Only works on Linux as it used a system call 
to get list of processes. 

Supports only one option -v to print out more verbose output for 
testing purposes. 

New installation requires creating a file community_str.txt and add
the community string to use for authentication with SNMP v2 
