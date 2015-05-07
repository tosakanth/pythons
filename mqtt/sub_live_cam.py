import paho.mqtt.client as mqtt
import time
import base64

import pygame 
import pygame.image
import zlib

class ImageHandler(object):
	def __init__(self):
		pygame.init()
		self.size = (320,240)
		self.image_format='RGB'
		self.display = pygame.display.set_mode(self.size, 0)        
		
	def decode_base64(self,b64str): 
		img =  None
		try :
			img = pygame.image.fromstring(zlib.decompress(base64.decodestring(b64str)),self.size , self.image_format)   
		except :
			pass
				
		return  img

	def show_image(self,img):
		self.display.blit(img, (0,0))
		pygame.display.flip()
						
	def quit(self):
		pygame.quit()
    



BROKER_PORT = 1883
BROKER_HOST = "test.mosquitto.org" # Test host from mosquitto.org
KEEPALIVE = 60 #maximum period in seconds allowed between communication
TOPIC='tk/demo'

def on_connect(client,userdata,results):
    print "Connected with result "+str(results)
   

def on_message(client,userdata,msg):
	global stop_flag
	global capture
	img = capture.decode_base64(msg.payload)
	if img is not None :
		capture.show_image(img)
	
	
	
		
    
imgHandler  = ImageHandler()            
client = mqtt.Client()
    
# Be generated when client receives CONNACK message from broker.
client.on_connect =  on_connect

# Be generated after message from broker arrived.
client.on_message = on_message


client.connect(BROKER_HOST,BROKER_PORT,KEEPALIVE)
client.subscribe(TOPIC,0)
client.loop_start()

#There are a lot of better ideas but this is my controllable loop
while True :
	try:
		pass
	except KeyboardInterrupt:
		break
		
imgHandler.quit()   
client.unsubscribe(TOPIC)
client.disconnect()		








