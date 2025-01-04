from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
def compile():
    codefile = fd.askopenfilename()
root = Tk()
root.title("nmcfs Compiler")
root.resizable(width=False, height=False)
frame1 = Frame(root, width=300, height=300)
frame1.grid(row=0, column=0)
label1 = Label(frame1, text="Compile nmcfs code",
                  fg="white", font=("Arial", 12, "bold"))
label1.place(relx=0.5, rely=0.1, anchor=CENTER)
ttk.Button(frame1, text="Quit", command=root.destroy).grid(column=1, row=0)
ttk.Button(frame1, text="Compile", command=compile).grid(column=2, row=0)
root.mainloop()
