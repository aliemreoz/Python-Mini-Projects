#modules that we used for this project
import urllib2
import urllib
from bs4 import BeautifulSoup
import re
from Tkinter import *
import ttk
from PIL import Image, ImageTk
import tkMessageBox

class Main():

    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE)
        self.root.title("SEHIR Research Projects Analyzer")

        self.GUI()

        self.root.mainloop()

    def Fetch(self): #command of fetch button, it checks the url.

        if self.entry.get()=="http://cs.sehir.edu.tr/en/research/":
            self.AddCombobox()
            self.AllDict()

        else:
            tkMessageBox.showerror("Unvalid Url", "Please provide a url that contains research project of SEHIR CS Faculty members.")

    def BeautifulSoup(self): #getting values from url using BeautifulSoup

        self.response = urllib2.urlopen("http://cs.sehir.edu.tr/en/research/")
        self.html_doc = self.response.read()
        self.soup=BeautifulSoup(self.html_doc, "html.parser")
        self.items=self.soup.find_all(class_="list-group-item")

        self.temp_names=[]
        self.temp_dates=[]
        self.temp_institution=[]
        self.temp_person=[]
        self.temp_info=[]

    #getting instructor names, years and institutions

        for a in self.items:
            self.temp_names.append(a.find("h4").text.strip())
            self.temp_dates.append(a.find_all("p")[0].text.strip())
            self.temp_institution.append(a.find_all("p")[1].text.strip())
            self.temp_person.append(a.find_all("p")[2].text.strip())
            self.temp_info.append(a.find_all("p")[4].text.strip())

    #getting images which they are used near the project descriptions
        i=1
        self.img_list=[]
        while i<16:
            self.img_list.append(str("cs.sehir.edu.tr"+self.soup.find_all('img')[i]["src"]))
            i=i+1

    def EditBS(self): #editing the values that got from BS

        self.BeautifulSoup()

        self.names=[]
        for i in self.temp_names:
            self.names.append(i.encode("utf-8"))


        self.temp_dates2=[]
        self.temp_dates3=[]
        self.dates=[]
        self.exact_dates=[]
        for i in self.temp_dates:
            self.temp_dates2.append(i.encode("utf-8")) #dates with special characters
        self.pat="[A-Za-z].+"
        for i in self.temp_dates2:
            for j in re.findall(self.pat,i):
                self.temp_dates3.append(j)  #to seperate dates without special characters
        for i in self.temp_dates3:
            if int(i[-4:]) not in self.dates:
                self.dates.append(int(i[-4:])) #last 4 chaarcters are years (without months)


        self.dates.sort()
        self.dates.insert(0,"All Years") #for ascending sort of years
        x=0
        y=1
        while x<len(self.temp_dates3):
            self.exact_dates.append(self.temp_dates3[x]+" - "+self.temp_dates3[y])
            x=x+2
            y=y+2 #years are sorted according to their starting and ending dates.To get starting year of other project it should follow +2


        self.institution=[]
        for i in self.temp_institution:
            self.institution.append(i[23:].encode("utf-8")) #institution names are written after 22 characters. First 22 character= Finding Institution



        self.person=[]
        for i in self.temp_person:
            self.person.append(i[32:].encode("utf-8")) #instructor names are written after 32 characters. First 32 characters=Principal Investigator



        self.info=[]
        for i in self.temp_info:
            self.info.append(i.encode("utf-8"))

        l=0
        for i in self.info: #for deleting special characters like \n
            fix_list=re.findall("\S+",self.info[l])
            fixed_str=""
            for i in fix_list:
                fixed_str=fixed_str+i+" "
            self.info.pop(l)
            self.info.insert(l,fixed_str)
            l=l+1

    def AddCombobox(self): #for adding values to comboboxes

        self.EditBS()

        self.eliminated_person=[]
        self.surname_person=[]
        self.person_surname=[]

        for i in self.person: #for creating person list that sorted by surname
            if i not in self.eliminated_person:
                self.eliminated_person.append(i)
        for i in self.eliminated_person:
            self.surname_person.append(i.split()[1]+" "+i.split()[0])
            self.surname_person.sort()
        for i in self.surname_person:
            self.person_surname.append(i.split()[1]+" "+i.split()[0])
        self.Ali_Cakmak=self.person_surname[6]
        self.person_surname.remove(self.Ali_Cakmak)
        self.person_surname.insert(4,self.Ali_Cakmak)
        self.person_surname.insert(0,"All Investigators")


        self.eliminated_institutions=[]
        for i in self.institution:
            if i not in self.eliminated_institutions:
                self.eliminated_institutions.append(i)
        self.eliminated_institutions.insert(0,"All Institutions")

        #to put values onto comboboxes
        self.combobox1["values"]=self.dates
        self.combobox2["values"]=self.person_surname
        self.combobox3["values"]=self.eliminated_institutions
        self.combobox1.set("All Years")
        self.combobox2.set("All Investigators")
        self.combobox3.set("All Institutions")

    def AllDict(self): #creating dictionaries for filtering

        self.year_dict={}
        self.person_dict={}
        self.institution_dict={}
        self.project_dict={}
        self.img_dict={}


        t=0
        while t<len(self.names):
            self.project_dict[self.names[t]]=self.info[t]
            t=t+1 #creating dictionary, keys are name of projects and values are descriptions of projects



        p=0
        while p<len(self.names):
            self.img_dict[self.names[p]]=self.img_list[p]
            p=p+1 #creating dictionary, keys are name of projects and values are images of projects


        c=0
        d=1
        e=0
        while c<len(self.temp_dates3):
            self.years=[]
            for i in range(int(self.temp_dates3[c][-4:]),int(self.temp_dates3[d][-4:])+1):
                self.years.append(i)
            self.year_dict[self.names[e]]=self.years
            c=c+2
            d=d+2
            e=e+1 #creating dictionary, keys are names of projects and values are years interval of projects



        a=0
        while a<len(self.person):
            self.person_dict[self.names[a]]=self.person[a]
            a=a+1 #creating dictionary, keys are names of projects and values are instructor who worked on relevant project



        b=0
        while b<len(self.institution):
            self.institution_dict[self.names[b]]=self.institution[b]
            b=b+1 #creating dictionary, keys are names of projects and values are institutions of project


    def Filter(self): #for filtering process which is based on user's prefer

        try:

            self.listbox.delete(0, END) #for cleaning listbox

            self.selected_year=self.combobox1.get()
            self.selected_person=self.combobox2.get().encode("utf-8")
            self.selected_institution=self.combobox3.get().encode("utf-8")

            self.selected_year_list=[]
            self.selected_person_list=[]
            self.selected_institution_list=[]
            self.main_filter=[]

            if self.selected_year=="All Years":
                self.selected_year_list=self.names

            else:
                for keys,values in self.year_dict.iteritems():

                    for i in values:
                        if i==int(self.selected_year):
                            self.selected_year_list.append(keys)

            if self.selected_person=="All Investigators":
                self.selected_person_list=self.names

            else:
                for keys, values in self.person_dict.iteritems():
                    if values ==self.selected_person:
                        self.selected_person_list.append(keys)

            if self.selected_institution=="All Institutions":
                self.selected_institution_list=self.names

            else:
                for keys, values in self.institution_dict.iteritems():
                    if values ==self.selected_institution:
                        self.selected_institution_list.append(keys)

            #finding intersection of multiple list
            self.intersection = list(set(self.selected_year_list)&set(self.selected_person_list) & set(self.selected_institution_list))

            for i in self.intersection:
                self.listbox.insert(END,i)

        except:

            tkMessageBox.showerror("Error!","Please fetch research projects first!")

    def Image(self): #creating image file based on user's selection

        #find from http://stackoverflow.com/questions/28195660/resize-url-image-using-urllib-and-pil
        self.image = urllib.urlretrieve("http://"+self.img_dict[self.selected_project], "aa.gif")
        self.opened_image = Image.open("aa.gif")
        self.width, self.height = self.opened_image.size
        self.new_width=int(float(self.width)*0.8)
        self.new_height=int(float(self.height)*0.8)
        self.new_image = self.opened_image.resize((self.new_width,self.new_height), Image.ANTIALIAS) #resize image
        self.project_image = ImageTk.PhotoImage(self.new_image)
        return self.project_image

    def Show(self): #for showing project descriptions and images in canvases


        try:

            self.selected_project=self.listbox.get(ACTIVE)
            self.selected_project_info = self.project_dict[self.selected_project]

            self.maincanvas2=Canvas(self.root,bg='#FFFFFF',width=120,height=240)
            self.maincanvas2.grid(row=11,rowspan=5,column=3,columnspan=2,sticky="WE")


            #for adding text in good visuality
            l=0
            h=10
            while l<len(self.selected_project_info):
                self.maincanvas2.create_text(10,h,font="Helvetiva 10",fill="blue",text=self.selected_project_info[l:l+55],anchor="nw")
                l=l+55
                h=h+16

            self.yscrollbar = Scrollbar(self.root,orient=VERTICAL,command=self.maincanvas2.yview)
            self.yscrollbar.grid(row=11,rowspan=5,column=4,sticky="NSWE")
            self.maincanvas2.config(yscrollcommand=self.yscrollbar)

            self.maincanvas = Canvas(bg='white',width=275,height=150)
            self.maincanvas.grid(row=11,rowspan=5,column=0,columnspan=3,sticky="NSWE")
            self.maincanvas.create_image(0, 0, image=self.Image(), anchor='nw')

        except:

            tkMessageBox.showerror("Error!","Please select project first!")

    def GUI(self):  #visual item of project,they are just for visualite


        self.label = Label(text = "SEHIR Research Projects Analyzer - CS Edition",bg = "blue", font = "Helvetica 17 bold", fg = "white",width=60)
        self.label.grid(row=0, column=0, columnspan=7, sticky = "WE")

        self.label2 = Label(text = "Please provide a url:",font = "Helvetica 12 bold", fg = "black")
        self.label2.grid(row= 1,column=0, sticky = "W",padx=10,pady=10)

        self.entryvalue=StringVar()
        self.entryvalue.set("http://cs.sehir.edu.tr/en/research/")
        self.entry=Entry(bg="yellow",textvariable=self.entryvalue)
        self.entry.grid(row=2,column=0,columnspan=3,sticky="WE",padx=10)

        self.button1=Button(text = "Fetch Research Projects", font = "Helvetica 10",command=self.Fetch)
        self.button1.grid(row=2,column=3,sticky="W",padx=20)

        self.label3=Label(text="."*400)
        self.label3.grid(row=3,column=0,columnspan=7,sticky="WE")

        ##############

        self.label4=Label(text="Filter Research Projects By",font = "Helvetica 13 bold")
        self.label4.grid(row=4,column=0,sticky="W",padx=10,pady=7)

        self.label5=Label(text="Pick a Project",font= "Helvetica 13 bold")
        self.label5.grid(row=4,column=2,sticky="W",padx=20,pady=7)

        self.label6=Label(text="Year:",font = "Helvetica 10",fg = "blue")
        self.label6.grid(row=5,column=0,sticky="W",padx=10,pady=7)

        self.label7=Label(text="Principal Investigator:",font = "Helvetica 10",fg = "blue")
        self.label7.grid(row=6,column=0,sticky="W",padx=10,pady=7)

        self.label8=Label(text="Funding Institution:",font = "Helvetica 10",fg = "blue")
        self.label8.grid(row=7,column=0,sticky="W",padx=10,pady=7)

        self.combobox1=ttk.Combobox(width=45)
        self.combobox1.grid(row=5,column=1,sticky="W",padx=10,pady=7)

        self.combobox2=ttk.Combobox(width=45)
        self.combobox2.grid(row=6,column=1,sticky="W",padx=10,pady=7)

        self.combobox3=ttk.Combobox(width=45)
        self.combobox3.grid(row=7,column=1,sticky="W",padx=10,pady=7)

        self.listbox=Listbox()
        self.listbox.grid(row=5,rowspan=3,column=2,columnspan=3,sticky="WE",pady=7)

        self.scroll=Scrollbar(command=self.listbox.yview,orient=VERTICAL)
        self.scroll.grid(row=5,rowspan=3,column=4,sticky="NSWE",pady=7)
        self.listbox.configure(yscrollcommand=self.scroll)

        self.button2=Button(text=" Display Project Titles ",font = "Helvetica 10",command=self.Filter)
        self.button2.grid(row=8,column=1,sticky="W",padx=10,pady=7)

        self.button3=Button(text="  Show Description  ",font = "Helvetica 10",command=self.Show)
        self.button3.grid(row=8,column=4,sticky="E",pady=7)

        self.label9=Label(text="."*400)
        self.label9.grid(row=9,column=0,columnspan=7,sticky="WE")

        ##################

        self.label10=Label(text="Project Description",font = "Helvetica 13 bold",fg = "black")
        self.label10.grid(row=10,column=4,sticky="W")

        self.maincanvas = Canvas(bg='white',width=275,height=150)
        self.maincanvas.grid(row=11,rowspan=5,column=0,columnspan=3,sticky="NSWE")

        self.maincanvas2=Canvas(self.root,bg='#FFFFFF',width=120,height=240)
        self.maincanvas2.grid(row=11,rowspan=5,column=3,columnspan=2,sticky="WE")

Main()
