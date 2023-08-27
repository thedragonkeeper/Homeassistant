
import datetime

class Gui():
    def __init__(self, client):
        import tkinter as tk
        import tkinter.font as tkFont
        self.client = client
        self.root = tk.Tk()
        self.tk = tk
        self.tkFont = tkFont
        self.device_buttons = {}
        self.infodisplaying = ""
        self.input_item_rows = []

        self.set_window()


    def set_window(self):
        #setting title
        self.root.title("undefined")
        #setting window size
        width=1280
        height=800
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.DevicesLabel=self.tk.Label(self.root)
        ft = self.tkFont.Font(family='Times',size=10)
        self.DevicesLabel["font"] = ft
        self.DevicesLabel["fg"] = "#333333"
        self.DevicesLabel["justify"] = "center"
        self.DevicesLabel["text"] = "Devices"
        self.DevicesLabel.place(x=10,y=20,width=200,height=25)

        self.InfoBox=self.tk.Message(self.root)
        ft = self.tkFont.Font(family='Times',size=10)
        self.InfoBox["font"] = ft
        self.InfoBox["fg"] = "#333333"
        self.InfoBox["justify"] = "center"
        self.InfoBox["text"] = ""
        self.InfoBox.place(x=155,y=45,width=605,height=350)

        self.update_self()
        self.root.mainloop()

    def update_self(self):
        # get current time as text
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.DevicesLabel["text"] = "Devices  :  "+str(current_time)
        self.get_device_list()
        self.root.after(5000, self.update_self)

    def create_device_button(self, name, id):
        Button=self.tk.Button(self.root)
        Button["bg"] = "#e9e9ed"
        ft = self.tkFont.Font(family='Times',size=10)
        Button["font"] = ft
        Button["fg"] = "#000000"
        Button["justify"] = "center"
        Button["text"] = name
        Button["command"] = lambda: self.Button_command(str(id),0)
        return Button

    def create_device_trigger(self, name, id, boxes, func, x,y,w,h):
        Button=self.tk.Button(self.root)
        Button["bg"] = "#e9e9ed"
        ft = self.tkFont.Font(family='Times',size=10)
        Button["font"] = ft
        Button["fg"] = "#000000"
        Button["justify"] = "center"
        Button["text"] = name
        Button["command"] = lambda: self.triggerstates( str(id), func, boxes=boxes)
        Button.place(x=x,y=y,width=w,height=h)
        return Button

    def get_device_list(self):
        my_buttons = {}
        for device in self.client.devices.keys():
            data = self.client.devices[device]["data"]
            if "DeviceInfo" in data:
                my_buttons[str(device)] = self.create_device_button(data["DeviceInfo"]["name"], str(device))
            else:
                my_buttons[str(device)] = self.create_device_button("Unknown: "+str(device), str(device))
        for button in self.device_buttons:
            if str(button) == str(self.infodisplaying):
                self.InfoBox["text"] = "Device Disconnected"
            self.device_buttons[button].destroy()
        self.device_buttons = my_buttons
        x,y,w,h = 10,60,150,25
        for button in self.device_buttons.keys():
            self.device_buttons[button].place(x=x,y=y,width=w,height=h)
            y = y + h + 1
            if str(button) == str(self.infodisplaying):
                self.Button_command(str(button), 1)


    def make_label(self, text, x,y,w,h):
        Label=self.tk.Label(self.root)
        ft = self.tkFont.Font(family='Times',size=10)
        Label["font"] = ft
        Label["fg"] = "#333333"
        Label["justify"] = "center"
        Label["text"] = text
        Label.place(x=x,y=y,width=w,height=h)
        return Label

    def triggerstates(self, id, func, boxes=None):
        print(id)
        print(func)
        if boxes != None:
            print("boxes: "+str(len(boxes)))
            mydict = {}
            for x in boxes:
                mydict[x[0]] = x[1].get()
            self.client.commands.triggerstatechange(id, func, mydict)
        else:
            self.client.commands.triggerfunc([func, id])

    def create_device_trigger_func(self, id, name, x,y,w,h):
        Button=self.tk.Button(self.root)
        Button["bg"] = "#e9e9ed"
        ft = self.tkFont.Font(family='Times',size=10)
        Button["font"] = ft
        Button["fg"] = "#000000"
        Button["justify"] = "center"
        Button["text"] = name
        Button["command"] = lambda: self.triggerstates(str(id), name, boxes=None)
        Button.place(x=x,y=y,width=w,height=h)
        return Button


    def Button_command(self, device, auto):
        if device in self.client.devices:
            text = ""
            client = self.client.devices[device]
            if "id" in client:
                text = text + "id: " + str(client["id"]) + "\n"
            if "addr" in client:
                text = text + "ip: " + str(client["addr"][0]) + "\n"
            if "data" in client:
                client = client["data"]
                text = text + "__ DEVICE INFO __" + "\n"
                if "DeviceInfo" in client:
                    for each in client["DeviceInfo"]:
                        text = text + str(each) + ": " + str(client["DeviceInfo"][each]) + "\n"
                text = text + "__ CURRENT STATES __" + "\n"
                if "States" in client:
                    for each in client["States"]:
                        #if str(type(client["States"][each])) == "<class 'dict'>":
                        text = text + str(each) + ": " + str(client["States"][each]) + "\n"
            self.InfoBox["text"] = text
            self.infodisplaying = device
            if auto == 0:
                self.input_items(device)

    def input_items(self, device):
        for rows in self.input_item_rows:
            for cols in rows:
                cols[0].destroy()
                for boxes in cols[1]:
                    boxes[1].destroy()
        self.input_item_rows = []
        x,y,w,h=155,400,150,25
        if device in self.client.devices:
            client = self.client.devices[device]
            if "data" in client:
                client = client["data"]
                if "Functions" in client:
                    rows = []
                    for each in client["Functions"]:
                        cols = []
                        nx = x
                        if client["Functions"][each] == [0]:
                            cols.append([self.create_device_trigger_func(str(device), str(each), nx,y,150,h),[]])
                            nx = nx+150
                        else:
                            print(client["Functions"][each])
                            cols.append([self.make_label(str(each), nx,y,200,h),[]])
                            nx = nx+200
                            #client["Functions"][each].pop(0)
                            inputboxs = []
                            for entry in client["Functions"][each]:
                                #entry = entry.split(":")
                                cols.append([self.make_label(str(entry[1]), nx,y,w,h),[]])
                                nx = nx+w
                                if entry[0] != "Bool":
                                    box = self.tk.Entry(self.root)
                                    box.place(x=nx,y=y,width=150,height=h)
                                    inputboxs.append([str(entry[1]), box])
                                    nx = nx+150
                            if len(inputboxs) > 0:
                                cols.append([self.create_device_trigger("Submit", str(device), inputboxs , each ,nx,y,50,h),inputboxs])
                        if len(cols) > 0:
                            y = y + h
                            rows.append(cols)
                    self.input_item_rows = rows

if __name__ == "__main__":
    from Client import Client
    client = Client("127.0.0.1", 5051, "my.crt")
    client.ConnectToServer()
    Gui(client)
