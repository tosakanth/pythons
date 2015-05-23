import argparse
import serial
import logging
import sys
import time

parser = argparse.ArgumentParser(description='To test ESP8266 communication')
parser.add_argument('-p',action='store', dest='comm_port', help='port',default='/dev/ttyAMA0')
parser.add_argument('-b',action='store',dest='baud_rate',help='baudrate',default=9600,type=int)

#inititiat logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



#--- function ---
def enum(**enums):
    return type('Enum', (), enums)
    
def send_cmd(cmd,timeout=1,retry=5):
	global esp_ser
	tick = 0
	reply=''
	
	logging.info("sending command %s to ESP" % cmd)
	for t in range(retry):
		#discard all content
		esp_ser.flushInput()
		
		#send command to ESP
		esp_ser.write(cmd+'\r\n')
		
		#wait for reply from ESP
		reply=esp_ser.readline()
		time.sleep(0.2)
		
		while (tick < timeout or 'busy' in reply):
			while(esp_ser.inWaiting()):
				#get all characters in esp_ser's buffer
				reply= esp_ser.readline().strip( "\r\n" )
                                #reply = esp_ser.readline()
				logging.debug(reply)
				tick = 0
			if reply in status.OK :
				break
			if reply in status.ERROR :
				break
                        if reply in status.PROMPT :
                                break
			time.sleep(1)	
			tick = tick+1
		time.sleep(1)
		if reply in status.OK :
			break
	print "RESULT : %s" % reply					
		
#some useful status
status = enum(PROMPT='>',ERROR='ERROR', OK=['OK', 'ready', 'no change'], BUSY='busy')

#get argument values from user
arguments = parser.parse_args()

#initiate serial comm.
esp_ser = serial.Serial(arguments.comm_port,arguments.baud_rate)

#clean up and reopen port
if esp_ser.isOpen() :
	esp_ser.close()
esp_ser.open()
esp_ser.isOpen()	

try:
	print "Ctrl-C to stop"
	prompt ="?"
	while True :
		user_input =raw_input(prompt) 
		send_cmd(user_input)
except KeyboardInterrupt :
	esp_ser.close()		
