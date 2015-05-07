import paho.mqtt.client as mqtt
import time
import base64

import pygame 
import pygame.camera
import pygame.image
import zlib

class Capture(object):
	def __init__(self):
		pygame.init()
		pygame.camera.init()
		self.size = (320,240)
		self.image_format='RGB'
		self.clist = pygame.camera.list_cameras()
		if not self.clist:
			self.camera = None
			raise ValueError("Sorry, no cameras detected.")
		else :    
			self.camera = pygame.camera.Camera(self.clist[0], self.size)

	def take_snap(self):		
		snapshot = None
		if self.camera is not None :
			self.camera.start()
			#if self.camera.query_image():
			snapshot = self.camera.get_image()
			self.camera.stop()
		return snapshot	

	def encode_base64(self,src_img):
		encoded = None
		try:
			img_str = pygame.image.tostring(src_img,self.image_format)
			imgcompressed = zlib.compress(img_str, 9)
			encoded = base64.encodestring(imgcompressed)
		except:
			pass	
		return encoded
		

	def quit(self):
		pygame.quit()
    



BROKER_PORT = 1883
BROKER_HOST = "test.mosquitto.org" # Test host from mosquitto.org
KEEPALIVE = 60 #maximum period in seconds allowed between communication
TOPIC='tk/demo'

def on_connect(client,userdata,results):
    print "Connected with result "+str(results)
   
    
    
def on_publish(client,userdata,mid):
    print "Message has been published with id = "+str(mid)

    
capture  = Capture()            
client = mqtt.Client()
    
# Be generated when client receives CONNACK message from broker.
client.on_connect =  on_connect

# Be generated after client has published message to broker.
client.on_publish = on_publish


client.connect(BROKER_HOST,BROKER_PORT,KEEPALIVE)
client.subscribe(TOPIC,0)
client.loop_start()
stop_flag=False

while True:
	try:	
		pic=capture.take_snap()	
		if pic is not None :
			b64 = capture.encode_base64(pic)
			if b64 is not None :
				client.publish(TOPIC,b64)
		time.sleep(5)
	except KeyboardInterrupt:
		break

capture.quit()   
client.disconnect()		
