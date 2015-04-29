from copy import deepcopy, copy

class Event():
    
    INIT        = "init"
    CHANGE      = "change"
    OPEN        = "open"
    CLOSE       = "close"
    ACTIVATE    = "activate"
    COMPLETE    = "complete"
    DEACTIVATE  = "de_activate"
    
    def __init__( self, type ):
        self.type = type
        self.target = None
        self.data = None
        
class EventDispatcher():
    def __init__(self):
        self.map = {}
    
    '''
        - Adds an event handler by binding it to an event type
    '''
    def push_handler( self, type, handler ):
        if type not in self.map:
            self.map[type] = [ handler ]
        else:    
            self.map[type].append( handler )
        
    '''
        - Remove an event handler
    '''
    def pop_handler( self, type, handler ):
        if type in self.map:
            handlers = self.map[type]
            for h in handlers:
                if handler == h:
                    handlers.remove(h)
    
    '''
        - Invoke each handler bound to the dispatched event
        - uses deepcopy to handle use case wherein new hanlders are added to
        - within other handlers, causing lengths of dictionaries to change and errors to be thrown
    '''
    def dispatch_event( self, event ):
        type = event.type
        event.target = self
        # -- creating copy to prevent length of handlers from changing if handlers are added within other handlers
        clone = deepcopy( self.map )
        for type in clone:
            handlers = self.map[type]
            for handler in handlers:
                handler( event )
                

def on_test(evt):
	print "Hello World"
                
Evt =  EventDispatcher()
Evt.push_handler(Event.INIT,on_test)               
