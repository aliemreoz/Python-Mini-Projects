from Tkinter import *
import tkFileDialog
import tkMessageBox
import clusters

class Main():
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE)
        self.root.title("Course Analyzer - Sehir Limited Edition")

        self.GUI()


        self.course_name=[]
        self.course_desc=[]
        self.selected_courses=[]
        self.SelectedCourses={}
        self.LastDict={}
        self.selected_course_name=[]
        self.CC_List=[]
        self.GC_List=[]
        self.CD={}
        self.last_CD={}

        self.root.mainloop()

    def GUI(self):

        self.label = Label(text = "COURSE ANAYLZER - SEHIR LIMITED EDITION",bg = "red", font = "Helvetica 17 bold", fg = "white", width =86)
        self.label.grid(row= 0,column=0, columnspan = 20 , sticky = "WE")

        self.label2 = Label(text= "Upload a file that contains course descriptions: ",font = "Helvetica 12")
        self.label2.grid(row= 1,column=4, columnspan = 8 , sticky = "W",pady=20)

        self.label3 = Label(text= "Selected File: ",font = "Helvetica 12")
        self.label3.grid(row= 2,column=4, columnspan = 3 , sticky = "W")

        self.browse_button= Button(text = "Browse", font = "Helvetica 11",command=self.browse_file_func)
        self.browse_button.grid(row=1,column=11, columnspan=2, sticky="WE")

        self.canvas= Canvas(height=42,width=550,)
        self.canvas.create_rectangle(10,10,470,35,)
        self.canvas.create_text(235,22,font="Helvetica 11  ",text="Please select a file.")
        self.canvas.grid(row=2,column=8, columnspan=8, sticky="WE")

        self.canvas2=Canvas(height=5,width=1200,)
        self.canvas2.create_line(50,0,1150,0,width=5)
        self.canvas2.grid(row=3,column=0,columnspan=18)

        self.label4 = Label(text= "Similarity Measure: ",font = "Helvetica 10")
        self.label4.grid(row= 5,column=4, columnspan = 3 , sticky = "W",)

        self.var = IntVar()
        self.radiobutton1=Radiobutton(text="Pearson",font="Helvetica 10",variable=self.var, value=1)
        self.radiobutton1.grid(row=4,column=8,columnspan=2)
        self.radiobutton2=Radiobutton(text="Tanimoto",font="Helvetica 10",variable=self.var, value=2)
        self.radiobutton2.grid(row=6,column=8,columnspan=2)

        self.label5 = Label(text= "Select Course Codes: ",font = "Helvetica 10")
        self.label5.grid(row=4,column=11,columnspan=3)

        self.listbox = Listbox(height=7,selectmode="multiple")
        self.listbox.grid(column=14,row=4,rowspan=3,columnspan=2,sticky= "WE")
        self.scroll1=Scrollbar(command=self.listbox.yview,orient=VERTICAL)
        self.scroll1.grid(column=16,row=4,rowspan=3,sticky="WNS")
        self.listbox.configure(yscrollcommand=self.scroll1.set)

        self.firstbutton=Button(text="Draw Hierarchical Cluster Diagram",font = "Helvetica 10",)
        self.firstbutton.grid(row=7, column=2, columnspan=4,stick="WE",pady=5)

        self.secondbutton=Button(text="Print Hierarchical Cluster as Text",font = "Helvetica 10",command=self.PrintClust)
        self.secondbutton.grid(row=7, column=7, columnspan=4,stick="WE",pady=5)

        self.thirdbutton=Button(text="Show Data Matrix",font = "Helvetica 10",command=self.AddDataMatrix)
        self.thirdbutton.grid(row=7, column=12, columnspan=3,stick="WE",pady=5)

    def browse_file_func(self):

            self.file_path = tkFileDialog.askopenfilename(title='Please select a directory')

            if ".txt" not in self.file_path:
                #if selected file is not an txt file, the program will show error
                tkMessageBox.showerror("File Error", "The chosen file is not a txt file. Be sure you selected a txt file.")

                self.canvas= Canvas(height=42,width=550,)
                self.canvas.create_rectangle(10,10,470,35,)
                self.canvas.create_text(235,22,font="Helvetica 11  ",text="You selected non-txt file, select again!")
                self.canvas.grid(row=2,column=8, columnspan=8, sticky="WE")

                self.listbox.delete(0, END)

            else:

                if "courses_" not in self.file_path:
                #if selected file is not an proper txt file, the program will show error
                    tkMessageBox.showerror("File Error", "The chosen file is not proper. Be sure you selected a correct file.")

                    self.canvas= Canvas(height=42,width=550,)
                    self.canvas.create_rectangle(10,10,470,35,)
                    self.canvas.create_text(235,22,font="Helvetica 11  ",text="You selected unproper file, select again!")
                    self.canvas.grid(row=2,column=8, columnspan=8, sticky="WE")
                    self.listbox.delete(0, END)

                else:

                    self.canvas= Canvas(height=42,width=550,)
                    self.canvas.create_rectangle(10,10,470,35,)
                    self.canvas.create_text(235,22,font="Helvetica 11  ",text=self.file_path)
                    self.canvas.grid(row=2,column=8, columnspan=8, sticky="WE")

                    self.Func()
                    self.ListBoxFunc()


    def Func(self):
        #opening the txt file
        self.file=open(self.file_path,"r")
        self.line_list=(self.file.readlines())

        #splitting txt file by their line index, even lines are course name, odd lines are course description
        i = 0
        for line in self.line_list:
            if i % 2 == 0 :
                self.course_name.append(line)
            else:
                self.course_desc.append(line)
            i += 1

        j=0
        for i in self.course_name:
            self.course_name[j]=self.course_name[j].strip()
            j=j+1

        k=0
        for i in self.course_desc:
            self.course_desc[k]=self.course_desc[k].strip()
            k=k+1

        self.pat_1 = "[A-Z]+"
        self.pat_2 = "[0-9]+"

        for i in self.course_name:
            self.CC_List.append(re.findall(self.pat_1,i)[0]+" "+re.findall(self.pat_2,i)[0])
            if re.findall(self.pat_1,i)[0] not in self.GC_List:
                self.GC_List.append(re.findall(self.pat_1,i)[0])

        #Below course names are not proper for regular expression patter, they have both numbers and capitol letter. we add them manually.
        if "courses_ee.txt" in self.file_path:

            self.CC_List[4]="PHYS 103L"
            self.CC_List[6]="PHYS 104L"
            x=0
            while x<51:
                self.CD[self.CC_List[x]]=self.course_desc[x]

                x=x+1
        if "courses_cs.txt"in self.file_path:

            self.CC_List[3]="PHYS 103L"
            self.CC_List[5]="PHYS 104L"
            x=0
            while x<49:
                self.CD[self.CC_List[x]]=self.course_desc[x]
                x=x+1

        if "courses_ie.txt" in self.file_path:

            self.CC_List[3]="PHYS 103L"
            self.CC_List[5]="PHYS 104L"
            x=0
            while x<63:
                self.CD[self.CC_List[x]]=self.course_desc[x]
                x=x+1

        self.GC_List.sort() #for alphabetical order of courses

    def ListBoxFunc(self):

        self.listbox.delete(0, END)

        for courses in self.GC_List:
            self.listbox.insert(END,courses)

    def DataMatrix(self):
        #getting selected courses from listbox
        self.curselection=self.listbox.curselection()
        for i in self.curselection:
            self.selected_courses.append(self.GC_List[i])

        for item in self.selected_courses:
            for courses in self.CC_List:
                if re.findall(self.pat_1,item)[0] in courses:
                    self.selected_course_name.append(courses)

        #uploading course names and description into LastDict
        for items in self.selected_course_name:
            self.LastDict[items]=self.CD[items]

        clusters.create_matrix(self.LastDict,outfile="data.txt")

    def AddDataMatrix(self):

        self.DataMatrix()

        #creating canvas for data matrix
        self.maincanvas=Canvas(self.root,bg='#FFFFFF',width=100,height=320,)
        self.maincanvas.grid(row=8,rowspan=8,column=1,columnspan=16,pady=10,sticky="WE")
        self.xscrollbar = Scrollbar(self.root, orient=HORIZONTAL,command=self.maincanvas.xview)
        self.xscrollbar.grid(row=15,column=1,columnspan=16,sticky="WSE")

        self.yscrollbar = Scrollbar(self.root,orient=VERTICAL,command=self.maincanvas.yview)
        self.yscrollbar.grid(column=17,row=8,rowspan=8,sticky="WNS")

        self.maincanvas.config(xscrollcommand=self.xscrollbar,yscrollcommand=self.yscrollbar)
        self.datafile=open("data.txt","r")

        index=10
        for i in self.datafile:
            self.maincanvas.create_text(10,index,text=i,anchor="nw")
            index+=30

    def PrintClust(self):

        self.DataMatrix()
        #creating canvas for printing cluster
        self.maincanvas=Canvas(self.root,bg='#FFFFFF',width=100,height=320,)
        self.maincanvas.grid(row=8,rowspan=8,column=1,columnspan=16,pady=10,sticky="WE")
        self.xscrollbar = Scrollbar(self.root, orient=HORIZONTAL,command=self.maincanvas.xview)
        self.xscrollbar.grid(row=15,column=1,columnspan=16,sticky="WSE")

        self.yscrollbar = Scrollbar(self.root,orient=VERTICAL,command=self.maincanvas.yview)
        self.yscrollbar.grid(column=17,row=8,rowspan=8,sticky="WNS")

        self.maincanvas.config(xscrollcommand=self.xscrollbar,yscrollcommand=self.yscrollbar)

        courses, words, data = clusters.readfile("data.txt")
        #creating if condition for distance methods, tanimoto and pearson
        if str(self.var.get())=="1":

            clust=clusters.hcluster(data,distance=clusters.pearson)
            self.printclust=clusters.clust2str(clust, labels=courses)
            self.maincanvas.create_text(350,10,font="Helvetiva 10",text=self.printclust,anchor="nw")

        elif str(self.var.get())=="2":

            clust=clusters.hcluster(data,distance=clusters.tanimoto)
            self.printclust=clusters.clust2str(clust, labels=courses)
            self.maincanvas.create_text(350,10,font="Helvetiva 10",text=self.printclust,anchor="nw")
        else:

            tkMessageBox.showerror("ERROR","Please select distance method.")
            self.DataMatrix()

Main()
