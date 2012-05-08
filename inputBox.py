#!/usr/bin/env python

import Tkinter
import getopt
import sys
import os

# --2011.01.15 PM 06:12 Created by xialulee--
#   accept -e or --encode for encoding received text
#
# --For MSYS BASH--
# --ActivePython 2.6.6.15--
# --Windows 7--
# --xialulee--

ERROR_NOERROR, ERROR_PARAM = range(2)

def usage():
    perr = sys.stderr.write
    perr('Usage: %s [options]\n' % (os.path.split(sys.argv[0])[-1],))
    perr('Popup a textbox whose contents will copy to stdout\n')
    perr('\n')
    perr(' -e, --encode=CODE\tuse the CODE to encode the text in the textbox before\n\t\t\tcopying it to stdout\n')
    perr(' -h, --help\t\tdisplay this help and exit\n')

def main():

    root = Tkinter.Tk()
    ent  = Tkinter.Entry(root)
    ent.pack()
    ent.focus()
  
    ent.bind('<Return>', (lambda event: root.quit()))
    root.mainloop()
    text = ent.get()

    print text

if __name__ == '__main__':
    main()
