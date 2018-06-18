#Imported Modules

from Tkinter import *
import ttk
import tkFileDialog
import os
import xlrd
import anydbm
import tkMessageBox

class Main(): 
    def __init__(self): #Initial elements of the program. When main class called, these elements will be processed automatically.
        self.root = Tk()    #Program's main window

        #Window settings
        self.root.geometry("600x500+400+150")
        self.root.title("Curriculum Wiewer by Oz&Gulmez")
        self.root.resizable(width = FALSE, height = TRUE)

        self.GUI()  #In every entrance to program, graphical interface will be created.

        self.last_situation = anydbm.open("curriculum.db", "c") #That is our save file. After we started program, the database will be created or open if it is already exist.
        self.file_path = ""     #The initial value for curriculum file's path. It is important for next if conditions.
        self.root.mainloop()  
        
    def GUI(self):      #Graphical user interface elements. All widgets is included that method for the beginning of the program.

        #Those widgets are permanent non-interactive widgets.
        self.label = Label(text = "Curriculum Wiewer", bg = "green", font = "Helvetica 32 italic", fg = "white", width = 25).grid(columnspan = 3, sticky = "WE")  
        self.select_file = Label(text = "Please select curriculum excel file: ", font = "Helvetica 13 bold").grid(row = 1,columnspan = 2, sticky = "e", pady = 12)
        self.browse_file = Button(text = "Browse", font = "Helvetica 11", command = self.browse_file_func).grid(column = 2, row = 1, sticky = "w", pady = 12)
        
        #Interactive widgets
        self.selected_curriculum = StringVar()         
        self.select_curriculum = Label(text = "Please select semester that you want to print: ", font = "Helvetica 13 bold").grid(row = 2,columnspan = 2, sticky = "e")
        self.curriculum_list = ttk.Combobox(textvariable = self.selected_curriculum, values=("Semester I", "Semester II", "Semester III", "Semester IV", "Semester V", "Semester VI", "Semester VII", "Semester VIII")).grid(column = 2, row = 2, sticky = "w")

        self.display_button = Button(text = "Display", font = "Helvetica 11", command = self.display_function).grid(row = 3, column = 2, sticky = "w", pady = 10)       
    
    def browse_file_func(self):     #Browse button's function. This method includes codes about working of the browse button.       
        self.file_path = tkFileDialog.askopenfilename(parent=self.root,title='Please select a directory')
        if ".xls" not in self.file_path:    #xls and xlsx are unique excel file extensions and all excel files must contain .xls part in its path.
                tkMessageBox.showerror("File Type Error", "The chosen file is not an Excel file. Be sure you selected an Excel File")
        self.last_situation["last file"] = self.file_path  #Saving the last chosen file in to database.     

    def display_function(self):     #Display button's function. This method includes codes about duties of display button. That is the main method that critical functions appears for users

        self.reset()    #visually clears the output part of the window, technically creates new frames on output part of the window.

        #Categories of the outputs. 

        Label(text = "Code", font = "Helvetica 12 bold").grid(row = 4, column = 0, pady = 10)
        Label(text = "Title", font = "Helvetica 12 bold").grid(row = 4, column = 1, pady = 10)
        Label(text = "Credit", font = "Helvetica 12 bold").grid(row = 4, column = 2, pady = 10)
        
        #if condition which checks inputs from user firstly, database for having previous data.

        if self.selected_curriculum.get() == "" and self.file_path == "" :
            if "last curriculum" in self.last_situation and "last file"  in self.last_situation:
                self.curriculum_file = xlrd.open_workbook(self.last_situation["last file"]).sheet_by_index(0) #Curriculum file variable

                #For loops for tracking file for inputs or imported datas from database. First checks rows, second checks columns.

                for row in range(47):
                    for column in range(15):
                        if self.curriculum_file.cell_value(row, column) == self.last_situation["last curriculum"]:
                            semester_row = row  #The row number which wanted curriculum information begins.
                            first_column = column   #The columns number which wanted curriculum information starts.

            else:
                tkMessageBox.showerror("Input Error", "Not found input or older session's data. Please enter semester and file information.")

        elif self.selected_curriculum.get() != "" and self.file_path != "":
                      
            self.last_situation["last curriculum"] = self.selected_curriculum.get() #Saving the last curriculum that selected by user into database.
            self.curriculum_file = xlrd.open_workbook(self.file_path).sheet_by_index(0) #Curriculum file variable
            
            for row in range(47):
                for column in range(15):
                    if self.curriculum_file.cell_value(row, column) == self.selected_curriculum.get():  #Selected curriculum data used in that loop.
                        semester_row = row
                        first_column = column

        elif self.selected_curriculum.get() != "" and self.file_path == "":     #User can choose another semester without selecting a new file path.    
            if "last file" in self.last_situation:
                self.curriculum_file = xlrd.open_workbook(self.last_situation["last file"]).sheet_by_index(0)   #calling file path info. from database.
                for row in range(47):
                    for column in range(15):
                        if self.curriculum_file.cell_value(row, column) == self.selected_curriculum.get():
                            semester_row = row
                            first_column = column
                self.last_situation["last curriculum"] = self.selected_curriculum.get()
            else:
                tkMessageBox.showerror("Missing Data", "You must select a file and a curriculum if you are running program for the first time.")
        else:   #General error massege, prevents a crush.
            tkMessageBox.showerror("Missing Data", "You must select new curriculum if you choose a new file.")

        last_column = first_column #Variable for last column of the wanted information's position in excel file. Created for while loop.

        while self.curriculum_file.cell_value(semester_row+1, last_column) != "ECTS":   #finds last column of interested part of the file.
            last_column = last_column + 1

        grid_column = 0 #Column numbers of the outputs' positions on the window. 
        grid_row = 5    #Row numbers of the outputs' positions on the window. 
               
        #Drawing output interface.

        while self.curriculum_file.cell_value(semester_row, first_column) != "":
            semester_row += 1
            for semester_column in range (first_column, last_column + 1):                
                if semester_column-first_column in [0,1,5]:
                    self.output(self.curriculum_file.cell_value(semester_row+1, semester_column), grid_row, grid_column)    # Calling output method for drawing labels.
                    grid_column += 1
            grid_row += 1
            grid_column = 0     

    def output(self, title, output_row, output_column):     #That method is for drawing output that user want to. To make easy, it was written in another method.
        Label(text = title, font = "Helvetica 10 bold italic").grid(row = output_row, column = output_column)   #each row contains information about one lesson.
        
    def reset(self):        #This method will reset output area for further processes. The way is covering outputs with a frame after each press on display button. Not efficient but works.
        Frame(self.root, width = 600, height = 200).grid(row = 5, rowspan = 10, columnspan = 3, sticky = "w")       
        
Main()
