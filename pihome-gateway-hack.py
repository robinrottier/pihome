#!/usr/bin/python3

import re
import socket
import sys
import telnetlib, time, datetime
#from typing import Any

import paho.mqtt.client as paho

# Debug print to screen configuration
dbgLevel = 1 	# 0-off, 1-info, 2-detailed, 3-all

# Get the local ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
ip = s.getsockname()[0]
base_ip = re.search('^[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.', ip)

gatewaytype = "wifi"                            # serial/wifi
gatewaylocation = "192.168.86.31"                     # ip address or serial port of your MySensors gateway
gatewayport = 5003                        # UDP port or bound rate for MySensors gateway
gatewaytimeout = 60                    # Connection timeout in Seconds

if dbgLevel >= 1:
	print("Local ip:      ", ip)
	print("Gateway Type:  ", "Wifi/Ethernet")
	print("IP Address:    ", gatewaylocation)
	print("UDP Port:      ", gatewayport)


msgs = [ 
	"100;1;1;1;2;0",
	"101;1;1;1;2;0",
	"101;2;1;1;2;0",
	"101;3;1;1;2;0"
]

nodeidMap = {
	"0": "controller",
	"20": "downstairs",
	"21": "upstairs",
	"30": "hotwater",
	}

# map type,subtype to payload meaning
controllermsgmap = {
	"0314": "init",
	"0018": "version",
}

sensormsgmap = {
	"0017": "verion",
	"0018": "version",
	"0124": "min_value",
	"0311": "sensor_type",
	"0312": "sketch_version",
	"0300": "battery_level",
	"0306": "unknown",
}

sensorchildmsgmap = {
	"0003": "max_child_id",
	"0006": "max_child_id",
	"0100": "temperature",
	"0138": "battery_v",
	}

def readFromGatewayLoop():
	while True:
		try:
			if dbgLevel >= 1:
				print("")
				print("Openning gateway...")
			gw = telnetlib.Telnet(gatewaylocation, gatewayport, timeout=gatewaytimeout) # Connect mysensors gateway from MySQL Database
			readFromGateway(gw)
			if dbgLevel >= 1:
				print("Gateway unexpectedly ended")
		except Exception as e:
			if dbgLevel >= 1:
				print("Gateway aborted:",e)
		finally:
			try:
				gw.close()
			except:
				# if that close fails just ignore it
				if (dbgLevel >= 2):
					print("Gateway close aborted (thats not too bad")
		time.sleep(10)

def readFromGateway(gw):

	mc = 0
	lastwasdot = False

	while 1:
		if len(msgs) > 0:
			wm = msgs.pop(0)
			if dbgLevel >= 2:
				print("Write: ",wm)
			gw.write(wm.encode("utf-8"))

		mc = mc+1

		in_str = gw.read_until(b'\n', timeout=1) # Here is receiving part of the code for Wifi

		in_str = in_str.decode('utf-8')
		in_str = in_str.replace("\n", "")
		in_str = in_str.replace("\r", "")
		if (in_str == ""):
			if dbgLevel >= 2:
				print(".", end="")
			lastwasdot = True
		else:
			if dbgLevel >= 2:
				if lastwasdot:
					print("")
				print("Received:"+str(mc)+": '"+in_str+"'")
			lastwasdot = False

			if len(in_str) > 50:
				print("Line length exceeds 50 - ignoring")
				continue

			statement = in_str.split(";")
			if len(statement) != 6:
				print("Line parsing did not find 6 parts - ignoring")
				continue
			
			if not statement[0].isdigit(): #check if received message is right format
				print("Line parsing did not find part 0 numeric - ignoring")
				continue

			node_id = str(statement[0])
			child_sensor_id = int(statement[1])
			message_type = int(statement[2])
			ack = int(statement[3])
			sub_type = int(statement[4])
			payload = statement[5].rstrip() # remove \n from payload

			if dbgLevel >= 3: # Debug print to screen
				print("Node ID:                     ",node_id)
				print("Child Sensor ID:             ",child_sensor_id)
				print("Message Type:                ",message_type)
				print("Acknowledge:                 ",ack)
				print("Sub Type:                    ",sub_type)
				print("Pay Load:                    ",payload)
			elif dbgLevel >= 2:
				print("Node:",node_id.rjust(2),str(child_sensor_id).rjust(3),"Type:",message_type,"Ack:",ack,"Sub_type:",str(sub_type).rjust(2),"Payload:",payload)

			node = nodeidMap.get(node_id)
			if node == None:
				print("Node:",node_id.rjust(2),str(child_sensor_id).rjust(3),"Type:",message_type,"Ack:",ack,"Sub_type:",str(sub_type).rjust(2),"Payload:",payload," !! Unknwon node id")
			else:
				k = str(message_type).rjust(2,"0")+str(sub_type).rjust(2,"0")
				if node == "controller":
					m = controllermsgmap.get(k)
				else:
					if child_sensor_id == 255:
						m = sensormsgmap.get(k)
					else:
						m = sensorchildmsgmap.get(k)

				if m == None:
					print(node,child_sensor_id,"Type:",message_type,"Ack:",ack,"Sub_type:",str(sub_type).rjust(2),"Payload:",payload," !! Unknwon msg type")
				else:
					print(node.ljust(10),str(child_sensor_id).ljust(3),m.ljust(12),payload)


readFromGatewayLoop()
