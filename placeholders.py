import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    '''Custom modern Placeholder Entry box, takes positional argument master and placeholder\n
    
    BUG 1: Possible bugs with binding to this class\n
    BUG 2: Anomalous behaviour with config or configure method
    '''

    def __init__(self, master, placeholder, **kwargs):
        # Style for ttk widget
        self.__s = ttk.Style()
        self.__s.configure('my.TEntry', foreground='black', font=(0, 0, 'normal'))
        self.__s.configure('placeholder.TEntry', foreground='grey', font=(0, 0, 'bold'))

        # Init entry box
        ttk.Entry.__init__(self, master,style='my.TEntry', **kwargs)
        self.text = placeholder
        self.__has_placeholder = False  # placeholder flag

        # Add placeholder if box empty
        self.__add()

        # Bindings of the widget
        self.bind('<FocusIn>', self.__clear)
        self.bind('<FocusOut>', self.__add)
        self.bind('<KeyRelease>',self.__normal)

    def __clear(self, *args):
        """Function to clear the placeholder"""
        if super().get() == self.text and self.__has_placeholder:  # remove placeholder when focus gain
            super().delete(0, tk.END)
            self.configure(style='my.TEntry')
            self.__has_placeholder = False  # set flag to false

    def __add(self, *args):
        """Function to add the placeholder"""
        if super().get() == '' and not self.__has_placeholder:  # if no text add placeholder
            self.configure(style='placeholder.TEntry')
            super().insert(0, self.text)  # insert placeholder
            self.icursor(0)  # move insertion cursor to start of entrybox
            self.__has_placeholder = True  # set flag to true

    def __normal(self, *args):
        """Method to revert to normal properties"""
        self.__add()  # if empty add placeholder
        if super().get() == self.text and self.__has_placeholder:  # clear the placeholder if starts typing
            self.bind('<Key>', self.__clear)
            self.icursor(-1)  # keep insertion cursor to the end
        else:
            self.configure(style='my.TEntry')  # set normal font

    def get(self):
        """Function to get the contents of the Entry widget"""
        if super().get() == self.text and self.__has_placeholder:
            return ''
        else:
            return super().get()

    def insert(self, index, string):
        """Function to insert into the Entry widget"""
        self.__clear()
        super().insert(index, string)

    def delete(self, first, last):
        """Function to delete text inside the Entry widget"""
        if super().get() != self.text:
            super().delete(first, last)
            self.__add()
        elif self.get() == self.text and not self.__has_placeholder:
            super().delete(first, last)
            self.__add()

if __name__ == '__main__':
    root = tk.Tk()
    e = PlaceholderEntry(root,placeholder='Enter your name: ')
    e.pack(padx=10,pady=10)

    b = ttk.Button(root,text='FOCUS!',command=lambda: print(len(e.get())))
    b.pack()

    root.mainloop()