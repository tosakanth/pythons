class Event:
 
    def __init__(self, name , data=None):
        self._name = name
        self._data = data
 
    def get_name(self):
        return self._name
 
    def get_data(self):
        return self._data
        
#=======================================================================
class Dispatcher:
 
    def __init__(self):
        self._events = dict()
 
    def remove_all(self):
        self._events = None
 
    def get_listener(self, event_name, listener):
        # return True when it already has event name or False when it does not
        if event_name in self._events.keys():
            # if listener is registered return True or False if it is not. 
            return listener in self._events[event_name]
        else:
            # return False in other cases.
            return False
 
    def dispatch_event(self, event):
        evt_name = event.get_name()
        if evt_name in self._events.keys():
            # get all listeners registered in.
            listeners = self._events[evt_name]
 
            for listener in listeners:               
                listener(event)
 
    def add_event_listener(self, event_name, listener):
        already_has_listener = self.get_listener(event_name, listener)
        if not already_has_listener:
            # find an array associating with the event_name or create a blank array if it does not exist
            listeners = self._events.get(event_name, [] )
 
            #append a new listener to the array 
            listeners.append( listener )
 
            self._events[event_name] = listeners
 
    def remove_event_listener(self, event_name, listener):
        already_has_listener = self.get_listener(event_name, listener)
        if already_has_listener:
            # get all listeners for the given event name in term of array
            listeners = self._events[ event_name ]
 
            if len( listeners ) == 1:
                # if there is only one listener remains, just remove the key
                del self._events[ event_name ]
 
            else:
                # if there are more than one listeners, remove the specified listener
                listeners.remove( listener )
                
                #update the dictionary    
                self._events[event_name] = listeners   
                
#=======================================================================  
class MyEvent(Event):
	ASK = 'to ask an event'                
	RESPONSE = 'to response the event'
	
class TheAsk(object):
	def __init__(self,event_dispatcher):
		self.event_dispatcher = event_dispatcher
		self.event_dispatcher.add_event_listener("xxx",self.on_answer)
		
	def to_ask(self):
		print "I'm asking Who are listening to me ?"	
		
		#dispatch event by using itself as data
		myevt = Event("yyy","I am a man.")
		self.event_dispatcher.dispatch_event(myevt)
		
	def on_answer(self,evt):
		print evt.get_data()
		
class TheResponse(object):
	def __init__(self,evt_dispatcher):
		self.event_dispatcher = evt_dispatcher
		self.event_dispatcher.add_event_listener("yyy",self.on_ask)		
		
	def on_ask(self,evt):
		myevt=Event("xxx","My name TOSAKANTH")
		self.event_dispatcher.dispatch_event(myevt)

#=======================================================================
class Listener1:
   def __init__(self,dispatcher):
      self.dispatcher = dispatcher
      #listen to the event named "when sup up" and when it ups call on_sun_up
      self.dispatcher.add_event_listener("when sun up",self.on_sun_up)


   def on_sun_up(self,evt):
      print "When the sun ups, I am going to sing "+evt.get_data()


   def start_to_ask(self):
      my_evt = Event("when sun down","'One more night'")
      self.dispatcher.dispatch_event(my_evt)


class Listener2:
   def __init__(self,dispatcher):
      self.dispatcher=dispatcher
      #listen to the event named "when sup down" and when it ups call on_sun_down
      self.dispatcher.add_event_listener("when sun down",self.on_sun_down)
      my_evt = Event("when sun up","'Morning has broken'")
      self.dispatcher.dispatch_event(my_evt)

   def on_sun_down(self,evt):
      print "When the sun downs, I am going to sing "+evt.get_data()

#=======================================================================
if __name__ == "__main__":
   disp = Dispatcher()
   lis1 = Listener1(disp)
   lis2 = Listener2(disp)
   lis1.start_to_ask()
'''
if __name__ == "__main__":
	edi = Dispatcher()
	ask = TheAsk(edi)
	ans = TheResponse(edi)
	ask.to_ask()		
'''
