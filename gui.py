from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
def compile():
    codefile = fd.askopenfilename()
root = Tk()
root.title("nmcfs Compiler")
root.resizable(width=False, height=False)
frame1 = Frame(root, width=300, height=500)
frame1.grid(row=0, column=0)
frame1.grid_propagate(0)
frame1.update()
l = Label(frame1,text="nmcfs Compiler")
l.place(x=frame1.winfo_width()/2+5, y=25, anchor="center")
quitbutton = ttk.Button(frame1, text="Quit", command=root.destroy)
quitbutton.place(x=frame1.winfo_width()/2,y=450)
compilebutton = ttk.Button(frame1, text="Compile", command=compile)
compilebutton.place(x=frame1.winfo_width()/2-105,y=450)
root.mainloop()
