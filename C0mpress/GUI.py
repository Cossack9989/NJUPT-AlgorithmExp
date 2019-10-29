from tkinter import ttk,filedialog,StringVar
from tkinter import *
import tkinter.messagebox
import logging,os

from C0mpress import C0mpress
from D3c0mpress import D3c0mpress

class App:
    def __init__(self, master):
        self.master = master
        self.filename = None
        self.st = None
        self.key = None
        self.et = None
        self.sb = None
        self.pb = None
        self.ub = None
        self.ratio = 0.0
        self.initWidgets()
    def initWidgets(self):
        self.st = StringVar()
        self.key = StringVar()
        self.master.geometry('320x100')
        f = Frame(self.master)
        f.pack()
        ttk.Label(self.master, textvariable=self.st,width=24,font=('StSong', 15, 'normal'),foreground='black').pack(fill=BOTH, expand=YES)
        self.et = ttk.Entry(f,textvariable=self.key,width=15,foreground='blue')
        self.et.pack(side=LEFT)
        self.sb = ttk.Button(f,text="选择文件",width=8,command=self.selectFile)
        self.sb.pack(side=LEFT)
        self.pb = ttk.Button(f,text="压缩",width=8,state = tkinter.DISABLED,command=self.press)
        self.pb.pack(side=LEFT)
        self.ub = ttk.Button(f,text="解压",width=8,state = tkinter.DISABLED,command=self.unpress)
        self.ub.pack(side=LEFT)

    def press(self):
        self.pb["state"] = tkinter.DISABLED
        x = C0mpress(self.filename,self.key.get().encode("latin-1"))
        self.et["state"] = tkinter.DISABLED
        x.do()
        self.ratio=os.path.getsize(x.targetFile.name)/os.path.getsize(self.filename)
        if self.key.get()!= "":
            self.st.set("press ratio %f \r\nwith rc4 encryption"%self.ratio)
        else:
            self.st.set("press ratio %f \r\nno encryption"%self.ratio)
        self.et["state"] = tkinter.ACTIVE
        return
    def unpress(self):
        self.ub["state"] = tkinter.DISABLED
        x = D3c0mpress(self.filename,self.key.get().encode("latin-1"))
        judgeFlag = x.undo()
        if judgeFlag == 2:
            self.st.set("unpress without encryption\r\n succeed")
        elif judgeFlag == 1:
            self.st.set("data corruption found\r\nwarning")
        elif judgeFlag == 0:
            self.st.set("unpress with encryption\r\nsucceed")
        else:
            self.st.set("unknown error")
        return
    def selectFile(self):
        try:
            fname = filedialog.askopenfilename()
            assert fname!= ''
            fp = open(fname,"rb")
            self.filename = fname
            buf = fp.read(4)
            if buf.startswith(b"C0sk") and fp.name.endswith(".c0p"):
                self.st.set("pressed file found")
                self.ub["state"] = tkinter.ACTIVE
            else:
                self.st.set("raw data")
                self.pb["state"] = tkinter.ACTIVE
        except Exception as e:
            logging.error("ERROR DURING SELECTION\r\n%s"%str(e))
            tkinter.messagebox.showerror("ERROR DURING SELECTING FILE",message="DETAILED ERROR MESSAGE\r\n%s"%str(e))

root = Tk()
root.title("C0mpress from C0sk")
App(root)
root.mainloop()