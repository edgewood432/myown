import os                                                                       
import pyinotify                                                                

WATCH_FOLDER = os.path.expanduser('/tmp')                                          

class EventHandler(pyinotify.ProcessEvent):                                     
    def process_IN_CLOSE_WRITE(self, event):                                    
        """"                                                                    
        Writtable file was closed.                                              
        """                                                                     
        print("Event: ", event.pathname, event.name)
        if event.pathname.endswith('.jpg'):                                     
            print(event.pathname)

    def process_IN_MOVED_TO(self, event):                                       
        """                                                                     
        File/dir was moved to Y in a watched dir (see IN_MOVE_FROM).            
        """                                                                     
        if event.pathname.endswith('.jpg'):                                     
            print(event.pathname)

    def process_IN_CREATE(self, event):                                         
        """                                                                     
        File/dir was created in watched directory.                              
        """                                                                     
        if event.pathname.endswith('.jpg'):                                     
            print(event.pathname)


def main():                                                                     
    # watch manager                                                             
    mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE
    watcher = pyinotify.WatchManager()                                          
    watcher.add_watch(WATCH_FOLDER,                                             
                      mask,                                                     
                      rec=True)                                                 
    handler = EventHandler()                                                    
    # notifier                                                                  
    notifier = pyinotify.Notifier(watcher, handler)                             
    notifier.loop()                                                             

if __name__ == '__main__':                                                      
    main()  
