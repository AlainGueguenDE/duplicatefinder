"""
a GUI for searching duplicate files , based on the couple size / hashtag
and disply the duplicated file
search on folder selected by users .
save 2 files:
  raw list of files (name path size hastag)
  list of duplicated files

Notes: dev on conda opencv38
       this is a testbed for developme net of guis in pycharm
"""
# from pycharm original template
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename,askdirectory,asksaveasfile,asksaveasfilename
import tktable
from pandastable import Table as pdTable  #, TableModel
import pandas as pd
import list_md5 as lsmd5

class duplicatfinder(tk.Frame):
    def __init__(self,master):
        self.dfduplicate=None
        self.master=master
        #super().__init__(*args, **kwargs)
        self.master.grid()
        #self.geometry("640x480")
        ttk.Style().configure('green/black.TLabel', foreground='green', background='black')
        ttk.Style().configure('green/black.TButton', foreground='green', background='black',highlightbackground ="#0000FF")

        self.greeting = ttk.Label(self.master,
                        text="Folders to search",
                        )

        self.buttonfolders = ttk.Button(self.master,
            text="select search folder",
            width=25,
            style='green/black.TButton',
            command=self.choosefolder
        )
        self.buttonfolderout = ttk.Button(self.master,
                                        text="save result as",
                                        width=25,
                                        style='green/black.TButton',
                                        command=self.choosefolderout
                                        )
        self.cleanselection = ttk.Button(self.master,
            text="Clear selection",
            width=25,
            command=self.clearselection
        )
        self.quitprogram = ttk.Button(self.master,
                                         text="Quit",
                                         width=25,
                                         command=self.master.destroy
                                         )
        self.buttonSub = ttk.Button(self.master,
            text="search duplicate",
            #width=25,
            command=self.show_output
        )
        self.buttonDisplay = ttk.Button(self.master,
            text="Display duplicate",
            #width=25,
            command=self.displaydfduplicate
        )

        self.ButtonProcess = ttk.Button(self.master,
            text="process duplicate",
            command=self.processduplicate
        )

        self.output = ttk.Label(self.master,text="output result file name")
        self.entry = ttk.Entry(self.master)#,fg="black", bg="white")
        self.text_box=tk.Text(self.master, width = 90 , height = 10)
        self.greeting.grid(column=0, row=0, sticky="W")
        self.buttonfolders.grid(column=0, row=1,sticky="W")
        self.cleanselection.grid(column=1, row=1,sticky="N")
        self.quitprogram.grid(column=3, row=1,sticky="E")
        self.text_box.grid(column=0, row=2,columnspan=4, rowspan=2,sticky="W")
        self.output.grid(column=0, row=4, columnspan=1, sticky="W")
        self.entry.grid(column=1, row=4, sticky="W")
        self.buttonfolderout.grid(column=2, row=4,sticky="W")
        self.buttonSub.grid(column=0, row=5, sticky="E")
        self.buttonDisplay.grid(column=2, row=5, sticky="W")
        self.ButtonProcess.grid(column=3 , row=5,sticky="nsew")
        self.containerframe = ttk.Frame(self.master )#,width=3000)#,columnspan=640)
        self.containerframe.grid(column=0,
                                 row=7,
                                 columnspan=640,
                                 sticky="nsew",

                                 )
        self.containerframe.grid_propagate(True)
        self.pt = pdTable(self.containerframe,
                          sticky="nsew",
                          editable = TRUE)
        self.pt.show()
        #self.containerframe.grid_propagate(True)

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
        fulldf,duplicatedDF,nbelemfound=lsmd5.creatDFmd5LST(lsttxt,resultname)# ./anewdatframde.csv")
        self.dfduplicate=duplicatedDF #.sort_values(['size', 'hashmd5'], ascending=[False, True])
        print ("-----")
        print (self.dfduplicate)
        print ("-----")
        print (duplicatedDF)
        print ("-----")


        print ("fini")


    def choosefolder(self):
        filename = askdirectory()
        self.text_box.insert("1.0", "%s\n"%filename)
        return filename
    def choosefolderout(self):
        filename = asksaveasfilename(confirmoverwrite=False)
        self.entry.insert(0, "%s\n"%filename)
        return filename

    def clearselection(self):
        self.text_box.delete('1.0', tk.END)

    def displaydfduplicate(self):
        #print (self.dfduplicat.to_string)
        #self.dfdisplay.insert("",'end',iid=1,text='First',values=(1,'n1-Alex','tr,','quart'))
        crti=1
        for ind in self.dfduplicate.index:
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
                    self.dfduplicate['filename'][ind],
                    self.dfduplicate['filepath'][ind],
                    self.dfduplicate['size'][ind]
                    )
        self.pt = pt = pdTable(self.containerframe, dataframe=self.dfduplicate,
                                    showtoolbar=True, showstatusbar=True)
        #self.pt.addColumn()#newname='selectionbooleenne')



        self.pt.show()
            #self.pt.insert_row(
            #self.table.tag_configure(self.dfduplicat['filename'][ind],background="yellow")
            #self.table.insert_row(row1)
            #row2 = ("John", 15, "john@gmail.com")
            #mytable.
            #self.table.insert_row(row2)
        crti += 1

    def processduplicate(self):
        for ind in self.dfduplicate.index:
            print (ind)
        print ("content of container")
        pifpof = self.pt
        print (type(pifpof))
        for row in pifpof.iterrows():
            print (row)
        #for element  n self.pt:
        #    print (element )

if __name__ == '__main__':

    main_window = tk.Tk()
    combo = duplicatfinder(main_window)
    main_window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
