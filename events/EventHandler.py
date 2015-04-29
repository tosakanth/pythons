class Event( object ):
    """
    Generic event to use with EventDispatcher.
    """
 
    def __init__(self, event_type, data=None):
        """
        The constructor accepts an event type as string and a custom data
        """
        self._type = event_type
        self._data = data
 
    @property
    def type(self):
        """
        Returns the event type
        """
        return self._type
 
    @property
    def data(self):
        """
        Returns the data associated to the event
        """
        return self._data
        
#=======================================================================
class EventDispatcher( object ):
    """
    Generic event dispatcher which listen and dispatch events
    """
 
    def __init__(self):
        self._events = dict()
 
    def __del__(self):
        """
        Remove all listener references at destruction time
        """
        self._events = None
 
    def has_listener(self, event_type, listener):
        """
        Return true if listener is register to event_type
        """
        # Check for event type and for the listener
        if event_type in self._events.keys():
            return listener in self._events[ event_type ]
        else:
            return False
 
    def dispatch_event(self, event):
        """
        Dispatch an instance of Event class
        """
        # Dispatch the event to all the associated listeners
        if event.type in self._events.keys():
            listeners = self._events[ event.type ]
 
            for listener in listeners:
                listener( event )
 
    def add_event_listener(self, event_type, listener):
        """
        Add an event listener for an event type
        """
        # Add listener to the event type
        if not self.has_listener( event_type, listener ):
            listeners = self._events.get( event_type, [] )
 
            listeners.append( listener )
 
            self._events[ event_type ] = listeners
 
    def remove_event_listener(self, event_type, listener):
        """
        Remove event listener.
        """
        # Remove the listener from the event type
        if self.has_listener( event_type, listener ):
            listeners = self._events[ event_type ]
 
            if len( listeners ) == 1:
                # Only this listener remains so remove the key
                del self._events[ event_type ]
 
            else:
                # Update listeners chain
                listeners.remove( listener )
 
                self._events[ event_type ] = listeners      
                
#=======================================================================  
class MyEvent(Event):
	ASK = 'to ask an event'                
	RESPONSE = 'to response the event'
	
class TheAsk(object):
	def __init__(self,event_dispatcher):
		self.event_dispatcher = event_dispatcher
		self.event_dispatcher.add_event_listener(MyEvent.RESPONSE,self.on_answer)
		
	def to_ask(self):
		print "I'm asking Who are listening to me ?"	
		
		#dispatch event by using itself as data
		self.event_dispatcher.dispatch_event(MyEvent(MyEvent.ASK,self))
		
	def on_answer(self,evt):
		print evt.data	
		
class TheResponse(object):
	def __init__(self,evt_dispatcher):
		self.event_dispatcher = evt_dispatcher
		self.event_dispatcher.add_event_listener(MyEvent.ASK,self.on_ask)		
		
	def on_ask(self,evt):
		self.event_dispatcher.dispatch_event(MyEvent(MyEvent.RESPONSE,"My name is Tosakanth"))

#=======================================================================

if __name__ == "__main__":
	edi = EventDispatcher()
	ask = TheAsk(edi)
	ans = TheResponse(edi)
	ask.to_ask()		
