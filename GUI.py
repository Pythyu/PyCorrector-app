from Configurator import *
from tkinter import *
import random
color = ['blue','red','yellow','green','white','black']


class SubFrame:
    def __init__(self, parent, subframes=None, title="", color=None,frameSide=RIGHT):
        if color is None:
            self.color = random.choice(color)
        else:
            self.color = color
        if subframes is None:
            subframes = []
        self.current = Frame(parent,bg = self.color, borderwidth = 1,relief=RIDGE)
        self.current.pack(side=frameSide)
        self.title = title
        if title != "":
            self.label = Label(self.current, text=title)
            self.label.pack(side=TOP)
        self.button = Button(self.current, text="+", command=self.reproduce)
        self.button.pack(side=LEFT,anchor="n")
        self.clo = Button(self.current, text="-", command=self.die)
        self.clo.pack(side=RIGHT,anchor="n")

        self.subframes = subframes

    def reproduce(self):
        self.subframes.append(SubFrame(self.current,title=self.title))

    def die(self):
        self.current.destroy()

class FrameFunc(SubFrame):
    def __init__(self, parent, subframes=None, title="",frameSide=RIGHT):
        super().__init__(parent, subframes, "Test Function", "red", frameSide)
        self.entry = Entry(self.current)
        self.entry.pack(side=LEFT)
        
    def reproduce(self):
        self.subframes.append(DataFrame(self.current,title=self.title))

class DataFrame(SubFrame):
    def __init__(self, parent, subframes=None, title=""):
        super().__init__(parent, subframes, "Test set", "blue")


    def reproduce(self):
        if self.subframes:
            return
        self.subframes.append(ArgFrame(self.current,title=self.title))

class ArgFrame(SubFrame):
    def __init__(self, parent, subframes=None, title=""):
        super().__init__(parent, subframes, "Data List", "green")


    def reproduce(self):
        self.subframes.append(DataFra(self.current,title=self.title))

class DataFra(SubFrame):
    def __init__(self, parent, subframes=None, title=""):
        super().__init__(parent, subframes, "Data", "yellow")
        self.button.pack_forget()
        self.entry = Entry(self.current)
        self.entry.pack(side=RIGHT)

    def reproduce(self):
        pass






class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("800x600")


        self.frames = []
        self.button = Button(self.tk, text="+", command=self.reproduce)
        self.button.pack(side=TOP)
        self.butconf = Button(self.tk, text="generate config file", command=self.configfill)
        self.butconf.pack(side=BOTTOM)



        self.tk.mainloop()

    def reproduce(self):
        self.frames.append(FrameFunc(self.tk,title="Exemple Title",frameSide=TOP))

    def configfill(self):
        for func in self.frames:
            name = func.entry.get()
            set_list = []
            for dataset in func.subframes:
                arg_list = []
                for args in dataset.subframes:
                    data_list = []
                    for data in reversed(args.subframes):
                        payload = data.entry.get()
                        data_list.append(Data(payload))
                    arg_list.append(Arguments(data_list))
                set_list.append(arg_list[0])
            Config.FUNCTIONS.append(UserFunc(name, DataSet(set_list)))
            print(Config.FUNCTIONS[-1])





if __name__ == "__main__":
    app = App()
