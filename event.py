from Tkinter import *
import ttk

root = Tk()

def calculate(*args) :
    value = float(feet.get())
    meters.set((0.305 * value * 10000. + .5)/10000.)

def callback_function(*args) :
    meters.set('blue')

mf = ttk.Frame(root, padding="3 3 12 12")
mf.grid(column=0, row=0, sticky=(N, W, E, S))
mf.columnconfigure(0, weight=1)
mf.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mf, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mf, textvariable=meters, background='#E9D66B').grid(column=2,
          row=2, sticky=(W, E))

ttk.Button(mf, text="Calculate", command=calculate).grid(column=2,row=3,
          sticky=W)

ttk.Label(mf, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mf, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mf, text="meters").grid(column=3, row=2, sticky=W)

for child in mf.winfo_children():
   child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)

# this is the key line
root.bind('red', callback_function)

root.mainloop()
