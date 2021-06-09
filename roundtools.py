import tkinter as tk
from tkinter import ttk

class RoundedToolTip:
    """Custom rounded tooltips, easy to use, specify widget and text as positional arguments
 
    Keyword Arguments:
        triggerkey  -- Which key/event(default is <Enter>) triggers the tooltip to show
        
        releasekey  -- Which key/event hides(default is <Leave>) the tooltip
        
        bg          -- Background color of tooltip window(default-white), accepts hex and standard colors
        
        fg          -- Foreground color/Font color of the text, accepts hex and standard colors
        
        delayed     -- Show the tooltip when triggered, or wait(default-True)

        delaytime   -- Time taken to wait and show the tooltip in ms(default-1000)

        fadein      -- Default is set to 'enabled', set to 'disabled' to disable fadein of the tooltip

        fadeout     -- Default is set to 'enabled', set to 'disabled' to disable fadeout of the tooltip
        
        shadowed    -- Default is set to True, gives a drop shadow effect
        
        shadowcolor -- Default set to 'black', changes the color of the drop shadow, if enabled
        
        side        -- Default is set to 'right', change side to 'left' for tooltip on left side
        
        onpress     -- Default is True, hides tooltip on press of other key or left mousclick
    """
    def __init__(self, widget: tk.Widget, text: str, triggerkey: str='<Enter>', releasekey: str='<Leave>', bg: str='white', delayed: bool=True, delaytime: int=1000, fg: str='black', fadeout: str='enabled', fadein: str='enabled', shadowed: bool=True, shadowcolor: str='black', outlinecolor: str='black', side: str='right', onpress: bool=True):
        
        # Widget properties
        self.widget          = widget
        self.text            = text
        self.bg              = bg
        self.fg              = fg
        self.fadeout         = fadeout
        self.fadein          = fadein
        self.side            = side
        self.onpress         = onpress
        self.delayed         = delayed
        self.delaytime       = delaytime
        self.shadowed        = shadowed
        self.outlinecolor    = outlinecolor
        if self.shadowed:
            self.shadowcolor = shadowcolor

        # Widget attributes
        self.__time          = 0
        self.__once          = False
        self.__hidden        = True
        args                 = dict(locals())
        del args['self']

        # Perform type check on the inserted values
        self.__type_check(args)

        # Making the window
        self.__master = tk.Toplevel()
        self.__master.attributes('-alpha', 0)  # Hide the window
        self.__master.overrideredirect(1)
        self.__master.attributes('-topmost', True)
        self.__master.attributes('-transparentcolor', '#f0f0f0')  # Green key
        
        self.__frame = tk.Frame(self.__master)
        self.__frame.pack(expand=1)

        # Dummy widget to get size of text
        self.__label = tk.Label(self.__frame, text=self.text)
        self.__label.grid(row=0, column=0,ipadx=5,ipady=5)
        self.__master.update()
        h,w = self.__label.winfo_height(),self.__label.winfo_width()
        self.__label.grid_remove()

        # Canvas for rounded box
        self.__canvas = tk.Canvas(self.__frame)
        self.__canvas.grid(row=0,column=0)

        # Multiple rectangles for shadows
        if self.shadowed:
            for i in range(3):
                self.__round_rectangle(5,5,w+i,h+i, radius=25, fill=self.shadowcolor,tag=f'shadow{i}') # Add shadow color
        # Main rounded rectangle
        self.__round_rectangle(5,5,w,h, radius=25, fill=self.bg ,outline=self.outlinecolor,tag='frame')
        # Text for the widget
        self.__canvas.create_text((5+w)/2,(5+h)/2,text=text, fill=self.fg, tag='text')

        # Widget bindings
        if self.onpress:
            self.widget.bind('<ButtonPress>', self.__remove)
            self.widget.bind('<Key>', self.__remove)
        self.widget.bind(triggerkey, self.__start_timer)
        self.widget.bind(releasekey, self.__re_timer)
            
    def __add(self, event):
        """Function to fade and show tooltip"""

        def show():
            """Function to add the tooltip on the calculated dimensions"""
            if self.side.lower() == 'right':
                # Window size
                w = self.__label.winfo_width() + 10
                h = self.__label.winfo_height() + 10

                # Offset size
                offset_x = event.widget.winfo_width()
                offset_y = 2
                self.x = event.widget.winfo_rootx() + offset_x
                self.y = event.widget.winfo_rooty() + offset_y

                # Apply geometry
                self.__master.geometry(f'{w}x{h}+{self.x}+{self.y}')

                # Bringing the visibility of the window back
                # self.__master.attributes('-alpha', 1)
                # self.__hidden = False  # Setting status to false
            
            elif self.side.lower() == 'left':
                # Window size
                w = self.__label.winfo_width() + 10
                h = self.__label.winfo_height() + 10

                # Offset size
                offset_x = 5
                offset_y = 5
                self.x = event.widget.winfo_rootx() - w
                self.y = event.widget.winfo_rooty() + offset_y

                # Apply geometry
                self.__master.geometry(f'{w}x{h}+{self.x}+{self.y}')

                # Bringing the visibility of the window back
                # self.__master.attributes('-alpha', 1)
                # self.__hidden = False  # Setting status to false
            
            else:
                raise tk.TclError(f"Unknown value '{self.side}' for option -side. Must be right or left")        
        
        x,y = self.__master.winfo_pointerx(),self.__master.winfo_pointery()
        wid = self.__master.winfo_containing(x,y)        
        if wid == self.widget:

            if self.__hidden:
                show()
            
            if self.fadein.lower() == 'enabled':  # If fadeout enabled
                # print(self.__master.attributes('-alpha'))
                if self.__hidden:  # If window is hidden
                    alpha = self.__master.attributes('-alpha')
                    if alpha < 1:
                        alpha += 0.10
                        self.__master.attributes('-alpha', alpha)
                        self.__master.after(20, self.__add, event)
                    else:
                        self.__hidden = False

                else:
                    self.__master.attributes('-alpha', 1)  # show the window

            elif self.fadein.lower() == 'disabled':  # If fadeout disabled
                if self.__hidden:
                    self.__master.attributes('-alpha', 1)
                    self.__hidden = False

            else:
                raise tk.TclError(f"Unknown value '{self.fadein}' option -fadeout. Must be 'enabled' or 'disabled'")
        
        else:
            self.clear()

    def __remove(self, *args):
        """Function to remove tooltip with/without fade effect"""

        if self.fadeout.lower() == 'enabled':  # If fadeout enabled
            if not self.__hidden:  # If window is not hidden
                alpha = self.__master.attributes('-alpha')
                if alpha > 0:
                    alpha -= 0.10
                    self.__master.attributes('-alpha', alpha)
                    self.__master.after(20, self.__remove)
                    # print('remove')
                else:
                    self.__hidden = True

            else:
                self.__master.attributes('-alpha', 0)  # Hide the window

        elif self.fadeout.lower() == 'disabled':  # If fadeout disabled
            if not self.__hidden:
                self.__master.attributes('-alpha', 0)
                self.__hidden = True

        else:
            raise tk.TclError(f"Unknown value '{self.fadeout}' option -fadeout. Must be 'enabled' or 'disabled'")

    def clear(self):
        """Function to destroy the tooltip window"""
        self.__master.attributes('-alpha',0)
        self.__hidden = True
    
    def __start_timer(self,e):
        """Function to start the wait timer"""
        if self.delayed:
            self.__time += 1

            if self.__time >= self.delaytime and self.__hidden and not self.__once:           
                self.__add(e)
                self.__once = True
        
            self.rep = self.widget.after(1,self.__start_timer,e)
        else:
            self.__add(e)

    def __re_timer(self,e=None):
        """Function to restart the timer"""
        if self.delayed:
            self.__time = 0
            self.widget.after_cancel(self.rep)
            self.__remove()
            self.__once = False
        
        else:
            self.__remove()

    def __round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """To create rounded rectangle, taken from the SO answer"""
        # https://stackoverflow.com/q/44099594/13382000
        points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
        
        return self.__canvas.create_polygon(points, **kwargs, smooth=True)

    def __update_rectangle_coords(self, round_rect, x1, y1, x2, y2, radius=25):
        """Function to update the given rounded rectange"""
        points = (x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1)
        self.__canvas.coords(round_rect, *points)

    def __type_check(self,args):
        """Function for type inspection on runtime"""
        for k,v in zip(self.__init__.__annotations__.items(),args.values()):
            if not isinstance(v,k[1]):
                raise TypeError(f"Invalid type '{type(v)}' for property -{k[0]}, valid type is '{k[1]}'")

    def config_text(self,text):
        """Function to update the text of tooltip"""

        self.__label.config(text=text)
        self.__label.grid(row=0,column=0,ipadx=5,ipady=5)
        self.__master.update()
        h,w = self.__label.winfo_height(),self.__label.winfo_width()
        self.__label.grid_forget()
        
        self.__update_rectangle_coords('frame',5,5,w,h)
        self.__canvas.coords('text',(5+w)/2,(5+h)/2)
        self.__canvas.itemconfig('text',text=text)
        if self.shadowed:
            for i in range(3):
                self.__update_rectangle_coords(f'shadow{i}',5,5,w+i,h+i)

