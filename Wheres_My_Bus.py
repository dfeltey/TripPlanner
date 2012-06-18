'''import realtime_bus
from Tkinter import *       

class Application(Frame):              
    def __init__(self, master=None):
        Frame.__init__(self, master)
        v = IntVar()   
        self.grid()                    
        self.createWidgets()

    def createWidgets(self):
    	self.
        self.quitButton = Button ( self, text='Quit',
            command=self.quit )        
        self.quitButton.grid()         

app = Application()                    
app.master.title("Sample application") 
app.mainloop() 
'''
from Tkinter import *
from realtime_bus import *


def sel():
	output=""
	var = v.get()
	vehicles = get_route_vehicles(var)
	for bus in vehicles:
		data = get_vehicle_status(bus)
		output+= str(data) + '\n'
	label.config(text = output)

busses = [1,2,3,7,8,9,13,14,15,36,45,60,75,102]

master = Tk()

v = IntVar()

for bus in busses:
	b = Radiobutton(master,text=str(bus),variable=v,value=bus,command=sel)
	b.pack(anchor=W)
label=Label(master)
label.pack()

master.mainloop()
