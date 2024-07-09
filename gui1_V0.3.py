"""
 A prototype for a duplicate file finder with a graphical interface
 this program is an attempt to learn and use the tkinter graphical interface around a duplicate file finder script also accessible through
 the command line as an external package  list_md5

 the code explore various approach for the desing and implementation of graphical interfaces.
 the duplicate files are identified  in comparing size and MD5 checksum  over file s form different locations.
 Author Alain Gueguen gueguen.alain@gmail.com  2023/2024
"""

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename,askdirectory
#import tktable
from pandastable import Table as pdTable
import pandas as pd

import list_md5 as lsmd5
#from pandastable import TableModel
#from ttkwidgets import CheckboxTreeview
#new comment

#text_box=None
class duplicatfinder(tk.Frame):

    def __init__(self,master):
        self.dfduplicate=None
        self.master=master
        #super().__iint__(*args, **kwargs)
        self.master.grid()
        #self.geometry("640x480")
        #self.master.grid_columnconfigure(0, weight=1)
        #self.master.grid_columnconfigure(1, weight=2)
        #self.master.grid_columnconfigure(2, weight=1)
        #self.master.grid_rowconfigure(0, weight=1)
        #self.master.grid_rowconfigure(1, weight=1)
        #self.master.grid_rowconfigure(2, weight=3)
        #self.master.grid_rowconfigure(3, weight=1)
        #self.master.grid_rowconfigure(4, weight=1)

        ttk.Style().configure('green/black.TLabel', foreground='green', background='black')
        ttk.Style().configure('green/black.TButton', foreground='green', background='black',highlightbackground ="#0000FF")

        self.greeting = ttk.Label(self.master,
                        #column=0, row=0,
                        #bg="grey",
                        #fg="blue",
                        text="Folders to search",
                        )

        self.buttonfolders = ttk.Button(self.master,
            #column=0, row=1,
            text="select",
            width=25,
            #height=1,
            #bg="grey",
            #fg="black",
            #highlightbackground='black',
            style='green/black.TButton',
            command=self.choosefolder
        )
        self.cleanselection = ttk.Button(self.master,
            #column=1, row=1,
            text="Clear selection",
            width=25,
            #height=1,

            #bg="grey",
            #fg="black",
            command=self.clearselection
        )

        self.buttonSub = ttk.Button(self.master,
            text="Submit",
            width=25,
            #height=1,
            #bg="grey",
            #fg="black",
            command=self.show_output
        )
        self.buttonDisplay = ttk.Button(self.master,
            text="Display duplicate",
            width=25,
            #height=1,
            #bg="grey",
            #fg="black",
            command=self.displaydfduplicate
        )

        self.output = ttk.Label(self.master,text="output result file name")
        self.entry = ttk.Entry(self.master)#,fg="black", bg="white")
        self.text_box=tk.Text(self.master, width = 95 , height = 10)
        self.status_box = tk.Text(self.master, width=95, height=10)
        #greeting.place(x=5,y=1)
        self.greeting.grid(column=0, row=0, sticky="W")
        #buttonfolders.pack(side=tk.LEFT)
        self.buttonfolders.grid(column=0, row=1,sticky="W")#, sticky="NSEW")   #.place(x=5,y=20)
        #cleanselection.pack(side=tk.RIGHT)
        self.cleanselection.grid(column=3, row=1,sticky="E")#, sticky="NSEW")   #.place(x=200,y=20)

        self.text_box.grid(column=0, row=2, columnspan=4, rowspan=2, sticky="W")  # , sticky="NSEW")   #.place(x=5,y=70)
        self.status_box.grid(column=5, row=2, columnspan=2, rowspan=2, sticky="W")  # , sticky="NSEW")   #.place(x=5,y=70)

        self.output.grid(column=0, row=4, columnspan=1, sticky="W")
        self.entry.grid(column=1, row=4, columnspan=3, sticky="W")   #.place(x=150,y=400)#pack()#side = tk.RIGHT)
        self.buttonSub.grid(column=0, row=5, sticky="NSEW")   #..place(x=6,y=450)#pack()#side = tk.RIGHT)
        self.buttonDisplay.grid(column=1, row=5, sticky="NSEW")
        self.containerframe = ttk.Frame(self.master)
        self.containerframe.grid(column=0, row=9, columnspan=7,sticky="NSEW")
        self.pt = pdTable(self.containerframe)
        self.pt.show()

        #tree = CheckboxTreeview(root)

        ####self.dfdisplay = ttk.Treeview(self.master,columns=('select','filename','path','size'))#, width = 95 , height = 10)


        #####trv.grid(row=1,column=1,padx=30,pady=20)
        ####self.dfdisplay["columns"]=('select','filename','path','size')
        ##### column identifiers
        #####trv["columns"] = ("1", "2","3)
        ##### Defining headings, other option is tree
        ####self.dfdisplay['show'] = 'headings'
        #####tree['show'] = 'headings'
        ##### width of columns and alignment
        #####self.dfdisplay.column("#0", width = 10, anchor ='c')
        ####self.dfdisplay.column("select"  , width = 100, anchor ='c')
        ####self.dfdisplay.column("filename", width = 300, anchor ='c')
        ####self.dfdisplay.column("path"    , width = 500, anchor ='c')
        ####self.dfdisplay.column("size"    , width = 80, anchor ='c')

        # Headings
        # respective columns
        #self.dfdisplay.heading("#0", text ="Label"       )#   ,anchor='c')
        ####self.dfdisplay.heading("select"  , text="select")#
        ####self.dfdisplay.heading("filename", text="Name"  )#   ,anchor='c')
        ####self.dfdisplay.heading("path"   , text="path")   #
        ####self.dfdisplay.heading("size"   , text="size"   )#   ,anchor='c')
        #####self.dfdisplay.tag_configure('gray', background='#cccccc')
        ####self.dfdisplay.grid(column=0, row=6, columnspan=6,sticky="W")


        #self.table = tktable.Table(self.master,columns=('select','filename','path','size'))#,rows=10, cols=4)
        #self.table.column(0, width = 100, anchor ='c')
        #self.table.column(1, width = 300, anchor ='c')
        #self.table.column(2, width = 500, anchor ='c')
        #self.table.column(3, width = 80, anchor ='c')
        # bg='gray30', fg='white'

        ##self.table.grid(column=0, row=9, columnspan=6,sticky="W") #(side="top", fill="both", expand=True)
        #insert("1.0", "%s\n"%filename)
        #height = 5
        #width = 5
        #self.b=tk.Entry(master , text="")
        #for i in range(height): #Rows
            #for j in range(width): #Columns
                #self.b = tk.Entry(master , text="")
                #self.b.grid(row=i, column=j)

        #self.mainloop()

    def show_output(self):
        texts=self.text_box.get("1.0",tk.END)
        print (type(texts))
        lsttxt=texts.split('\n')
        print (lsttxt)
        outfilename=self.entry.get()#"1.0",tk.END)
        resultname="./anewdatframde.csv"
        if len(outfilename)>0:
            if outfilename.endswith(".csv"):
                resultname=outfilename
            else:
                resultname="%s.csv"%outfilename

        #lsmd5.creatDFmd5(lsttxt[0],"./anewdatframde.csv")
        #fulldf,duplicatedDF,nbelemfound=lsmd5.creatDFmd5LST(lsttxt,resultname)# ./anewdatframde.csv")
        fulldf,duplicatedDF,nbelemfound=lsmd5.creatDFmd5LST_feedback(lsttxt,resultname,self)
        self.dfduplicat=duplicatedDF #.sort_values(['size', 'hashmd5'], ascending=[False, True])
        print ("-----")
        print (self.dfduplicat)
        print ("-----")
        print (duplicatedDF)
        print ("-----")


        print ("fini")


    def choosefolder(self):
        filename = askdirectory()
        self.text_box.insert("1.0", "%s\n"%filename)
        return filename

    def clearselection(self):
        self.text_box.delete('1.0', tk.END)

    def displaydfduplicate(self):
        #print (self.dfduplicat.to_string)
        #self.dfdisplay.insert("",'end',iid=1,text='First',values=(1,'n1-Alex','tr,','quart'))
        crti=1
        for ind in self.dfduplicat.index:
            print ("index",ind)
            #['filename', 'filepath','size','hashmd5' ,
            #print(self.dfduplicat['filename'][ind], self.dfduplicat['filepath'][ind], self.dfduplicat['size'][ind],self.dfduplicat['hashmd5'][ind])

            #self.dfdisplay.insert("",'end',
            #                      iid=crti ,
            #                      text='bla%s'%crti,
            #                      values=(
            #                        "OK",
            #                        self.dfduplicat['filename'][ind],
            #                        self.dfduplicat['filepath'][ind],
            #                        self.dfduplicat['size'][ind],

            #                      ))
            var = IntVar()
            served = ttk.Checkbutton(self.master, text="", variable=var)
            row1 = ( served,
                    self.dfduplicat['filename'][ind],
                    self.dfduplicat['filepath'][ind],
                    self.dfduplicat['size'][ind]
                    )
        self.pt = pt = pdTable(self.containerframe, dataframe=self.dfduplicat,
                                    showtoolbar=True, showstatusbar=True)
        self.pt.show()
        crti+=1

            #self.pt.insert_row(
            #self.table.tag_configure(self.dfduplicat['filename'][ind],background="yellow")
            #self.table.insert_row(row1)
            #row2 = ("John", 15, "john@gmail.com")
            #mytable.
            #self.table.insert_row(row2)


#self.dfduplicat['hashmd5'][ind])
            #self.dfdisplay.insert("",'end',iid=1,text='First',values=(1,'n1-Alex'))
            #self.dfdisplay.insert("",'end',iid=2,text='second',values=(2,'n2-Ravi'))
            #self.dfdisplay.insert("",'end',iid=3,text='third',values=(3,'n3-Ronn'))
                #1,'n1-Alex','tr,','quart'))
             #trv.insert("",'end',iid=1,text='First',values=(1,'n1-Alex'))
        #df = TableModel.getSampleData()
        #self.table = pt = Table(f, dataframe=df,
        #                            showtoolbar=True, showstatusbar=True)




    #def windowcreation():


#if __name__ == "__main__":
#    windowcreation()
main_window = tk.Tk()
combo = duplicatfinder(main_window)
#combo.pack(fill="both", expand=True)
#combo.config(width=600, height=600
#combo.text_box.config(font=("consolas", 12), undo=True, wrap='word')
#combo.text_box.config(borderwidth=3, relief="sunken")

#style = ttk.Style()
#style.theme_use('clam')

main_window.mainloop()

