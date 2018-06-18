from Tkinter import *
import ttk
from xlrd import *
import anydbm
import pickle
from recommendations import * #we transform that codes to python package

class Main():
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE) # for preventing resize of window
        self.root.title("Enter the Recommender")
        #calling main functions of program
        self.GUI()
        self.TOP()
        self.CC_Ratings()
        self.GetDataFromDatabase()
        self.MIDDLE()
        self.BOTTOM()

        self.root.mainloop()

    def GUI(self):

        #visual item of project,they are just for visualite

        self.label = Label(text = "Cafe Crown Recommendation Engine - SEHIR Special Edition",bg = "black", font = "Helvetica 14 bold", fg = "yellow", width =100)
        self.label.grid(row= 0,columnspan = 10 , sticky = "WE")

        self.welcoming_message = Label(text = "Welcome! \n Please rate entries that you have had at CC, and we will recommend you what you may like to have!", font= "Calibri 13 bold italic")
        self.welcoming_message.grid(row=1,columnspan = 10, sticky = "WE")

        self.line = Label(text = "................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................. ",font= "Calibri 5")
        self.line.grid(row=2,columnspan = 10, sticky = "WE")

        self.text1 = Label(text = "Choose a meal:",font="Calibri 12 bold",fg="red")
        self.text1.grid(column = 0,row = 3,columnspan=2,sticky=W,padx=15)

        self.text2 = Label(text = "Enter your rating:",font="Calibri 12 bold",fg="red")
        self.text2.grid(column = 2,row = 3,columnspan=2,sticky=W)

        self.line2 = Label(text = "................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................. ",font= "Calibri 5")
        self.line2.grid(row=6,columnspan = 10, sticky = "WE")

        self.get_rec_message = Label(text = "Get Recommedations", font= "Helvetica 13 bold italic")
        self.get_rec_message.grid(row=7,columnspan = 10, sticky = "WE")

        self.line3 = Label(text = "................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................. ",font= "Calibri 5")
        self.line3.grid(row=8,columnspan = 10, sticky = "WE")

        self.text3 = Label(text = "Settings: ",font="Calibri 12 bold",fg="red")
        self.text3.grid(column = 0,row = 9,columnspan=2,sticky=W,padx=15)

        self.num_of_rec = Label(text="Number of recommedations:",font="Calibri 9" )
        self.num_of_rec.grid(column = 0,row = 10,columnspan=2,sticky="E",padx=15)

        self.text4 = Label(text="Choose recommendation method:",font="Calibri 9",fg="red" )
        self.text4.grid(column = 4,row = 10,columnspan=2,sticky="W",padx=15)

        self.text5 = Label(text="Choose similarity metric:",font="Calibri 9",fg="red" )
        self.text5.grid(column = 4,row = 13,columnspan=2,sticky="W",padx=15)

        self.line4 = Label(text = "................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................. ",font= "Calibri 5")
        self.line4.grid(row=17,columnspan = 10, sticky = "WE")

        self.text6 = Label(text = "Result Box (Recommendations) : ",font="Calibri 12 bold",fg="red")
        self.text6.grid(column = 0,row = 18,columnspan=2,sticky="W",padx=5)

        self.label2=Label(text = "Resultbox 2",bg = "purple", font = "Helvetica 9", fg = "white")
        self.label2.grid(row= 19,column =3,columnspan=2,sticky = "WE")

        self.label2=Label(text = "Resultbox 3",bg = "red", font = "Helvetica 9", fg = "white")
        self.label2.grid(row= 19,column =6,columnspan=3,sticky = "WE",padx=5)

    def TOP(self):

        #top part of the project

        self.rated_meals=Listbox(width=45, height=10)
        self.rated_meals.grid(column=5,row=3,rowspan=3,columnspan=2,sticky="WE")
        self.scroll1=Scrollbar(command=self.rated_meals.yview,orient=VERTICAL)
        self.scroll1.grid(column=7,row=3,rowspan=3,sticky="NS")
        self.rated_meals.configure(yscrollcommand=self.scroll1.set)

        self.add_button = Button(text = "        Add        ", font = "Calibri 10 bold", fg="blue",command=self.Add)
        self.add_button.grid(column = 4, row = 4, sticky=E,padx=30)

        self.remove_button= Button(text = "        Remove       \n Selected", font = "Calibri 10 bold", fg="red",command=self.Remove)
        self.remove_button.grid(column = 8, row = 4, sticky=W,padx=30)


        #getting item from excel file
        menu_file = open_workbook("Menu.xlsx","rb").sheet_by_index(0)
        self.selected_meal = StringVar()
        self.meal_list = ttk.Combobox( textvariable = self.selected_meal)
        list=[]
        for column in range(1):    #meals are gathered in only one column
            for row in range(67):       #and 67 rows
                a=menu_file.cell(row+1,column).value.encode('utf-8')    #written row+!,because the first row does not have any meal, it is title
                list.append(a)
        self.meal_list["values"]=list
        self.meal_list.grid(column = 0, row = 4,columnspan=2,sticky=W,padx=15)

        self.slider=Scale(from_=1, to=10, length=275, orient=HORIZONTAL)
        self.slider.grid(column = 2,row = 4,columnspan=2,sticky="W")

        #creating databases and dictionaries for upcoming functions
        self.cc_ratings=anydbm.open("cc_ratings.db","c")
        self.CC_Ratings_dict={}
        self.Temp_dict={}
        self.OwnRatings_dict={}
        self.ownratings1=anydbm.open("own_ratings1.db","c") #keys=meal , values=ratings
        self.ownratings2=anydbm.open("own_ratings2.db","c") #keys="User" , values = {meals,rating}

    def GetDataFromDatabase(self):

        #when user open the program, database informations seem on listbox which in top

        self.DatabaseDict={}

        for keys,values in self.ownratings1.items():     #transform database to dictionary
            self.DatabaseDict[keys]=pickle.loads(values)

        for i,j in self.DatabaseDict.items():           #adding item on listbox from dictionary
            self.rated_meals.insert(END,(i,"--->",j))

    def CC_Ratings(self):

    #transfrom given database which is cc_ratings.db to dictionary

        for i,j in self.cc_ratings.items():
            self.CC_Ratings_dict[i]=pickle.loads(j)

    def Add(self):

        #getting meal name and rating,then they become keys and values of dictionaries respectively
        self.Adding_Dict={}
        self.Adding_Dict[self.meal_list.get().encode('utf-8')]=self.slider.get()
        for i,j in self.Adding_Dict.items():
            self.rated_meals.insert(END,(i,"--->",j))   #adding data(meal and rating) to listbox



        #getting meal name and rating,then they become keys and values of database respectively
        self.ownratings1[self.meal_list.get().encode('utf-8')]=pickle.dumps(self.slider.get())
        for i,j in self.ownratings1.items():
            self.Temp_dict[i]=pickle.loads(j)      #transform db to dict

        #key of db become "User" and values become self.Temp_dict which we create in upper line
        self.ownratings2["User"]=pickle.dumps(self.Temp_dict)
        for i,j in self.ownratings2.items():
            self.OwnRatings_dict[i]=pickle.loads(j)   #transform db to dict


        #putting together of two dict which are CC_Ratings_dict and OwnRatings_dict
        for keys1,values1 in self.OwnRatings_dict.items():
            for keys2,values2 in self.CC_Ratings_dict.items():
                if keys2 not in keys1:
                    self.OwnRatings_dict[keys2]=self.CC_Ratings_dict[keys2]


    def Remove(self):
        #removing items from db
        self.removing_item_index = self.rated_meals.curselection()
        self.starting_point = 0
        self.a=(self.rated_meals.get(ACTIVE)[0])
        self.b= ((self.a).encode("utf-8")) #changing type of items from unicode to str
        del self.ownratings1[self.b]

        #removing items from listbox depend on their index
        for i in self.removing_item_index :
            idx = int(i) - self.starting_point
            self.rated_meals.delete( idx,idx )
            self.starting_point = self.starting_point + 1


    def MIDDLE(self):

        #middle part of the project

        self.v=IntVar()
        self.v.set(6)

        self.entry = Entry(textvariable=self.v,width=5)
        self.entry.grid(column = 2,row = 10,sticky="W")



        self.var = IntVar()
        self.var2 = IntVar()

        self.R1_1 = Radiobutton(text="User-Based",variable=self.var, value=1)
        self.R1_1.grid(column = 4,row = 11,columnspan=2,sticky="W",padx=30)

        self.R1_2 = Radiobutton(text="Item-Based",variable=self.var, value=2)
        self.R1_2.grid(column = 4,row = 12,columnspan=2,sticky="W",padx=30)

        self.R2_1 = Radiobutton(text="Euclidean Score",variable=self.var2, value=3)
        self.R2_1.grid(column = 4,row = 14,columnspan=2,sticky="W",padx=30)

        self.R2_2 = Radiobutton(text="Pearson Score",variable=self.var2, value=4)
        self.R2_2.grid(column = 4,row = 15,columnspan=2,sticky="W",padx=30)

        self.R2_3 = Radiobutton(text="Jaccard Score",variable=self.var2, value=5)
        self.R2_3.grid(column = 4,row = 16,columnspan=2,sticky="W",padx=30)

        self.get_rec_button= Button(text = "Get Recommendation", font = "Calibri 11 bold", fg="blue", command=self.GetRec)
        self.get_rec_button.grid(column = 6, row = 14, sticky=W)


        #for selecting user to show him/her ratings, we add a button for doing that work
        self.get_user_rec_button= Button(text=" --> ", font = "Calibri 12 bold", fg="blue", command=self.SelectingUser)
        self.get_user_rec_button.grid(column = 5, row = 21,  sticky="WE" ,padx=30)

    def GetRec(self):

        self.entry_value=int(self.entry.get())


        self.Reset() #cleaning the resultboxes

        #creating if condition according to user select, user-based=1(euclidean=3,pearson=4,jaccard=5) and item-based=2

        if str(self.var.get())=="1" and str(self.var2.get())=="3":

            self.label2=Label(text = "Users similar to you",bg = "purple", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =3,columnspan=2,sticky = "WE")

            self.label2=Label(text = "User ratings (select a user on the left) ",bg = "red", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =6,columnspan=3,sticky = "WE",padx=5)

            self.user_euclidean_list = getRecommendations(self.OwnRatings_dict,"User",sim_distance)

            for i,j in self.user_euclidean_list[0:(self.entry_value)]:
                self.resultbox.insert(END,(round(i,2), "-->",j))

            self.euclidean_users=topMatches(self.OwnRatings_dict,"User",n=7,similarity=sim_distance)

            for k,l in self.euclidean_users:
                self.resultbox2.insert(END,(round(k,2),"-",l))

        if str(self.var.get())=="1" and str(self.var2.get())=="4":

            self.label2=Label(text = "Users similar to you",bg = "purple", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =3,columnspan=2,sticky = "WE")

            self.label2=Label(text = "User ratings (select a user on the left) ",bg = "red", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =6,columnspan=3,sticky = "WE",padx=5)

            self.user_pearson_list = getRecommendations(self.OwnRatings_dict,"User",sim_pearson)

            for i,j in self.user_pearson_list[0:(self.entry_value)]:
                self.resultbox.insert(END,(round(i,2), "-->",j))

            self.pearson_users=topMatches(self.OwnRatings_dict,"User",n=7,similarity=sim_pearson)

            for k,l in self.pearson_users:
                self.resultbox2.insert(END,(round(k,2),"-",l))

        if str(self.var.get())=="1" and str(self.var2.get())=="5":

            self.label2=Label(text = "Users similar to you",bg = "purple", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =3,columnspan=2,sticky = "WE")

            self.label2=Label(text = "User ratings (select a user on the left) ",bg = "red", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =6,columnspan=3,sticky = "WE",padx=5)

            self.user_jaccard_list = getRecommendations(self.OwnRatings_dict,"User",sim_jaccard)

            for i,j in self.user_jaccard_list[0:(self.entry_value)]:
                self.resultbox.insert(END,(round(i,2), "-->",j))

            self.jaccard_users=topMatches(self.OwnRatings_dict,"User",n=7,similarity=sim_jaccard)

            for k,l in self.jaccard_users:
                self.resultbox2.insert(END,(round(k,2),"-",l))


        self.itemsim = calculateSimilarItems(self.OwnRatings_dict)

        if str(self.var.get())=="2":

            self.resultbox3.delete(0, END)

            self.label2=Label(text = "    Your Ratings    ",bg = "purple", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =3,columnspan=2,sticky = "WE")

            self.label2=Label(text = "Similiar Items (select an item on the left)",bg = "red", font = "Helvetica 9", fg = "white")
            self.label2.grid(row= 19,column =6,columnspan=3,sticky = "WE",padx=5)

            self.item_list= getRecommendedItems(self.OwnRatings_dict,self.itemsim,"User")

            for i,j in self.item_list[0:(self.entry_value)]:
                self.resultbox.insert(END,(round(i,2), "-->",j))

            for i,j in self.Temp_dict.items():
                self.resultbox2.insert(END,(i,"-->",j))

    def SelectingUser(self):

        self.resultbox3.delete(0, END) #cleaning the resultbox3 to prevent mix of selection


        #creating the resulbox3 according to user-selection
        if str(self.var.get())=="1" and str(self.var2.get())=="3":

            self.user_tup = self.resultbox2.curselection()
            self.user_index=self.user_tup[0]
            self.selected_user = (self.euclidean_users[self.user_index])[1]

            self.SelUserRating=self.OwnRatings_dict[self.selected_user]
            self.resultbox3.insert(END,(self.selected_user + " also rated the following"))

            for keys,values in self.SelUserRating.items():
                self.resultbox3.insert(END,(keys+"-->"+str(values)))

        if str(self.var.get())=="1" and str(self.var2.get())=="4":

            self.user_tup = self.resultbox2.curselection()
            self.user_index=self.user_tup[0]
            self.selected_user = (self.pearson_users[self.user_index])[1]
            self.SelUserRating=self.OwnRatings_dict[self.selected_user]
            self.resultbox3.insert(END,(self.selected_user + " also rated the following"))

            for keys,values in self.SelUserRating.items():
                self.resultbox3.insert(END,(keys+"-->"+str(values)))

        if str(self.var.get())=="1" and str(self.var2.get())=="5":

            self.user_tup = self.resultbox2.curselection()
            self.user_index=self.user_tup[0]
            self.selected_user = (self.jaccard_users[self.user_index])[1]
            self.SelUserRating=self.OwnRatings_dict[self.selected_user]
            self.resultbox3.insert(END,(self.selected_user + " also rated the following"))

            for keys,values in self.SelUserRating.items():
                self.resultbox3.insert(END,(keys+"-->"+str(values)))

        if str(self.var.get())=="2":

            self.meal_tup=self.resultbox2.curselection()
            self.meal_index=self.meal_tup[0]
            self.select_item=self.Temp_dict.items()[self.meal_index]
            self.selected_items=self.select_item[0]
            self.similiar_items=calculateSimilarItems(self.OwnRatings_dict,67)

            for i,j in self.similiar_items[self.selected_items]:
                self.i=round(i,2)
                self.resultbox3.insert(END,(j+"-->"+str(self.i)))

    def Reset(self):
        #cleaning the resultbox1 and resultbox2 to prevent mix of selection
        self.resultbox.delete(1, END)
        self.resultbox2.delete(0, END)

    def BOTTOM(self):
        #bottom part of the project which includes resultboxes

        self.resultbox = Listbox(width=35, height=7)
        self.resultbox.grid(column=0,row=19,rowspan=4,columnspan=2,sticky="WE",padx=5)
        self.scroll2=Scrollbar(command=self.resultbox.yview,orient=VERTICAL)
        self.scroll2.grid(column=2,row=19,rowspan=4,sticky="NSW")
        self.resultbox.configure(yscrollcommand=self.scroll2.set)
        self.resultbox.insert(END,"Similarity Score --> Recommendation")

        self.resultbox2 = Listbox(width=20, height=5)
        self.resultbox2.grid(column=3,row=20,rowspan=3,columnspan=2,sticky="WE",)

        self.resultbox3 = Listbox(width=50, height=5)
        self.resultbox3.grid(column=6,row=20,rowspan=3,columnspan=3,sticky="WE",padx=5)
        self.scroll3=Scrollbar(command=self.resultbox3.yview,orient=VERTICAL)
        self.scroll3.grid(column=9,row=20,rowspan=4,sticky="NSW")
        self.resultbox3.configure(yscrollcommand=self.scroll3.set)

Main()