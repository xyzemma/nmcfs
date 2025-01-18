# Import Modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import sv_ttk
import webbrowser
from tktooltip import ToolTip
import parser

#ORIGINAL_DPI = 240.23645320197045   # This is the DPI of the computer you're making/testing the script on.

#def get_dpi():
#    screen = Tk()
#    current_dpi = screen.winfo_fpixels('1i')
#    screen.destroy()
#    return current_dpi

#SCALE = get_dpi()/ORIGINAL_DPI    # Now this is the appropriate scale factor you were mentioning.

# Now every time you use a dimension in pixels, replace it with scaled(*pixel dimension*)
#def scaled(original_width):
#    return round(original_width * SCALE)

#if __name__ == '__main__':
#    root = Tk()
#    root.geometry(f'{scaled(500)}x{scaled(500)}')    # This window now has the same size across all monitors. Notice that the scaled factor is one if the script is being run on a the same computer with ORIGINAL_DPI. 
#    root.mainloop()

# Functions
def selectfile(): # Function called by "Select" Button
    global codefile
    codefile = fd.askopenfilename()
    pathinput.delete(0,END)
    pathinput.insert(0,codefile)

def selectdir(): # Function called by second "Select" Button
    global outdir
    outdir = fd.askdirectory()
    outdirinput.delete(0,END)
    outdirinput.insert(0,outdir)

def compile(): # Function called by "Compile" Button
    print("test")

def urlopen(url): # Function used for License Link
    webbrowser.open_new_tab(url)

# Window Setup
root = Tk()
root.title("nmcfs Compiler")
root.resizable(width=False, height=False)
sv_ttk.set_theme("light")
frame1 = ttk.Frame(root, width=300, height=500)
im = Image.open('nmcfs_templogo.png')
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)
frame1.grid(row=0, column=0)
frame1.grid_propagate(0)
frame1.update()

# Logo
logoimg = Image.open("nmcfs_templogo.png")
logoimg = logoimg.resize((100,100))
logoimg = ImageTk.PhotoImage(logoimg)
logo = ttk.Label(frame1, image=logoimg)
logo.place(x=frame1.winfo_width()/2-50,y=5)

# Main UI Elements
l = ttk.Label(frame1,text="nmcfs Compiler",font=("Helvetica",15,"bold"))
l.place(x=frame1.winfo_width()/2, y=120, anchor="center")
quitbutton = ttk.Button(frame1, text="Quit", command=root.destroy, width=15)
quitbutton.place(x=160,y=420)
compilebutton = ttk.Button(frame1, text="Compile", command=compile, width=15)
compilebutton.place(x=10,y=420)

# Input Path
pathlabel1 = ttk.Label(frame1,text="File to compile:",font=("Helvetica",7,"bold"))
pathlabel1.place(x=10,y=200)
pathinput = ttk.Entry(frame1, width=19)
pathinput.place(x=10,y=220,height=30)
pathbutton = ttk.Button(frame1,text="Select",command=selectfile)
pathbutton.place(x=230,y=220)

# Output Path
outdirinput = ttk.Entry(frame1, width=19)
outdirinput.place(x=10,y=300,height=30)
pathlabel2 = ttk.Label(frame1,text="Output Path:",font=("Helvetica",7,"bold"))
pathlabel2.place(x=10,y=280)
pathbutton2 = ttk.Button(frame1,text="Select",command=selectdir)
pathbutton2.place(x=230,y=300)

# License
licensetext = ttk.Label(frame1, text="nmcfs © MIT License - 2025 Rosafy",foreground="blue", cursor="hand2", font=("Helvetica",6),wraplength=200, justify="center")
licensetext.place(x=50, y=470)
licensetext.bind("<Button-1>", lambda e: urlopen("https://github.com/rosafy/nmcfs/blob/main/LICENSE"))
ToolTip(licensetext, msg="Read License")

# Run
root.mainloop()