class ToolTip():
    '''
    Custom Tooltips, easy to use, specify widget and text as positional arguments\n
    Additional Arguments:\n
    triggerkey - Which key triggers the placeholder\n
    releasekey - Which key hides the placeholder\n
    bg - Background color of tooltip window(default-yellow-ish), accepts hex and standard colors\n
    fg - Foreground color/Font color of the text, accepts hex and standard colors\n
    fadeout - Default set to 'enabled', set to 'disabled' to disable fadeout of tooltip\n
    ISSUE: What if user want it on left side?
    '''

    def __init__(self, widget, text, triggerkey='<Enter>', releasekey='<Leave>', bg='#ffffe0', fg='black', side='right', fadeout='enabled'):
        # basic widget attributes
        self.widget = widget
        self.text = text
        self.bg = bg
        self.side = side
        self.fg = fg
        self.fadeout = fadeout

        # making the tooltip
        self.master = tk.Toplevel()
        self.master.attributes('-alpha', 0)  # hide the window
        self.master.attributes('-transparentcolor', '#f0f0f0')  # hide the window
        self.master.overrideredirect(1)
        self.master.attributes('-topmost', True)
        self.frame = tk.Frame(self.master, bg=self.bg, highlightbackground="black",
                              highlightcolor="black", highlightthickness=1)
        self.frame.pack(expand=1, fill='x')
        self.label = tk.Label(self.frame, text=self.text,
                              bg=self.bg, justify=tk.LEFT, fg=self.fg)
        self.label.grid(row=0, column=0)

        # widget binding
        self.widget.bind(triggerkey, self.add)
        self.widget.bind(releasekey, self.remove)
        self.widget.bind('<ButtonPress>', self.remove)

        # reference to window status
        self.hidden = True

    def add(self, event):
        if self.side.lower() == 'right':
            # Window size
            w = self.label.winfo_width() + 10
            h = self.label.winfo_height() + 10

            # Offset size
            offset_x = event.widget.winfo_width()
            offset_y = 2
            self.x = event.widget.winfo_rootx() + offset_x
            self.y = event.widget.winfo_rooty() + offset_y

            # Apply geometry
            self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')

            # Bringing the visibility of the window back
            self.master.attributes('-alpha', 1)
            self.hidden = False  # Setting status to false
        
        elif self.side.lower() == 'left':
            # Window size
            w = self.label.winfo_width() + 10
            h = self.label.winfo_height() + 10

            # Offset size
            offset_x = 5
            offset_y = 5
            self.x = event.widget.winfo_rootx() - w
            self.y = event.widget.winfo_rooty() + offset_y

            # Apply geometry
            self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')

            # Bringing the visibility of the window back
            self.master.attributes('-alpha', 1)
            self.hidden = False  # Setting status to false
        
        else:
            raise tk.TclError(f"Unknown value '{self.side}' for option -side. Must be right or left")

    def remove(self, *args):
        if self.fadeout.lower() == 'enabled':  # If fadeout enabled

            if not self.hidden:  # If window is not hidden
                alpha = self.master.attributes('-alpha')
                if alpha > 0:
                    alpha -= 0.10
                    self.master.attributes('-alpha', alpha)
                    self.master.after(20, self.remove)

            else:
                self.master.attributes('-alpha', 0)  # Hide the window

        elif self.fadeout.lower() == 'disabled':  # If fadeout disabled
            if not self.hidden:
                self.master.attributes('-alpha', 0)
                self.hidden = True

        else:
            raise tk.TclError(f"Unknown value '{self.fadeout}' option -fadeout. Must be 'enabled' or 'disabled'")

    def clear(self):
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    
    b = tk.Button(root,text='popit out')
    b.pack()
    b1 = tk.Button(root,text='popit out')
    b1.pack(pady=10)
    ToolTip(b,text='Damn this is so neat\nI like it haha')
    RoundedToolTip(b1,text='Damn this is so neat\nI like it haha')
    # print(a.__doc__)
    # ToolTip(b1,text='Damn this is so neat\nI like it haha',side='left')
    
    root.mainloop()
