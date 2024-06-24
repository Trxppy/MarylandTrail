# import local files
from classes.loader import *
from classes.interface import *

# initialize loader + interface
loader = Loader()
interface = Interface(loader)

## command controller
#def parse_command(command, loader):
#    if(command == "start"):
#        game.start();
#    if(command == "load"):
#        game.load();

## load console
#console_active = True
#while(console_active):
#    command = input()
#    if(command == "exit"):
#        console_active = False
#    else:
#        parse_command(command, loader)


