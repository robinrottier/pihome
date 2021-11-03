#!/usr/bin/python3

import telnetlib, time, datetime
from typing import Any

class bc:
	hed = '\033[95m'
	dtm = '\033[0;36;40m'
	ENDC = '\033[0m'
	SUB = '\033[3;30;45m'
	WARN = '\033[0;31;40m'
	grn = '\033[0;32;40m'
	wht = '\033[0;37;40m'
	ylw = '\033[93m'
	fail = '\033[91m'
    
gatewaytype = "wifi"                            # serial/wifi
gatewaylocation = "192.168.86.31"                     # ip address or serial port of your MySensors gateway
gatewayport = 5003                        # UDP port or bound rate for MySensors gateway
gatewaytimeout = 60                    # Connection timeout in Seconds

gw = telnetlib.Telnet(gatewaylocation, gatewayport, timeout=gatewaytimeout) # Connect mysensors gateway from MySQL Database
print(bc.grn + "Gateway Type:  Wifi/Ethernet", bc.ENDC)
print(bc.grn + "IP Address:    ",gatewaylocation, bc.ENDC)
print(bc.grn + "UDP Port:      ",gatewayport, bc.ENDC)

msgs = [ \
	"100;1;1;1;2;0",\
	"101;1;1;1;2;0",\
	"101;2;1;1;2;0",\
	"101;3;1;1;2;0"\
]

mc = 0
lastwasdot = False

while 1:
	if len(msgs) > 0:
		wm = msgs.pop(0)
		print("Write: ",wm)
		gw.write(wm.encode("utf-8"))

	mc = mc+1
	in_str = gw.read_until(b'\n', timeout=1) # Here is receiving part of the code for Wifi
	in_str = in_str.decode('utf-8')
	in_str = in_str.replace("\n", "\\n")
	in_str = in_str.replace("\r", "\\r")
	if (in_str == ""):
		print(".", end="")
		lastwasdot = True
	else:
		if lastwasdot:
			print("")
		print("Received:"+str(mc)+": '"+in_str+"'")
		lastwasdot = False
