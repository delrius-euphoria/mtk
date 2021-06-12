import tkinter as tk

class MButton(tk.Button):
    def __init__(self,master,hovfg='default',spacize=False,hovbg='default',padder=30,unit='default',*args,**kwargs):
        
        # Initialization of the button
        if unit == 'px':
            self.img = tk.PhotoImage(width=1,height=1)
            tk.Button.__init__(self,master,image=self.img,compound='top',relief='flat',bd=0,*args,**kwargs)
        elif unit == 'default':
            tk.Button.__init__(self,master,bd=0,*args,**kwargs)
        else:
            raise TypeError(f"Unknown value '{unit}' option -unit. Must be 'px' or 'default'")
    
        # to add a space between each character
        if spacize:
            new_txt = ' '.join(self['text'])
            self['text'] = new_txt

        self.hovfg = hovfg
        self.hovbg = hovbg

        # Initial colors 
        self.fg,self.bg = self.cget('fg'),self.cget('bg')

        # Set the new dimensions with padder
        w = self.winfo_reqwidth()  
        self.config(width=w+padder)

        # Binding on the widgets
        self.bind('<Enter>',self.enter)
        self.bind('<Leave>',self.leave)

    def enter(self,e):
        """Function to set colors on hover"""
        if (self.hovfg,self.hovbg) == ('default','default'):
            self.config(bg=self.fg,fg=self.bg)
        else:
            self.config(bg=self.hovbg,fg=self.hovfg)

    def leave(self,e):
        """Function to change colors on mouse leave"""
        if (self.hovfg,self.hovbg) == ('default','default'):
            fg,bg = self.cget('fg'),self.cget('bg')
            self.config(bg=fg,fg=bg)
        else:
            self.config(bg=self.bg,fg=self.fg)

if __name__ == '__main__':
    root = tk.Tk()

    a = MButton(root,text='HELLO',bg='black',fg='white',hovfg='#fbc531',hovbg='#192a56',spacize=True,font=('calibri',21), unit='px')
    a.pack()
    
    root.mainloop()