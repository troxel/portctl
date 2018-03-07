# portctl.py Port Control. 

Shutdown Ethernet ports on a switch in response to a detected 
switch closure on GPIO pins on a Raspberry pi. 

The file portctl_conf.json is the file that maps GPIO pins to 
Ethernet Switch IP and ports. See example portctl_conf.json.sample
for an example. Support multiple Ethernet Switches and Ports per
GPIO pin. Remember JSON does not permit comments. 

And example systemd unit file is provided. This is configured to 
restart on failure. Modify as needed

On startup the script kills any other instances running. This allows
a restart in a cron. Only works on Linux as it used a system call 
to get list of processes. 

Supports only one optioin -v to print out more verbose output for 
testing purposes. 
