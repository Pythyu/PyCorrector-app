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

    state_string = {0 : "Setup each functions and associated inputs >",
                    1 : "Set the expected inputs of each functions >",
                    2 : "Select a score function >",
                    3 : "Select Timeout Time >"}

    yaml_state = {0: "functions:",
                  1: "expected_outputs:",
                  2: "score_functions:",
                  3: "timeout_functions:"}

    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("800x600")

        self.state = 0
        self.total_string = "static:\n"+"    myvar: [\"text1\"]\n"

        self.frames = []
        self.mainLabel = Label(self.tk, text = "FUNCTIONS INPUTS >")
        self.mainLabel.pack(side=TOP)
        self.button = Button(self.tk, text="+", command=self.reproduce)
        self.button.pack(side=TOP)
        self.buttonNext = Button(self.tk, text="Next Step >", command=self.nextStep)
        self.buttonNext.pack(side=LEFT)
        self.butconf = Button(self.tk, text="config file generation will be available once the filling process will be over", command=None)
        self.butconf.pack(side=BOTTOM)



        self.tk.mainloop()

    def nextStep(self):
        if self.state < 3:
            if self.state == 2:
                self.butconf["command"] = self.configfill
                self.butconf["text"] = "Generate Config File !"
            else:
                self.configfill()
            self.state += 1
            self.mainLabel["text"] = self.state_string[self.state]

    def reproduce(self):
        self.frames.append(FrameFunc(self.tk,title="Exemple Title",frameSide=TOP))

    def configfill(self):

        if self.state == 3:
            outfile = open("config.yaml", "w")

        self.total_string += self.yaml_state[self.state] +"\n"
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
            self.total_string += "    " + str(Config.FUNCTIONS[-1]) + "\n"

        if self.state == 3:
            outfile.write(self.total_string)
            outfile.close()
            self.state = 0
            self.total_string = ""
            self.mainLabel["text"] = self.state_string[self.state]






if __name__ == "__main__":
    app = App()
