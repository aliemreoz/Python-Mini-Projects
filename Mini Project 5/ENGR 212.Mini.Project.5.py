import urllib2
from bs4 import BeautifulSoup
import re
from Tkinter import *
import tkMessageBox
import shelve
from django.utils.encoding import smart_str
from collections import defaultdict
import time

class Main():


    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE)
        self.root.title("Sehir Scholar")
        self.root.grid()
        self.root.configure(bg='white')
        self.root.option_add("*background", "white")

        self.GUI()

        #creating database that we use
        self.wordlocation = shelve.open("wordlocation.db", writeback=True, flag='c')
        self.citation_count = shelve.open("citation_count.db", writeback=True, flag='c')
        self.group_by_pub = shelve.open("group_by_pub.db", writeback=True, flag='c')

        self.main_dict={}
        self.members=[]
        self.links=[]
        self.member_links={}

        #it will sort alphabetically publication types on listbox
        self.sorted_type=[]
        self.sorted_type=self.group_by_pub.keys()
        self.sorted_type.sort()
        for type in self.sorted_type:
            self.listbox.insert(END,type)
        self.listbox.selection_set(0,END)

        self.root.mainloop()

    #visual item of project,they are just for visualite
    def GUI(self):

        self.label = Label(text = "SEHIR Scholar",bg = "blue", font = "Helvetica 25 bold", fg = "white",width=60)
        self.label.grid(row=0, column=0, columnspan=15, sticky = "WE")

        self.label2=Label(text='Url for faculty list:', font='Helvetica 11')
        self.label2.grid(row=1, column=4, columnspan=1, sticky='W',pady=5)

        self.entryvalue=StringVar()
        self.entryvalue.set("http://cs.sehir.edu.tr/en/people/")
        self.entry=Entry(textvariable=self.entryvalue,font=12)
        self.entry.grid(row=1,column=5,columnspan=4,sticky="WE",pady=5)

        self.button=Button(text='Build Index',font=12,command=self.build_index)
        self.button.grid(row=1, column=10, sticky='E', pady=5)

        #########

        self.entryvalue2=StringVar()
        self.entry2=Entry(font='Arial 16')
        self.entry2.grid(row=2, column=3, columnspan=8, sticky='WE',pady=10)

        ########

        self.label3=Label(text='Ranking Criteria', font='Helvetica 13 bold')
        self.label3.grid(row=3, column=5,sticky='W', pady=5)

        self.label4=Label(text='Weight', font='Helvetica 13 bold')
        self.label4.grid(row=3, column=6, sticky='W', pady=5)

        self.label5=Label(text='Filter Papers', font='Helvetica 13 bold')
        self.label5.grid(row=3, column=7, sticky='WE', pady=5)

        ########
        self.var=IntVar()
        self.var2=IntVar()
        self.checkbutton=Checkbutton(text='Word Frequency', font='Helvetica 13',variable=self.var)
        self.checkbutton.grid(row=4, column=5, sticky='W')

        self.checkbutton2=Checkbutton(text='Citation Count', font='Helvetica 13',variable=self.var2)
        self.checkbutton2.grid(row=5, column=5, sticky='W')

        self.entryvalue3=IntVar()
        self.entryvalue3.set(1)
        self.entry3=Entry(textvariable=self.entryvalue3, font='Helvetica 12', width=3)
        self.entry3.grid(row=4,column=6, sticky='W',padx=15)

        self.entryvalue4=IntVar()
        self.entryvalue4.set(1)
        self.entry4=Entry(textvariable=self.entryvalue4, font='Helvetica 12', width=3)
        self.entry4.grid(row=5,column=6, sticky='W',padx=15)

        self.listbox=Listbox(height=5,width=40,selectmode=MULTIPLE)
        self.listbox.grid(row=4, column=7,rowspan=2)

        self.button2=Button(text="Search",font=12,command=self.Search)
        self.button2.grid(row=4,column=8,sticky="E")

        self.text=Text(height=20)
        self.text.grid(row=7,column=3,columnspan=8,sticky="WE",pady=10)
        self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
        self.scroll.grid(row=7,column=11,sticky="NS")
        self.text.configure(yscrollcommand=self.scroll)

        self.button3=Button(text="Next",font=12,command=self.Next)
        self.button3.grid(column=10,row=8)

        self.label7=Label(bg="blue",fg="white",text="1", font='Helvetica 14', width=2)
        self.label7.grid(column=9,row=8)

        self.button4=Button(text="Previous",font=12,command=self.Previous)
        self.button4.grid(column=8,row=8)

        self.label8=Label(text="Page:",font="Helvetica 12 bold")
        self.label8.grid(row=8,column=7,sticky="E")

    #to seperate the keywords which we write on search box
    def separatewords(self,text):

        self.splitter = re.compile('\\W*')
        return [s.lower() for s in self.splitter.split(text) if s != '']

    #format of wordlocation dictionary becomes {keywords:{title of publication:[location of keyword1, location of keyword2, ..]}}
    def addtoindex(self,title):

        text = title
        words = self.separatewords(text)
        for i in range(len(words)):
            word = smart_str(words[i])
            self.wordlocation.setdefault(word, {})
            self.wordlocation[word].setdefault(title, [])
            self.wordlocation[word][title].append(i)

    #getting related links from http://cs.sehir.edu.tr/en/people/ with beautiful soup
    def get_links(self):

            self.response = urllib2.urlopen("http://cs.sehir.edu.tr/en/people/")
            self.html_doc = self.response.read()
            self.soup=BeautifulSoup(self.html_doc, "html.parser")
            self.items=self.soup.find_all(class_="member")

            for a in self.items: #to find instructors we use h4 tag, then we strip them
                self.members.append(a.find("h4").text.strip().encode("utf-8"))

            #for deleting special characters like \n
            l=0
            for i in self.members:
                fix_list=re.findall("\S+",self.members[l])
                fixed_str=""
                for i in fix_list:
                    fixed_str=fixed_str+i+" "
                self.members.pop(l)
                self.members.insert(l,fixed_str[0:-1])
                l=l+1

            #to get links of instructors
            for a in self.items:
                self.links.append("http://cs.sehir.edu.tr"+a.find_all("a")[0]["href"].encode("utf-8"))

            #creating a dictionary keys are names of instructors and values are their links {instructor1:link of instructor 1, instructor2:link of instructor2,...}
            t=0
            while t<len(self.members):
                self.member_links[self.members[t]]=self.links[t]
                t=t+1

    def build_index(self): #command of build index button, it checks the url

        self.get_links()

        for name,link in self.member_links.items():
            self.response2 = urllib2.urlopen(link)
            self.html_doc2 = self.response2.read()
            self.soup2=BeautifulSoup(self.html_doc2, "html.parser")
            self.items2=self.soup2.find_all(class_="tab-pane",id="publication") #getting items in tab-pane class with using beautiful soup

            self.publication_type=[]

            for i in self.items2:
                for a in i.find_all("p"): #tag p includes types of publications like book chapters, patents, journal papers
                    self.publication_type.append(a.text.strip().encode("utf-8")) #we gather publication types in one list

                self.Last_Pub_Index=int(i.find_all("li")[-1].text.strip().encode("utf-8").splitlines()[0][0:-2]) #tag li includes names of publications


            self.pub_list=[] #putting all names of publications in one list]
            l=0
            while l<self.Last_Pub_Index:
                for i in self.items2:
                    fixed_str=""
                    fix_list=re.findall("\S+",i.find_all("li")[l].text.strip().encode("utf-8")) #to separate special characters
                    fix_list.pop(0)
                    for i in fix_list:
                        fixed_str=fixed_str+i+" "
                    self.pub_list.append(fixed_str)
                l=l+1

            b=0
            while b<len(self.publication_type): #to find index of starting of different publication types
                try:
                    for i in self.items2:
                        self.seconds_index=int(i.find_all("ul")[1]("li")[0].text.strip().encode("utf-8").splitlines()[0][0:-2])-1
                        self.thirds_index=int(i.find_all("ul")[2]("li")[0].text.strip().encode("utf-8").splitlines()[0][0:-2])-1
                        self.fourth_index=int(i.find_all("ul")[3]("li")[0].text.strip().encode("utf-8").splitlines()[0][0:-2])-1
                except:ValueError
                b=b+1

            self.publications={} #to create dictionaries based on publication type, there are maximum 4 different types for all instructor
            if len(self.publication_type)==2:
                self.publications[self.publication_type[0]]=self.pub_list[0:self.seconds_index]
                self.publications[self.publication_type[1]]=self.pub_list[self.seconds_index:self.Last_Pub_Index]

            elif len(self.publication_type)==3:
                self.publications[self.publication_type[0]]=self.pub_list[0:self.seconds_index]
                self.publications[self.publication_type[1]]=self.pub_list[self.seconds_index:self.thirds_index]
                self.publications[self.publication_type[2]]=self.pub_list[self.thirds_index:self.Last_Pub_Index]

            elif len(self.publication_type)==4:
                self.publications[self.publication_type[0]]=self.pub_list[0:self.seconds_index]
                self.publications[self.publication_type[1]]=self.pub_list[self.seconds_index:self.thirds_index]
                self.publications[self.publication_type[2]]=self.pub_list[self.thirds_index:self.fourth_index]
                self.publications[self.publication_type[3]]=self.pub_list[self.fourth_index:self.Last_Pub_Index]

            self.main_dict[name]=self.publications

            #creating database based on wordlocation(1) and citation count(2)
            for pub in self.pub_list:
                self.addtoindex(pub)#(1)
                if "Citation" in pub: #(2)
                    m=0
                    while m<len(pub):
                        if pub[m]=="[": #since ciatation count is written after "[" sign, we use "[" and " " to get citation numbers ( such as: name of publication [82 Citation] )
                            if pub[m+2]==" ":
                                self.citation_count[pub]=int(pub[m+1])
                            elif pub[m+3]==" ":
                                self.citation_count[pub]=int(pub[m+1]+pub[m+2])
                            elif pub[m+4]==" ":
                                self.citation_count[pub]=int(pub[m+1]+pub[m+2]+pub[m+3])
                        m=m+1
                else:
                    self.citation_count[pub]=0

        #creating database based on publication type
        #get help from http://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key
        self.dd = defaultdict(list)
        for i,j in self.main_dict.items():
           for key, value in j.iteritems():
                self.dd[key].append(value)

        for i,j in self.dd.items():
            self.group_by_pub[i]=j #group_by_pub dict= {type1 of publications: names of publications which belong type1, type2: names of publications which belong type2,...}

        self.listbox=Listbox(height=5,width=40,selectmode=MULTIPLE) #selectmode is to select multiple categories of papers
        self.listbox.grid(row=4, column=7,rowspan=2)
        self.sorted_type=[]  #it will sort alphabetically categories of papers on listbox
        self.sorted_type=self.group_by_pub.keys()
        self.sorted_type.sort()
        for type in self.sorted_type:
            self.listbox.insert(END,type)
        self.listbox.selection_set(0,END)

        self.wordlocation.close()
        self.citation_count.close()
        self.group_by_pub.close()

    #end of building index
    ##################################################################################################################
    #start of searching

    #to normalize scores
    def normalizescores(self,scores,smallIsBetter=0):

        vsmall = 0.00001
        if smallIsBetter:
            minscore=min(scores.values())
            minscore=max(minscore, vsmall)
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \

                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    #adapting getmatchingpages function from mysearchengine
    def getmatchingpages(self,q):

        results = {}
        words = [smart_str(word) for word in q.split()]
        if words[0] not in self.wordlocation:
                return results, words
        pub_set = set(self.wordlocation[words[0]].keys())
        for word in words[1:]:
            if word not in self.wordlocation:
                return results, words
            pub_set = pub_set.intersection(self.wordlocation[word].keys())
        for pub in pub_set:
            results[pub] = []
            for word in words:
                results[pub].append(self.wordlocation[word][pub])
        return results, words

    #for finding word frequency score, after that we normalize it
    def frequencyscore(self,results):

        counts = {}
        for pub in results:
            score = 1
            for wordlocations in results[pub]:
                score *= len(wordlocations)
            counts[pub] = score
        return self.normalizescores(counts, smallIsBetter=False)

    #for finding citation score, after that we normalize it
    def citationscore(self,results):

        citation_score={}
        for pub in results.keys():

            if pub in self.citation_count.keys():
                citation_score[pub]=self.citation_count[pub]
        return self.normalizescores(citation_score,smallIsBetter=False)

    #deciding which ranking measure will be used and based on selection create scores
    def getscoredlist(self,results, words):

        weight1=float(int(self.entry3.get()))
        weight2=float(int(self.entry4.get()))

        #if both word frequency and citation count are selected
        if self.var.get()==1 and self.var2.get()==1:
            self.totalscores = dict([(pub, 0) for pub in results])
            weights = [(weight1, self.frequencyscore(results)),(weight2, self.citationscore(results))]
            for (weight,scores) in weights:
                for pub in self.totalscores:
                    self.totalscores[pub] += weight*scores.get(pub, 0)
            return self.normalizescores(self.totalscores)

        #if only word frequency is selected
        elif self.var.get()==1 and self.var2.get()==0:
            self.totalscores = dict([(pub, 0) for pub in results])
            weights = [(weight1, self.frequencyscore(results)),(0, self.citationscore(results))]
            for (weight,scores) in weights:
                for pub in self.totalscores:
                    self.totalscores[pub] += weight*scores.get(pub, 0)
            return self.normalizescores(self.totalscores)

        #if only citation count is selected
        elif self.var.get()==0 and self.var2.get()==1:
            self.totalscores = dict([(pub, 0) for pub in results])
            weights = [(0, self.frequencyscore(results)),(weight2, self.citationscore(results))]
            for (weight,scores) in weights:
                for pub in self.totalscores:
                    self.totalscores[pub] += weight*scores.get(pub, 0)
            return self.normalizescores(self.totalscores)
        else:
            tkMessageBox.showerror("Error","Please choose at least one ranking measure.")

    def MakeBoldAndBlue(self,word):    #get help from stackoverflow.com/questions/19283565/tkinter-how-to-get-index-for-a-specific-word

        start = '1.0'
        while True:
            tag_start = self.text.search(word, start, stopindex=END)
            if not tag_start: break
            tag_end = '%s+%dc' % (tag_start, len(word))
            self.text.tag_add('bold', tag_start, tag_end)
            self.text.tag_add("blue",tag_start,tag_end)
            self.text.tag_configure('bold', font='TkDefaultFont 10 bold')
            self.text.tag_configure("blue", foreground="blue")
            start = tag_start + "+1c"
        start2="1.0"
        while True:
            tag_start2 = self.text.search(word[0].upper()+word[1:], start2, stopindex=END)
            if not tag_start2: break
            tag_end2 = '%s+%dc' % (tag_start2, len(word))
            self.text.tag_add('bold', tag_start2, tag_end2)
            self.text.tag_add("blue",tag_start2,tag_end2)
            self.text.tag_configure('bold', font='TkDefaultFont 10 bold')
            self.text.tag_configure("blue", foreground="blue")
            start2 = tag_start2 + "+1c"

    def Search(self):

        start_time=time.time() #to start counting time
        self.label7=Label(bg="blue",fg="white",text="1", font='Helvetica 14', width=2)
        self.label7.grid(column=9,row=8)
        try:
            try:
                self.keywords=self.entry2.get().lower()
                self.wordlocation = shelve.open("wordlocation.db",flag='r')
                self.citation_count = shelve.open("citation_count.db",flag='r')
                self.group_by_pub = shelve.open("group_by_pub.db",flag='r')
                r,w=self.getmatchingpages(self.keywords)
                self.main_results=self.getscoredlist(r,w)
            except:
                tkMessageBox.showerror("Error","Please provide at least one keyword")

            #for deciding which type of publication is selected from listbox
            self.selected_type=[]
            self.curselection=self.listbox.curselection()
            for i in self.curselection:
                self.selected_type.append(self.sorted_type[i])

            #to find all titles in selected types of publications from listbox
            self.selected_type_pub=[]
            for i in self.selected_type:
                for x in self.group_by_pub[i]:
                    for y in x:
                        self.selected_type_pub.append(y)

            #to find intersection of title of publication coming from keywords and title of publications coming from listbox
            self.intersection=list(set(self.selected_type_pub)&set(self.main_results.keys()))

            self.last_dict={}
            for i in self.intersection:
                self.last_dict[i]=self.main_results[i] #last_dict= {title of publication1: score1, title of publication2:score2,...}

            self.text=Text(height=20) #creating textbox which results will seem
            self.text.grid(row=7,column=3,columnspan=8,sticky="WE",pady=10)
            self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
            self.scroll.grid(row=7,column=11,sticky="NS")
            self.text.configure(yscrollcommand=self.scroll)


            #get help from http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
            sort1=[]
            sort2=[]
            for keys,values in sorted(self.last_dict.iteritems(), key=lambda (k,v): (v,k),reverse=True):  #to sort dictinaries by values
                sort1.append(keys)
                sort2.append(values)


            for item in sort1:
                self.text.insert(END,sort1.index(item)+1)
                self.text.insert(END,".         ")
                self.text.insert(END,item)
                self.text.insert(END," ")
                self.text.insert(END,round(float(sort2[sort1.index(item)]),4))
                self.text.insert(END,"\n")


            self.elapsed_time=time.time()-start_time  #to measure elapsed time
            self.elapsed_time=round(float(self.elapsed_time),3)

            #number of publications and showing their finding time
            publication_number=str(len(sort1))+" Publications   "+"("+str(self.elapsed_time)+" seconds)"
            self.label6=Label(text=publication_number,font="Arial 14",fg="red",width=30)
            self.label6.grid(row=6,column=4)

            self.result=self.text.get("1.0",END).encode("utf-8").splitlines()
            self.text.delete("1.0",END)
            for i in self.result[0:10]:
                self.text.insert(END,i)
                self.text.insert(END,"\n")
            if len(self.keywords.split())==1:
                self.MakeBoldAndBlue(self.keywords)
            if len(self.keywords.split())>1:
                words=self.keywords.split()
                for i in words:
                    self.MakeBoldAndBlue(i)
            self.z=int(self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:-1])
        except:
            IndexError




    def Next_Value(self,a): #for create next textboxes

        for i in self.result[a:a+10]:
            self.text.insert(END,i)
            self.text.insert(END,"\n")
        if len(self.keywords.split())==1:
                self.MakeBoldAndBlue(self.keywords)
        if len(self.keywords.split())>1:
            words=self.keywords.split()
            for i in words:
                self.MakeBoldAndBlue(i)
        self.z=self.z+10

    def Next(self): #next button's command

        self.text=Text(height=20)
        self.text.grid(row=7,column=3,columnspan=8,sticky="WE",pady=10)
        self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
        self.scroll.grid(row=7,column=11,sticky="NS")
        self.text.configure(yscrollcommand=self.scroll)
        self.Next_Value(self.z)
        try:
            if int(self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:-1])<100:
                self.label7=Label(bg="blue",fg="white",text=self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0], font='Helvetica 14', width=2)
                self.label7.grid(column=9,row=8)
            elif int(self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:-1])>=100:
                self.label7=Label(bg="blue",fg="white",text=self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:2], font='Helvetica 14', width=2)
                self.label7.grid(column=9,row=8)
        except:
            IndexError

    def Previous_Value(self,b): #for create previous textboxes

        for i in self.result[b-20:b-10]:
            self.text.insert(END,i)
            self.text.insert(END,"\n")
        if len(self.keywords.split())==1:
                self.MakeBoldAndBlue(self.keywords)
        if len(self.keywords.split())>1:
            words=self.keywords.split()
            for i in words:
                self.MakeBoldAndBlue(i)
        self.z=self.z-10

    def Previous(self): #previous button's command

        self.text=Text(height=20)
        self.text.grid(row=7,column=3,columnspan=8,sticky="WE",pady=10)
        self.scroll=Scrollbar(command=self.text.yview,orient=VERTICAL)
        self.scroll.grid(row=7,column=11,sticky="NS")
        self.text.configure(yscrollcommand=self.scroll)
        self.Previous_Value(self.z)
        try:
            if int(self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:-1])<100:
                self.label7=Label(bg="blue",fg="white",text=self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0], font='Helvetica 14', width=2)
                self.label7.grid(column=9,row=8)
            elif int(self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:-1])>=100:
                self.label7=Label(bg="blue",fg="white",text=self.text.get("1.0",END).encode("utf-8").splitlines()[9].split()[0][0:2], font='Helvetica 14', width=2)
                self.label7.grid(column=9,row=8)
        except:
            IndexError
Main()