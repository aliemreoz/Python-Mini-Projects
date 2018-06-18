#moduls which are used
from Tkinter import *
from PIL import Image, ImageTk
from tkColorChooser import askcolor
import random

class Main():

    def __init__(self):

        self.root = Tk()
        self.root.geometry("1200x680+80+15")
        self.root.resizable(width = FALSE, height = FALSE)
        self.root.title("My Paint ")
        self.GUI()
        self.coor_dict={}
        self.overlaps={}
        self.fillcolor="#00ff00"
        self.bordercolor="#ff0000"
        self.move=False
        self.main_canvas.config (cursor ="tcross")
        self.root.mainloop()

    #visual item of project,they are just for visualite
    def GUI(self):

        self.label = Label(text = "My Paint",bg = "orange", font = "Helvetica 23 bold", fg = "white",width=65)
        self.label.grid(row=0, column=0, columnspan=40, sticky = "WE")
        self.image1 = Image.open("rectangle.png")
        self.rectangle_photo = ImageTk.PhotoImage(self.image1)
        self.rect_button=Button(image=self.rectangle_photo,width="5",height="21",command=self.RectangleButton)
        self.rect_button.grid(row=1,column=14,sticky="WE",pady=5)
        self.image2 = Image.open("oval.png")
        self.oval_photo = ImageTk.PhotoImage(self.image2)
        self.oval_button=Button(image=self.oval_photo,width="5",height="21",command=self.OvalButton)
        self.oval_button.grid(row=1,column=15,sticky="WE",pady=5)
        self.image3 = Image.open("line.png")
        self.line_photo = ImageTk.PhotoImage(self.image3)
        self.line_button=Button(image=self.line_photo,width="5",height="21",command=self.LineButton)
        self.line_button.grid(row=1,column=16,sticky="WE",pady=5)
        self.image4 = Image.open("drag.png")
        self.drag_photo = ImageTk.PhotoImage(self.image4)
        self.drag_button=Button(image=self.drag_photo,width="5",height="21",command=self.Drag)
        self.drag_button.grid(row=1,column=17,sticky="WE",pady=5)
        self.image5 = Image.open("eraser.png")
        self.eraser_photo = ImageTk.PhotoImage(self.image5)
        self.eraser_button=Button(image=self.eraser_photo,width=5,height=21,command=self.Erase)
        self.eraser_button.grid(row=1,column=18,sticky="WE",pady=5)
        self.label=Label(text="Fill Color:",font="Helvetica 11 bold")
        self.label.grid(row=1,column=19,sticky="WE",pady=5)
        self.fill_button=Button(bg="Green",width="4",relief=FLAT,command=self.FillColor)
        self.fill_button.grid(row=1,column=20,sticky="W",pady=5)
        self.label2=Label(text="Border Color:",font="Helvetica 11 bold")
        self.label2.grid(row=1,column=21,sticky="WE",pady=5)
        self.border_button=Button(bg="Red",width="4",relief=FLAT,command=self.BorderColor)
        self.border_button.grid(row=1,column=22,sticky="W",pady=5)
        self.label3=Label(text="Weight:",font="Helvetica 11 bold")
        self.label3.grid(row=1,column=23,sticky="WE",pady=5)
        self.spinbox = Spinbox(from_=1,to=30,width=2)
        self.spinbox.grid(row=1,column=24,sticky="WE",pady=5)
        self.main_canvas=Canvas(bg="white",width=1000,height=580)
        self.main_canvas.grid(row=2,column=1,rowspan=24,columnspan=36,sticky="WE")
        self.beautify=Button(text="Beautify Layout",relief=RAISED,command=self.Beautify,font="Helvetica 11 bold")
        self.beautify.grid(row=1,column=25,sticky="W",pady=5,padx=10)

    #to select item that we want to drag
    def SelectItem(self, event):

        self.move = True
        self.movex, self.movey = event.x, event.y
        self.moveitem = self.main_canvas.find_closest(event.x, event.y)
        self.main_canvas.itemconfig(self.moveitem)

    #to move item
    def MoveItem(self, event):

        if not self.move:
            return
        dx = event.x - self.movex
        dy = event.y - self.movey
        self.main_canvas.move(self.moveitem, dx, dy)
        self.movex, self.movey = event.x, event.y

    #end of dragging process
    def DropItem(self, event):

        if not self.move:
            return
        self.main_canvas.itemconfig(self.moveitem)
        self.move = False

    #to create rectangle on canvas, we define points(startx, starty)
    def RectangleCreate(self, event):

        self.process = True
        self.startx, self.starty = event.x, event.y
        object = self.main_canvas.create_rectangle(self.startx, self.starty, event.x, event.y,
                                                   width=int(self.spinbox.get()),fill=self.fillcolor,
                                                   outline=self.bordercolor)


        self.rectangle = object

    #to create rectangle on canvas according to its coordinates
    def RectangleSize(self, event):

        if self.process==True:
            object = self.main_canvas.find_closest(event.x, event.y) #get points from where mouse is clicked
            self.main_canvas.coords(self.rectangle, self.startx, self.starty, event.x, event.y)

    #end of the creating rectangle process
    def RectangleDrop(self, event):

        if self.process==True:
            self.process = False
            self.main_canvas.itemconfig(self.rectangle)

        self.coor_dict[self.rectangle]=self.main_canvas.coords(self.rectangle)
        try:
            x1,y1,x2,y2=self.main_canvas.coords(self.rectangle)
        except:ValueError
        try:
            if len(self.main_canvas.find_overlapping(x1,y1,x2,y2))>1: #it means there is overlap
                self.overlaps[self.main_canvas.find_overlapping(x1,y1,x2,y2)[-1]]=self.main_canvas.find_overlapping(x1,y1,x2,y2)[0:-1]
        except:UnboundLocalError
    #to create oval shapes, we define points (startx, starty)
    def OvalCreate(self, event):

        self.process = True
        self.startx, self.starty = event.x, event.y#get points from where mouse is clicked
        object = self.main_canvas.create_oval(self.startx, self.starty, event.x, event.y,
                                              width=int(self.spinbox.get()),fill=self.fillcolor,outline=self.bordercolor)
        self.oval = object

    #to create oval shapes on canvas according to its coordinates
    def OvalSize(self, event):

        if self.process==True:
            object = self.main_canvas.find_closest(event.x, event.y)
            self.main_canvas.coords(self.oval, self.startx, self.starty, event.x, event.y)

    #end of the creating oval shapes process
    def OvalDrop(self, event):

        if self.process==True:
            self.process = False
            self.main_canvas.itemconfig(self.oval)

        self.coor_dict[self.oval]=self.main_canvas.coords(self.oval)
        try:
            x1,y1,x2,y2=self.main_canvas.coords(self.oval)
        except:ValueError
        try:
            if len(self.main_canvas.find_overlapping(x1,y1,x2,y2))>1: #it means there is overlap
                self.overlaps[self.main_canvas.find_overlapping(x1,y1,x2,y2)[-1]]=self.main_canvas.find_overlapping(x1,y1,x2,y2)[0:-1]
        except:UnboundLocalError
    #to create line, we define points(startx, starty)
    def LineCreate(self, event):

        self.process = True
        self.startx, self.starty = event.x, event.y
        object = self.main_canvas.create_line(self.startx, self.starty, event.x, event.y,
                                              width=int(self.spinbox.get()),fill=self.fillcolor)
        self.line = object

    #to create line on canvas according to its coordinate
    def LineSize(self, event):

        if self.process==True:
            object = self.main_canvas.find_closest(event.x, event.y)
            self.main_canvas.coords(self.line, self.startx, self.starty, event.x, event.y)

    #end of the creating line process
    def LineDrop(self, event):

        if self.process==True:
            self.process = False
            self.main_canvas.itemconfig(self.line)
        self.coor_dict[self.line]=self.main_canvas.coords(self.line)
        try:
            x1,y1,x2,y2=self.main_canvas.coords(self.line)
        except:ValueError
        try:
            if len(self.main_canvas.find_overlapping(x1,y1,x2,y2))>1:
                self.overlaps[self.main_canvas.find_overlapping(x1,y1,x2,y2)[-1]]=self.main_canvas.find_overlapping(x1,y1,x2,y2)[0:-1]
        except:UnboundLocalError
    #for creating rectangles by mouse action
    def RectangleButton(self):
        self.rect_button.config(relief=SUNKEN)
        self.oval_button.config(relief=RAISED)
        self.line_button.config(relief=RAISED)
        self.drag_button.config(relief=RAISED)
        self.eraser_button.config(relief=RAISED)
        self.main_canvas.config (cursor ="tcross")
        self.main_canvas.bind('<ButtonPress-1>', self.RectangleCreate)
        self.main_canvas.bind('<B1-Motion>', self.RectangleSize)
        self.main_canvas.bind('<ButtonRelease-1>', self.RectangleDrop)

    #for creating ovals by mouse action
    def OvalButton(self):
        self.rect_button.config(relief=RAISED)
        self.oval_button.config(relief=SUNKEN)
        self.line_button.config(relief=RAISED)
        self.drag_button.config(relief=RAISED)
        self.eraser_button.config(relief=RAISED)
        self.main_canvas.config (cursor ="tcross")
        self.main_canvas.bind('<ButtonPress-1>', self.OvalCreate)
        self.main_canvas.bind('<B1-Motion>', self.OvalSize)
        self.main_canvas.bind('<ButtonRelease-1>', self.OvalDrop)

    #for creating lines by mouse action
    def LineButton(self):
        self.rect_button.config(relief=RAISED)
        self.oval_button.config(relief=RAISED)
        self.line_button.config(relief=SUNKEN)
        self.drag_button.config(relief=RAISED)
        self.eraser_button.config(relief=RAISED)
        self.main_canvas.config (cursor ="tcross")
        self.main_canvas.bind('<ButtonPress-1>', self.LineCreate)
        self.main_canvas.bind('<B1-Motion>', self.LineSize)
        self.main_canvas.bind('<ButtonRelease-1>', self.LineDrop)

     #visuality and functionality of bordercolor button
    def FillColor(self):

        self.fillcolor = askcolor()[-1] #get a color code from tuple's last item, first three items are RGB codes
        self.fill_button.destroy()
        self.fill_button=Button(bg=self.fillcolor,width="4",relief=FLAT,command=self.FillColor)
        self.fill_button.grid(row=1,column=20,sticky="W",pady=5)

    #visuality and functionality of bordercolor button
    def BorderColor(self):

        self.bordercolor = askcolor()[-1] #get a color code from tuple's last item, first three items are RGB codes
        self.border_button.destroy()
        self.border_button=Button(bg=self.bordercolor,width="4",relief=FLAT,command=self.BorderColor)
        self.border_button.grid(row=1,column=22,sticky="W",pady=5)

    #for dragging shapes by mouse action
    def Drag(self):

        self.rect_button.config(relief=RAISED)
        self.oval_button.config(relief=RAISED)
        self.line_button.config(relief=RAISED)
        self.drag_button.config(relief=SUNKEN)
        self.eraser_button.config(relief=RAISED)

        self.main_canvas.config (cursor ="hand2")
        self.main_canvas.bind('<ButtonPress-1>', self.SelectItem)
        self.main_canvas.bind('<B1-Motion>', self.MoveItem)
        self.main_canvas.bind('<ButtonRelease-1>', self.DropItem)
    #process of Erase function
    def SelectErase(self,event):

        self.erasex, self.erasey = event.x, event.y
        self.eraseitem = self.main_canvas.find_closest(event.x, event.y)
        self.main_canvas.delete(self.eraseitem)

    #for deleting shapes by mouse action
    def Erase(self):
        self.rect_button.config(relief=RAISED)
        self.oval_button.config(relief=RAISED)
        self.line_button.config(relief=RAISED)
        self.drag_button.config(relief=RAISED)
        self.eraser_button.config(relief=SUNKEN)
        self.main_canvas.config (cursor ="X_cursor")
        self.main_canvas.bind('<ButtonPress-1>', self.SelectErase)

    #optimization part, it will minimize the overlaps between shapes
    def Beautify(self):

         try:
            domain=(1150,580)  #domain of canvas
            best=None
            for i in self.overlaps.keys():
                x_dist=self.coor_dict[i][2]-self.coor_dict[i][0]
                y_dist=self.coor_dict[i][3]-self.coor_dict[i][1]
                for j in range(1000): #try to find coordinates that does not occupied by another shapes
                    x=random.randint(0, domain[0])
                    y=random.randint(0, domain[1])

                    if len(self.main_canvas.find_overlapping(x,y,x+x_dist,y+y_dist))==0:
                        if x+x_dist<1150-x_dist:#if condition for does not beyond canvas size
                            if y+y_dist<580-y_dist: #if condition for does not beyond canvas size
                                best=(x,y)


                self.main_canvas.move(i,best[0]-self.coor_dict[i][0],best[1]-self.coor_dict[i][1])#move overlapping shapes to best coordinate
                best=None
         except:NoneType



Main()
