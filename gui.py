from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import sv_ttk
import webbrowser
from tktooltip import ToolTip
import parser

# Functions
def selectfile():
    global codefile
    codefile = fd.askopenfilename()
    pathinput.delete(0, END)
    pathinput.insert(0, codefile)

def selectdir():
    global outdir
    outdir = fd.askdirectory()
    outdirinput.delete(0, END)
    outdirinput.insert(0, outdir)

def compile():
    print("test")

def urlopen(url):
    webbrowser.open_new_tab(url)


# Window Setup
root = Tk()
root.title("nmcfs Compiler")
root.geometry("300x500")
root.resizable(True, True)
root.minsize(300,500)
sv_ttk.set_theme("light")
im = Image.open('nmcfs_templogo.png')
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)


# DPI Scaling
ORIGINAL_DPI = 146.89156626506025
def get_dpi():
    screen = Tk()
    current_dpi = screen.winfo_fpixels('1i')
    screen.destroy()
    return current_dpi
SCALE = get_dpi()/ORIGINAL_DPI 

scaling_factor = root.tk.call("tk", "scaling")/SCALE 
def scale(value):
    if type(value) is int or type(value) is float or type(value) is complex:
        return max(int(value * scaling_factor), 1)
    elif type(value) is tuple:
        returnvalue = (max(value[0]*scaling_factor,1),max(value[1]*scaling_factor,1))
        return returnvalue
    else:
        raise Exception("Invalid Data Type")
    
# Frame Setup
frame1 = ttk.Frame(root)
frame1.grid(row=0, column=0, sticky="nsew", padx=scale(10), pady=scale(10))

# Configure Grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame1.grid_rowconfigure(8, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)

# Logo Setup
logoimg = Image.open("nmcfs_templogo.png")
logoimg = logoimg.resize((scale(50), scale(50)), Image.Resampling.LANCZOS)
logoimg = ImageTk.PhotoImage(logoimg)
logo = ttk.Label(frame1, image=logoimg)
logo.grid(row=0, column=0, columnspan=3)

# Main UI Elements
l = ttk.Label(frame1, text="nmcfs Compiler", font=("Helvetica", scale(8), "bold"))
l.grid(row=1, column=0, columnspan=3)

# Input Path
pathlabel1 = ttk.Label(frame1, text="File to compile:", font=("Helvetica", scale(4), "bold"))
pathlabel1.grid(row=2, column=0, sticky="w",pady=scale((30,0)),columnspan=2)

pathinput = ttk.Entry(frame1)
pathinput.grid(row=3, column=0, sticky="ew", columnspan=2,ipadx=scale(2000))

pathbutton = ttk.Button(frame1, text="Select", command=selectfile)
pathbutton.grid(row=3, column=2, padx=scale(5), pady=scale(0))

# Output Path
pathlabel2 = ttk.Label(frame1, text="Output Path:", font=("Helvetica", scale(4), "bold"))
pathlabel2.grid(row=4, column=0, sticky="w",columnspan=2,pady=scale((15,0)))

outdirinput = ttk.Entry(frame1)
outdirinput.grid(row=5, column=0, pady=scale(0), sticky="ew", columnspan=2)

pathbutton2 = ttk.Button(frame1, text="Select", command=selectdir)
pathbutton2.grid(row=5, column=2, padx=scale(5), pady=scale(0))

# License
licensetext = ttk.Label(
    frame1,
    text="nmcfs \u00a9 MIT License - 2025 Rosafy",
    foreground="blue",
    cursor="hand2",
    font=("Helvetica", scale(4)),
    wraplength=scale(70),
    justify="center",
)
licensetext.grid(row=9, column=0, columnspan=3,pady=0)
licensetext.bind("<Button-1>", lambda e: urlopen("https://github.com/rosafy/nmcfs/blob/main/LICENSE"))
ToolTip(licensetext, msg="Read License")

# Bottom Buttons
buttons = ttk.Frame(frame1)
buttons.grid(row=8, column=0, columnspan=3,pady=scale((15,0)))
quitbutton = ttk.Button(buttons, text="Quit", command=root.destroy,width=scale(7))
quitbutton.grid(row=0, column=1, sticky="sw",padx=scale((2.5,0)))

compilebutton = ttk.Button(buttons, text="Compile", command=compile, width=scale(7))
compilebutton.grid(row=0, column=0, sticky="se",padx=scale((0,2.5)))

# Run
root.mainloop()