from Tkinter import *
from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup
import urllib2
import xlrd
import docclass
import tkFileDialog
import tkMessageBox

#excel file must be in same file extension with project file

class Main():

    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE)
        self.root.title("Guess My Grade")
        self.root.grid()
        self.Course_Dict={}

        try:
            self.CS()
            self.IE()
            self.EE()
            self.Core_Course()
        except:
            tkMessageBox.showerror("Error","Check your connection.")
        self.Gather_All_Dict()

        self.GUI()
        self.root.mainloop()

    #visual item of project,they are just for visualite
    def GUI(self):
        self.label = Label(text = "Guess My Grade! v1.0",bg = "black", font = "Helvetica 25 bold", fg = "white",width=60)
        self.label.grid(row=0, column=0, columnspan=10, sticky = "WE")

        self.label2 = Label(text = "Please upload your curriculum file with the grades:",fg = "blue", font = "Helvetica 16")
        self.label2.grid(row=1, column=0, columnspan=4, sticky = "W",pady=10,padx=50)

        self.button=Button(text="Browse",bg="dark red",fg="white",font="Helvetica 14",command=self.EXCEL)
        self.button.grid(row=1,column=6,columnspan=2,stick="WE",pady=10)

        self.line_label=Label(text="-"*240)
        self.line_label.grid(row=2, column=0, columnspan=10, sticky = "WE")

        self.label3 = Label(text = "Enter urls for course descriptions",font = "Helvetica 16")
        self.label3.grid(row=3, column=0, columnspan=4, sticky = "W",padx=30)

        self.text=Text(height=6,bg="grey")
        self.text.grid(row=4,column=0,columnspan=6,sticky="WE",padx=30)
        links=["http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12","http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13",
               "http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14","http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32"]
        for i in links:
            self.text.insert(END,i)
            self.text.insert(END,"\n")
        self.label4=Label(text = "Key:",font = "Helvetica 16 bold")
        self.label4.grid(row=5, column=0,sticky = "W",padx=30,pady=10)

        self.labelA=Label(text="A",font="Helvetica 16 italic",bg="Dark Green",fg="white",width=6)
        self.labelA.grid(row=6, column=0,sticky = "WE",padx=30)

        self.labelB=Label(text="B",font="Helvetica 16 italic",bg="Light Green",fg="white",width=6)
        self.labelB.grid(row=6, column=1,sticky = "WE")

        self.labelC=Label(text="C",font="Helvetica 16 italic",bg="Orange",fg="white",width=6)
        self.labelC.grid(row=6, column=2,sticky = "WE",padx=30)

        self.labelD=Label(text="D",font="Helvetica 16 italic",bg="Red",fg="white",width=6)
        self.labelD.grid(row=6, column=3,sticky = "WE")

        self.labelF=Label(text="F",font="Helvetica 16 italic",bg="Black",fg="white",width=6)
        self.labelF.grid(row=6, column=4,sticky = "WE",padx=30)

        self.button2=Button(text="Predict Grades",bg="dark red",fg="white",font="Helvetica 14",command=self.Predict)
        self.button2.grid(row=6,column=6,columnspan=3,stick="WE")

        self.line_label2=Label(text="-"*240)
        self.line_label2.grid(row=7, column=0, columnspan=10, sticky = "WE")

        self.label5=Label(text = "Predicted Grades",font = "Helvetica 16 bold")
        self.label5.grid(row=8, column=0,columnspan=2,sticky = "W",padx=30,pady=10)

        self.text2=Text(height=10)
        self.text2.grid(row=9,column=0,columnspan=9,sticky="WE")

        self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
        self.scroll.grid(row=9,column=8,columnspan=2,sticky="NS")
        self.text2.configure(yscrollcommand=self.scroll)

    #getting all courses and course descriptions of CS Faculty with Selenium and Beautiful Soup
    def CS(self):
        driver = webdriver.Firefox()
        driver.get("http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=12")
        element=driver.find_element_by_link_text("Course Descriptions")
        element.click()
        time.sleep(5)
        source=driver.page_source
        driver.close()
        soup=BeautifulSoup(source,"html.parser")
        items=soup.find_all(class_="fakulte_ack")

        for i in items:
            a=i.find_all("strong")
        b=[]
        for i in a:
            b.append(i.text.strip().encode("utf-8"))
        pat="[A-Z]+"
        self.cs_course_codes=[]
        for i in b:
            try:
                if re.match(pat,i.split()[0])!=None:
                    self.cs_course_codes.append(i.split()[0]+" "+i.split()[1])
            except:IndexError

        for i in items:
            a=i.find_all("br")
        list=[]
        for i in a:
            list.append(i.next_sibling)
        self.cs_course_description=[]
        for i in list:
            if "NavigableString" in str(type(i)):
                self.cs_course_description.append(i.encode("utf-8"))

        a=0
        while a<60:
            for i in self.cs_course_description:
                if len(i)<97:
                    self.cs_course_description.remove(i)
            a=a+1
        ignored_list_for_cs=["ISBN","2nd","Press","ECTS","http:","Textbook:" ]
        for j in ignored_list_for_cs:
            for i in self.cs_course_description:
                if j in i:
                    self.cs_course_description.remove(i)

        l=0
        for i in self.cs_course_description:
            fix_list=re.findall("\S+",self.cs_course_description[l])
            fixed_str=""
            for i in fix_list:
                fixed_str=fixed_str+i+" "
            self.cs_course_description.pop(l)
            self.cs_course_description.insert(l,fixed_str)
            l=l+1

        self.cs_dict={}
        x=0
        while x<len(self.cs_course_description):
            self.cs_dict[self.cs_course_codes[x]]=self.cs_course_description[x]
            x=x+1
        self.cs_dict["ENGR 105"]=self.cs_dict["ENGR 106"]
        self.cs_dict.pop("ENGR 106")

    #getting all courses and course descriptions of IE Faculty with Selenium and Beautiful Soup
    def IE(self):
        driver = webdriver.Firefox()
        driver.get("http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=14")

        element=driver.find_element_by_link_text("Course Descriptions")
        element.click()
        time.sleep(1)
        source=driver.page_source


        driver.close()
        soup=BeautifulSoup(source,"html.parser")
        items=soup.find_all(class_="fakulte_ack")

        for i in items:
            cc=i.find_all("strong")
        b=[]
        for i in cc:
            b.append(i.text.strip().encode("utf-8"))
        pat="[A-Z]+"
        self.ie_course_codes=[]
        for i in b:
            try:
                if re.match(pat,i.split()[0])!=None:
                    self.ie_course_codes.append(i.split()[0]+" "+i.split()[1])
            except:IndexError
        self.ie_course_codes.pop(0)
        self.ie_course_codes.pop(27)
        self.ie_elective_courses=self.ie_course_codes[27:]

        for i in items:
            a=i.find_all("br")
        list=[]
        for i in a:
            list.append(i.next_sibling)
        self.ie_course_description=[]
        for i in list:
            if "NavigableString" in str(type(i)):
                self.ie_course_description.append(i.encode("utf-8"))


        ignored_list_for_ie=["ISBN","2nd","Press","ECTS","http:","Textbook:","ISE","Textbook :","ELECTIVE","461","521","Bierman","434","463","471","494","493" ]
        for j in ignored_list_for_ie:
            for i in self.ie_course_description:
                if j in i:
                    self.ie_course_description.remove(i)

        l=0
        for i in self.ie_course_description:
            fix_list=re.findall("\S+",self.ie_course_description[l])
            fixed_str=""
            for i in fix_list:
                fixed_str=fixed_str+i+" "
            self.ie_course_description.pop(l)
            self.ie_course_description.insert(l,fixed_str)
            l=l+1
        self.ie_course_description.pop(10)
        self.ie_course_description.pop(39)




        self.ie_dict={}

        x=0
        while x<len(self.ie_course_description):
            self.ie_dict[self.ie_course_codes[x]]=self.ie_course_description[x]
            x=x+1
        self.ie_dict["ENGR 105"]=self.ie_dict["ENGR 106"]
        self.ie_dict.pop("ENGR 106")

    #getting all courses and course descriptions of EE Faculty with Selenium and Beautiful Soup
    def EE(self):
        driver = webdriver.Firefox()
        driver.get("http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=13")

        element=driver.find_element_by_link_text("Course Descriptions")
        element.click()
        time.sleep(1)
        source=driver.page_source

        driver.close()
        soup=BeautifulSoup(source,"html.parser")
        list=[]
        self.ee_dict={}
        for i in soup.find_all("div",style="font-family:helvetica;font-size:9pt;color:rgb(0, 0, 0)"):
            list.append(i.text.strip().encode("utf-8"))
        a=0
        while a<50:
            for i in list:
                if "Textbook" in i:
                    list.remove(i)
            a=a+1

        for i in list:
            if "EECS" in i:
                list.remove(i)
        for i in list:
            if "EE 302" in i:
                EE_302=list[list.index(i)+1]+" "+list[list.index(i)+2]

        for i in list:
            if "EE" in i:
                EE_course_name=i.split()[0]+" "+i.split()[1]
                self.ee_dict[EE_course_name]=list[list.index(i)+1]

        self.ee_dict["EE 302"]=EE_302
        self.ee_dict["EECS 241"]="Description: This course covers fundamental concepts of Mathematics: definitions, proofs, sets, functions, relations. " \
                                 "Discrete structures: modular arithmetic, graphs, state machines, counting. Sampling distributions, central limit " \
                                 "theorem. Point and interval estimation."
        for i,j in self.ee_dict.items():

            fix_list=re.findall("\S+",j)
            fixed_str=""
            for f in fix_list:
                fixed_str=fixed_str+f+" "
            j=fixed_str[13:]
            self.ee_dict[i]=j

    #getting all courses and course descriptions of Core Electives with Beautiful Soup
    def Core_Course(self):
        response=urllib2.urlopen("http://www.sehir.edu.tr/en/Pages/Academic/Bolum.aspx?BID=32")
        html_doc = response.read()
        soup=BeautifulSoup(html_doc,"html.parser")
        items=soup.find_all("p")

        b=[]
        for i in items:
            b.append(i.text.strip().encode("utf-8"))
        list=[]
        pat2="[0-9]+"
        core_course_codes=[]
        for i in b:
            list.append(re.findall(pat2,i))

        c=0
        while c<50:
            for item in list:
                if len(item)<1:
                    list.remove(item)
            c=c+1
        for item in list:
                if len(item[0])<3:
                    list.remove(item)
        turkish=list.pop(-1)
        for i in range(4):
            turkish.pop(-1)

        first=[]
        second=[]
        for item in list:
            first.append("UNI "+item[0])
            if len(item[1])>2:
                second.append("UNI "+item[1])
            else:
                second.append("None")
        a=0
        while a<50:
            for i in b:
                if len(i)<400:
                    b.remove(i)
            a=a+1
        l=0
        for i in b:
            fix_list=re.findall("\S+",b[l])
            fixed_str=""
            for i in fix_list:
                fixed_str=fixed_str+i+" "
            b.pop(l)
            b.insert(l,fixed_str)
            l=l+1


        turkish_desc=b.pop(-1)

        self.core_course_dict={}
        p=0
        while p<len(b):
            self.core_course_dict[first[p]]=b[p]
            if second[p]!="None":
                self.core_course_dict[second[p]]=b[p]
            p=p+1

        r=0
        while r<len(turkish):
            self.core_course_dict["UNI "+turkish[r]]=turkish_desc
            r=r+1

    #creating a general dictionary for all courses {key=Course Code:value=Description}
    def Gather_All_Dict(self):

        for i,j in self.cs_dict.items():
            if i not in self.Course_Dict:
                self.Course_Dict[i]=self.cs_dict[i]
        for i,j in self.ee_dict.items():
            if i not in self.Course_Dict:
                self.Course_Dict[i]=self.ee_dict[i]
        for i,j in self.ie_dict.items():
            if i not in self.Course_Dict:
                self.Course_Dict[i]=self.ie_dict[i]
        for i,j in self.core_course_dict.items():
            if i not in self.Course_Dict:
                self.Course_Dict[i]=self.core_course_dict[i]

    #getting course names and grades if exists from excel for IE
    def IE_EXCEL(self):

        list=[]
        list2=[]
        list3=[]
        list4=[]
        excelfile="ie.xlsx"
        book = xlrd.open_workbook(excelfile)
        sheet = book.sheet_by_index(0)

        #first two numbers represents rows and third number represents column
        courses = {"Semester 1":(6,12,0),"Semester 2":(6,14,9),"Semester 3":(18,23,0),"Semester 4":(18,25,9),"Semester 5":(29,34,0),"Semester 6":(29,36,9), "Semester 7": (40,45,0),"Semester 8":(40,45,9)}
        self.ie_semester={}
        for key,row_column in courses.iteritems():
            c=[]
            for row_index in range(row_column[0], row_column[1]+1):
                course_info="%s" % (sheet.cell(row_index,row_column[2]).value.encode("utf-8"))
                c.append(course_info)
            self.ie_semester[key] = c
        a=0
        while a<50:
            for i,j in self.ie_semester.items():
                for k in j:
                    if k not in self.ie_course_codes:
                        j.remove(k)
            a=a+1


        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+6).value.encode('utf-8')
                list.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column).value.encode('utf-8')
                list2.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+15).value.encode('utf-8')
                list3.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+9).value.encode('utf-8')
                list4.append(a)

        self.ie_graded_course={}
        for i in range(len(list)):
            self.ie_graded_course[list2[i]]=list[i]
        for i in range(len(list3)):
            self.ie_graded_course[list4[i]]=list3[i]

        for i,j in self.ie_graded_course.items():
            if j=="":
                self.ie_graded_course.pop(i)
            if i=="Code":
                self.ie_graded_course.pop(i)
        for i,j in self.ie_graded_course.items():
            self.ie_graded_course[i]=j[0]

        semestercourses=[]
        for i in self.ie_semester.values():
            for j in i:
                if j not in semestercourses:
                    semestercourses.append(j)
        self.ungradedlist_ie=[]

        for j in semestercourses:
            if j not in self.ie_graded_course.keys():
                self.ungradedlist_ie.append(j)

    #getting course names,departmental electives and grades if exists from excel for CS
    def CS_EXCEL(self):
        list=[]
        list2=[]
        list3=[]
        list4=[]
        excelfile="cs.xlsx"
        book = xlrd.open_workbook(excelfile)
        sheet = book.sheet_by_index(0)

        #first two numbers represents rows and third number represents column
        courses = {"Semester 1":(6,12,0),"Semester 2":(6,14,9),"Semester 3":(18,23,0),"Semester 4":(18,25,9),"Semester 5":(29,34,0),"Semester 6":(29,36,9), "Semester 7": (41,45,0),"Semester 8":(41,45,9)}
        self.cs_semester={}
        for key,row_column in courses.iteritems():
            c=[]
            for row_index in range(row_column[0], row_column[1]+1):
                course_info="%s" % (sheet.cell(row_index,row_column[2]).value.encode("utf-8"))
                c.append(course_info)
            self.cs_semester[key] = c
        a=0
        while a<50:
            for i,j in self.cs_semester.items():
                for k in j:
                    if k not in self.cs_course_codes:
                        j.remove(k)
            a=a+1


        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+6).value.encode('utf-8')
                list.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column).value.encode('utf-8')
                list2.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+15).value.encode('utf-8')
                list3.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+9).value.encode('utf-8')
                list4.append(a)

        self.cs_graded_course={}
        for i in range(len(list)):
            self.cs_graded_course[list2[i]]=list[i]
        for i in range(len(list3)):
            self.cs_graded_course[list4[i]]=list3[i]

        for i,j in self.cs_graded_course.items():
            if j=="":
                self.cs_graded_course.pop(i)
            if i=="Code":
                self.cs_graded_course.pop(i)
        for i,j in self.cs_graded_course.items():
            self.cs_graded_course[i]=j[0]

        semestercourses=[]
        for i in  self.cs_semester.values():
            for j in i:
                if j not in semestercourses:
                    semestercourses.append(j)
        self.ungradedlist_cs=[]

        for j in semestercourses:
            if j not in self.cs_graded_course.keys():
                self.ungradedlist_cs.append(j)

        ###############

        courses = {"Computer System":(59,69,0),"Devices":(59,66,9),
                   "EE Systems":(73,76,0),"Theory and Algorithms":(73,82,9),
                   "Other":(85,85,0)}
        self.EECS={}
        for key,row_column in courses.iteritems():
            c=[]
            for row_index in range(row_column[0], row_column[1]+1):
                course_info="%s" % (sheet.cell(row_index,row_column[2]).value.encode("utf-8"))
                c.append(course_info)
            self.EECS[key] = c
        a=0
        while a<50:
            for i,j in self.EECS.items():
                for k in j:
                    if k not in self.cs_course_codes:
                        j.remove(k)
            a=a+1

    #getting course names,departmental electives and grades if exists from excel for EE
    def EE_EXCEL(self):
        list=[]
        list2=[]
        list3=[]
        list4=[]
        excelfile="ee.xlsx"
        book = xlrd.open_workbook(excelfile)
        sheet = book.sheet_by_index(0)

        #first two numbers represents rows and third number represents column
        courses = {"Semester 1":(6,12,0),"Semester 2":(6,14,9),"Semester 3":(18,23,0),"Semester 4":(18,25,9),"Semester 5":(29,34,0),"Semester 6":(29,36,9), "Semester 7": (40,44,0),"Semester 8":(40,44,9)}
        self.ee_semester={}
        for key,row_column in courses.iteritems():
            c=[]
            for row_index in range(row_column[0], row_column[1]+1):
                course_info="%s" % (sheet.cell(row_index,row_column[2]).value.encode("utf-8"))
                c.append(course_info)
            self.ee_semester[key] = c


        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+6).value.encode('utf-8')
                list.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column).value.encode('utf-8')
                list2.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+15).value.encode('utf-8')
                list3.append(a)

        for column in range(1):    #meals are gathered in only one column
            for row in range(46):       #and 67 rows
                a=sheet.cell(row+6,column+9).value.encode('utf-8')
                list4.append(a)

        self.ee_graded_course={}
        for i in range(len(list)):
            self.ee_graded_course[list2[i]]=list[i]
        for i in range(len(list3)):
            self.ee_graded_course[list4[i]]=list3[i]

        for i,j in self.ee_graded_course.items():
            if j=="":
                self.ee_graded_course.pop(i)
            if i=="Code":
                self.ee_graded_course.pop(i)
        for i,j in self.ee_graded_course.items():
            self.ee_graded_course[i]=j[0]

        semestercourses=[]
        for i in self.ee_semester.values():
            for j in i:
                if j not in semestercourses:
                    semestercourses.append(j)

        self.ungradedlist_ee=[]
        for j in semestercourses:
            if j not in self.ee_graded_course.keys():
                self.ungradedlist_ee.append(j)
        a=0
        while a<50:
            for i in self.ungradedlist_ee:
                if i=="":
                    self.ungradedlist_ee.remove(i)
                if i=="UNI xxx":
                    self.ungradedlist_ee.remove(i)
                if i=="xxx":
                    self.ungradedlist_ee.remove(i)
                if i=="EECS xxx":
                    self.ungradedlist_ee.remove(i)
            a=a+1

        self.EECS={}
        for key,row_column in courses.iteritems():
            c=[]
            for row_index in range(row_column[0], row_column[1]+1):
                course_info="%s" % (sheet.cell(row_index,row_column[2]).value.encode("utf-8"))
                c.append(course_info)
            self.EECS[key] = c
        a=0
        while a<50:
            for i,j in self.EECS.items():
                for k in j:
                    if k not in self.cs_course_codes:
                        j.remove(k)
            a=a+1

    #deciding which excel file will be used based on user's choice with FileDialog
    def EXCEL(self):
        self.excelfile = tkFileDialog.askopenfilename()
        if "xlsx" in self.excelfile:
            if "cs" in self.excelfile:
                self.CS_EXCEL()
            elif "ie" in self.excelfile:
                self.IE_EXCEL()
            elif "ee" in self.excelfile:
                self.EE_EXCEL()
            else:
                tkMessageBox.showerror("Error","Please upload a proper excel file")
        else:
            tkMessageBox.showerror("Error","Please upload an excel file")

    #train course description if course has grades.
    def MakeTrain(self):
        self.cl=docclass.naivebayes(docclass.getwords)
        if "cs" in self.excelfile:
            try:
                for i,j in self.cs_graded_course.items():
                    self.cl.train(self.Course_Dict[i],j)
            except:
                KeyError

        elif "ie" in self.excelfile:
             try:
                for i,j in self.ie_graded_course.items():
                    self.cl.train(self.Course_Dict[i],j)
             except:
                 KeyError

        elif "ee" in self.excelfile:
            try:
                for i,j in self.ee_graded_course.items():
                    self.cl.train(self.Course_Dict[i],j)
            except:
                KeyError

    #for painting prediction which belongs A
    def MakeColorForA(self):
        start=1.0
        while True:
            tag_start = self.text2.search(">A", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(">A"))
            self.text2.tag_add("dark green",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("dark green", background="dark green",foreground="white")
            start = tag_start + "+1c"

    #for painting prediction which belongs B
    def MakeColorForB(self):
        start=1.0
        while True:
            tag_start = self.text2.search(">B", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(">B"))
            self.text2.tag_add("light green",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("light green", background="light green")
            start = tag_start + "+1c"

    #for painting prediction which belongs C
    def MakeColorForC(self):
        start=1.0
        while True:
            tag_start = self.text2.search(">C", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(">C"))
            self.text2.tag_add("orange",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("orange", background="orange")
            start = tag_start + "+1c"

    #for painting prediction which belongs D
    def MakeColorForD(self):
        start=1.0
        while True:
            tag_start = self.text2.search(">D", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(">D"))
            self.text2.tag_add("red",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("red", background="red",foreground="white")
            start = tag_start + "+1c"

    #for painting prediction which belongs F
    def MakeColorForF(self):
        start=1.0
        while True:
            tag_start = self.text2.search(">F", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(">F"))
            self.text2.tag_add("black",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("black", background="black",foreground="white")
            start = tag_start + "+1c"

    #for underline title
    def MakeUnderlined(self):
        start=1.0
        while True:
            tag_start = self.text2.search("Semester", start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len("Semester")+2)
            self.text2.tag_add("underline",str(int(float(tag_start)))+".0",tag_end)
            self.text2.tag_config("underline", underline=True)
            start = tag_start + "+1c"

    #for underline title
    def MakeUnderlined2(self,word):
        start=1.0
        tag_start = self.text2.search(word, start, stopindex=END)
        tag_end = '%s+%dc' % (tag_start, len(word))
        self.text2.tag_add("underline",str(int(float(tag_start)))+".0",tag_end)
        self.text2.tag_config("underline", underline=True)

    #make a prediction based on past grades and write them in texrbox
    def Predict(self):
        self.text2=Text(height=10,font="Helvetica 15")
        self.text2.grid(row=9,column=0,columnspan=9,sticky="WE")
        self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
        self.scroll.grid(row=9,column=8,columnspan=2,sticky="NS")
        self.text2.configure(yscrollcommand=self.scroll)

        self.MakeTrain()
        if "cs" in self.excelfile:
            for i in self.ungradedlist_cs:
                if i in self.Course_Dict:
                    if i not in self.core_course_dict:

                        #showing semester number
                        for name,values in self.cs_semester.items():
                            for item in values:
                                if i==item:
                                    searched_val=values
                                    if self.cs_semester[name] == searched_val:
                                        if name not in self.text2.get("1.0",END).encode("utf-8"):
                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,name)

                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,"\n")

                                        #showing prediction for semester courses
                                        self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                                        self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"Departmental Electives")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            #showing prediction for departmental electives
            for i in self.EECS.values():
                for j in i:
                    self.text2.insert(END,j+"-->"+self.cl.classify(self.Course_Dict[j]))
                    self.text2.insert(END,"\n")

            self.ungraded_core=[]
            for i in self.core_course_dict.keys():
                if i not in self.cs_graded_course:
                    self.ungraded_core.append(i)

            self.text2.insert(END,"\n")
            self.text2.insert(END,"UNI COURSES")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            #showing prediction for uni courses
            for i in self.ungraded_core:
                self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                self.text2.insert(END,"\n")

        if "ie" in self.excelfile:
            for i in self.ungradedlist_ie:
                if i in self.Course_Dict:
                    if i not in self.core_course_dict:
                        for name,values in self.ie_semester.items():
                            for item in values:
                                if i==item:
                                    searched_val=values
                                    if self.ie_semester[name] == searched_val:
                                        if name not in self.text2.get("1.0",END).encode("utf-8"):
                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,name)

                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,"\n")
                                        self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                                        self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"Departmental Electives")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            for i in self.ie_elective_courses:
                self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                self.text2.insert(END,"\n")

            self.ungraded_core=[]
            for i in self.core_course_dict.keys():
                if i not in self.ie_graded_course:
                    self.ungraded_core.append(i)

            self.text2.insert(END,"\n")
            self.text2.insert(END,"UNI COURSES")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            for i in self.ungraded_core:
                self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                self.text2.insert(END,"\n")

        if "ee" in self.excelfile:
            for i in self.ungradedlist_ee:
                if i in self.Course_Dict:
                    if i not in self.core_course_dict:
                        for name,values in self.ee_semester.items():
                            for item in values:
                                if i==item:
                                    searched_val=values
                                    if self.ee_semester[name] == searched_val:
                                        if name not in self.text2.get("1.0",END).encode("utf-8"):
                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,name)

                                            self.text2.insert(END,"\n")
                                            self.text2.insert(END,"\n")
                                        self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                                        self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"Departmental Electives")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            for i in self.EECS.values():
                for j in i:
                    self.text2.insert(END,j+"-->"+self.cl.classify(self.Course_Dict[j]))
                    self.text2.insert(END,"\n")

            self.ungraded_core=[]
            for i in self.core_course_dict.keys():
                if i not in self.ee_graded_course:
                    self.ungraded_core.append(i)

            self.text2.insert(END,"\n")
            self.text2.insert(END,"UNI COURSES")
            self.text2.insert(END,"\n")
            self.text2.insert(END,"\n")
            for i in self.ungraded_core:
                self.text2.insert(END,i+"-->"+self.cl.classify(self.Course_Dict[i]))
                self.text2.insert(END,"\n")

        #painting prediction
        self.MakeColorForA()
        self.MakeColorForB()
        self.MakeColorForC()
        self.MakeColorForD()
        self.MakeColorForF()

        #underlining titles
        self.MakeUnderlined()
        self.MakeUnderlined2("UNI COURSES")
        self.MakeUnderlined2("Departmental Electives")

Main()