"""
Minesweeper

Implements a basic minesweeper game using the tkinter module.
Uses a Model-View-Controller structure.
"""

from functools import reduce
from itertools import product
from operator import add
from random import sample
from tkinter import Button, Frame, Label, StringVar, Tk,messagebox
from typing import Set, Tuple
import random,sys,os
from sys import exit
from tkinter import *


     
def get_adjacent(index: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Returns adjacent coordinates for input index"""

    x, y = index

    return {
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        }


class Model(object):
    """Creates a board and adds mines to it."""

    def __init__(self, width: int, height: int, num_mines: int,typ:str):
        self.width = width
        self.height = height
        self.num_mines = num_mines        
        self.grid = self.create_grid()
        print(self.grid)
        self.add_mines()    
        self.typ=typ    
        self.grid_coords = self.grid_coords()
        self.adjacent_mine_count()
        self.cells_revealed = set()     
        self.cells_flagged = set()
        self.revealed_zeroes = set()
        self.game_state = None


    def create_grid(self) -> list:
        """Returns a (width by height) grid of elements with value of 0."""
        self.softG=[[0] * self.width for _ in range(self.height)]

        return [[0] * self.width for _ in range(self.height)]#Not necessary

    def add_mines(self):
        """Randomly adds mines to board grid."""

        for x, y in sample(list(product(range(self.width), range(self.height))), self.num_mines):
            self.grid[y][x] = 'm'

    def grid_coords(self) -> list:
        """Returns a list of (x, y) coordinates for every position on grid."""

        return [(x, y) for y in range(self.height) for x in range(self.width)]

    def adjacent_mine_count(self):
        """Sets cell values to the number of their adjacent mines."""

        def is_mine(coords):
            try:
                if coords[0] >= 0 and coords[1] >= 0:
                    return self.grid[coords[1]][coords[0]] == 'm'
                else:
                    return False
            except IndexError:
                return False

        for position in self.grid_coords: 
            x, y = position
            if self.grid[y][x] != "m":
                grid_value = reduce(add, map(is_mine, get_adjacent(position)))
                self.grid[y][x] = grid_value

    def get_cell_value(self, index: Tuple[int, int]) -> int or str:
        """Returns model's cell value at the given index."""

        x, y = index
        return self.grid[y][x]



class View(Frame):
    """Creates a GUI with a grid of cell buttons."""

    def __init__(self, width: int, height: int, 
                 num_mines: int, difficulty: str, typ:str,controller: "Controller"):
        self.master = Tk()
        #self.master.title('Minesweeper')
        self.width = width
        self.height = height
        self.typ=typ
        self.flag=False
        self.num_mines = num_mines
        self.difficulty = difficulty
        self.controller = controller
        if self.controller.load_data!=None:
            self.flag=True
        self.cancelable=None
        self.record=[]
        self.color_dict = {
            0: 'white', 1: 'blue', 2: 'green',
            3: 'red', 4: 'orange', 5: 'purple',
            6: 'grey', 7: 'grey', 8: 'grey', "m": "black"
            }
        self.master.title('Minesweeper')


    def create_buttons(self) -> list:
        """Create cell button widgets."""

        def create_button(x, y):
            button = Button(self.master, width=5, bg='grey')
            button.grid(row=y + 5, column=x + 1)
            return button

        return [[create_button(x, y) for x in range(self.width)] 
                                     for y in range(self.height)]

    def initialize_bindings(self):
        """Set up the reveal cell and the flag cell key bindings."""

        for x in range(self.width):
            for y in range(self.height):
                def closure_helper(f, index):
                    def g(_): 
                        
                        f(index)                    
                    return g

                # Bind reveal decision method to left click
                self.buttons[y][x].bind(
                        '<Button-1>', closure_helper(
                        self.controller.reveal_decision, (x, y)))

                # Bind flag method to right click
                self.buttons[y][x].bind(
                        '<Button-3>', closure_helper(
                        self.controller.update_flagged_cell, (x, y)))

        # Set up reset button
        #self.top_panel.reset_button.bind('<Button-1>', self.controller.reset)

    def reset_view(self):
        """Destroys the GUI. Controller will create a new GUI"""

        self.master.destroy()
        #self.master=Tk()########################Again creating master window

    def reveal_cell(self, index: Tuple[int, int], value: int or str):
        """Reveals cell's value on GUI."""

        x, y = index
        self.buttons[y][x].configure(text=value, bg=self.color_dict[value])
        #self.record[x][y]=[value,self.color_dict[value]]

    def flag_cell(self, index: Tuple[int, int]):
        """Flag cell in GUI"""

        x, y = index
        self.buttons[y][x].configure(text="FLAG", bg="yellow")

    def unflag_cell(self, index: Tuple[int, int]):
        """Unflag cell in GUI"""
        x, y = index
        self.buttons[y][x].configure(text="", bg="grey")

    def update_mines_left(self, mines: int):
        """Updates mine counter widget"""

        self.top_panel.mine_count.set("Mines remaining: " + str(mines))

    def display_loss(self):
        """Display the loss label when lose condition is reached."""

        self.top_panel.loss_label.grid(row=0, columnspan=10)
        #print(self.grid)

    def display_win(self):
        """Display the win label when win condition is reached."""

        self.top_panel.win_label.grid(row=0, columnspan=10)

    def play_computer(self):
        try:
            for x in range(self.width):
                for y in range(self.height):
                    def closure_helper(f, index):
                        print(x,y)
                        def g(f,index): 
                            #print('yes')
                            f(index)                    
                        return g(f,index)
            if self.flag:
                if self.controller.load_data[1]!=[''] and self.controller.load_data[1]!=[]:
                    x,y=self.controller.load_data[1][0]
                    self.controller.load_data[1].remove((x,y))
                '''if  self.controller.load_data[1]!=[''] and self.controller.load_data[1]!=[]:
                    x1,y1=self.controller.load_data[1][0]
                    self.controller.load_data[2].remove((x1,y1))'''
                print('kysa')
                closure_helper(self.controller.reveal_decision, (x, y))
                #closure_helper(self.controller.update_flagged_cell, (x1, y1))
                if self.controller.load_data[1]==[] and self.controller.load_data[2]==[]:
                    self.flag=False
                    self.master.after_cancel(self.cancelable)
                    self.mainloop()
                self.cancelable=self.master.after(20,self.play_computer)
                        
            if not self.flag:
                x,y=random.randint(1,self.width-1),random.randint(1,self.height-1)
                flag=random.randint(1, 10)
                if flag%3!=0:
                    closure_helper(self.controller.reveal_decision, (x, y))
                else:#to put a at specific positions
                    closure_helper(self.controller.update_flagged_cell, (x, y))
                self.cancelable=self.master.after(3000,self.play_computer)

        except:
            pass        

    def mainloop(self):
        self.top_panel = TopPanel(self.master, self.height, 
                                  self.width, self.num_mines,controller=self.controller)
        self.buttons = self.create_buttons()
        self.top_panel.mines_left.grid(row=0, columnspan=5)
        if self.typ=='Player vs Computer' and not self.flag:    
            self.initialize_bindings()
        
        else:
            self.play_computer()
        self.master.mainloop()


class TopPanel(Frame):
    """Creates a top panel which contains game information."""

    def __init__(self, master: Tk, width: int, height: int, num_mines: int,controller='Controller'):
        Frame.__init__(self, master)
        self.controller=controller
        self.master = master
        self.master.title('Minesweeper')

        self.num_mines = num_mines
        self.grid()

        self.reset_button = Button(self.master, width=7, text='Reset',command=self.controller.reset)
        self.reset_button.grid(row=0)
        self.save_button=Button(self.master,width=7,text='Save',command=self.controller.save)
        self.save_button.grid(row=1,column=0)
        self.savs=['Save '+str(i) for i in range(5)]
        self.controller.sav = StringVar()#This variable will contain value for file to be saved in which save
        self.controller.sav.set(self.savs[0])
        self.controller.dropSav = OptionMenu( self.master , self.controller.sav , *self.savs)#options for selecting to which save file you want to save
        self.controller.dropSav.grid(row=2,column=0)

        self.loss_label = Label(text='You Lose!', bg='red')
        self.win_label = Label(text='You Win!', bg='green')

        self.mine_count = StringVar()
        self.mine_count.set('Mines remaining: ' + str(self.num_mines))
        self.mines_left = Label(textvariable=self.mine_count)


class TextView(object):
    """Creates a text interface of the minesweeper game."""

    def __init__(self, width: int, height: int, 
                 num_mines: int, difficulty: str, controller: "Controller"):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.controller = controller
        self.reveal_dict = {
            0: ' 0  ', 1: ' 1  ', 2: ' 2  ',
            3: ' 3  ', 4: ' 4  ', 5: ' 5  ',
            6: ' 6  ', 7: ' 7  ', 8: ' 8  ', "m": "mine"
            }
        self.cell_view = self.cell_view()
        self.show_grid()

    def cell_view(self)-> list:
        """Create text view of cells."""

        return [["cell" for x in range(self.width)] 
                         for y in range(self.height)]

    def show_grid(self):
        """Prints text grid to console. Includes column numbers."""

        top_row = [str(i) for i in range(self.width)]
        print(" ", *top_row, sep=" "*5)
        for row in range(len(self.cell_view)):
            print(str(row) + ":", *self.cell_view[row], sep="  ")

    def reveal_cell(self, index: Tuple[int, int], value: int or str):
        """Reveals a cell's value in the text view"""

        x, y = index
        self.cell_view[y][x] = self.reveal_dict[value]      

    def flag_cell(self, index: Tuple[int, int]):
        """Flags cell in cell_view"""

        x, y = index
        self.cell_view[y][x] = "FLAG"

    def unflag_cell(self, index: Tuple[int, int]):
        """Unflags cell in cell_view"""

        x, y = index
        self.cell_view[y][x] = "cell"

    def update_mines_left(self, mines):
        """Updates mine counter."""

        print("Mines remaining: " + str(mines))

    def display_loss(self):
        """Displays the lose label when loss condition is reached."""

        print("You Lose!")

    def display_win(self):
        """Displays the win label when win condition is reached."""

        print("You Win!")

    def mainloop(self):
        while True:
            try:
                cmd, *coords = input(
                        "Choose a cell in the format: "
                        + "flag/reveal x y. Type END to quit.  ").split()
                if cmd.lower()[0] == "e":
                    break
                x, y = coords[0], coords[1]
                if cmd.lower()[0] == "f":
                    self.controller.update_flagged_cell((int(x), int(y)))
                elif cmd.lower()[0] == "r":
                    self.controller.reveal_decision((int(x), int(y)))
                else:
                    print("Unknown command")
                self.show_grid()
            except:
                print("Incorrect selection or format")


class Controller(object):
    """Sets up button bindings and minesweeper game logic.

    Reveal_decision determines how to reveal cells. 
    End conditions are handled by the loss and win methods.
    """

    def __init__(self, width: int, height: int, 
                 num_mines: int, difficulty: str, view_type: str,typ:str,load=None):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.difficulty = difficulty
        self.load_data=load    
        self.typ=typ  
        self.flgs=[]
        self.clicks=[] 
        self.record=[]
        self.model = Model(self.width, self.height, self.num_mines,self.typ)
        if view_type == "GUI Game":
            self.view = View(self.width, self.height, 
                             self.num_mines, self.difficulty,self.typ, self)
        elif view_type == "TEXT Game":
            self.view = TextView(self.width, self.height, 
                                 self.num_mines, self.difficulty, self)
        self.view.mainloop()

    
    def save(self):
        self.record.append([self.width,self.height,self.num_mines])
        self.record.append(list(self.clicks))
        self.record.append(list(self.self.flgs))
        self.record.append(list(self.model.revealed_zeroes))
        for i in self.record:
            print(i,'Index'+str(self.record.index(i)))
        self.Saving()

    #game save 
    def Saving(self):
        nam=self.sav.get()  #getting all data from the game that i going to be saved
        #lists=self.data2Save()  #converting to a list format
        #lists=self.Savables(self.record)
        lisSavable=self.Savables(self.record) #converting to save format
        #print(lisSavable)   
        #exit()
        #nam='Save 0'
        self.sendToTxt(lisSavable,'Saves\\'+nam+'.txt') #calling save to text function

    #data in save file
    def data2Save(self):
        lis=[[self.numberOfHoles,self.numberOfGuesses],self.activeGuess,self.clr2save,self.answer]  #creating a list
        return lis

    #converting data to savable format
    def Savables(self,lists):
        #splitting to individual rows or lines for the file
        data=[[] for i in range(4)]
        data[0]=','.join([str(lists[0][0]),str(lists[0][1]),str(lists[0][2])])#first line will contain rows and columns
        outLis=[]
        for i in lists[1]:
            for j in i:
                outLis.append(str(j))
        data[1]=','.join(outLis) #active guess
        outLis=[]
        for i in lists[2]:
            for j in i:
                outLis.append(str(j))
        data[2]=','.join(outLis)#colors from the grid
        outLis=[]
        for i in lists[3]:
            for j in i:
                outLis.append(str(j))
        data[3]=','.join(outLis)  #answer
        return data


    #-----To Update Txt file Orderly according to frequency------#
    def sendToTxt(self,lists,directory='Saves/Save 01.txt'):
        nam=open(directory,'w') #opening the file and clearin it
        nam.close() #closing the file
        nam=open(directory,'a')         #opening it again
        for i in range(len(lists)): #looping almost 4 times
            argument=lists[i]+'\n'  #writing line wise
            nam.write(argument)
        nam.close() #closing the file
    
    def reset(self, event=None):
        """Resets the game"""
        if self.typ=='Computer vs Computer':
            self.view.master.after_cancel(self.view.cancelable)
            self.view.can=self.view.master.after(3000,self.cancelling)
        if self.load_data!=None:
            self.load_data=None

        self.view.reset_view()        
        self.model = Model(self.width, self.height, self.num_mines,self.typ)
        self.view = View(self.width, self.height, 
                         self.num_mines, self.difficulty,self.typ, controller=self)
        self.view.mainloop()
    def cancelling(self):
        self.view.after_cancel(self.view.can)
    def reveal_decision(self, index: Tuple[int, int]):
        """Main decision method determining how to reveal cell."""

        x, y = index
        self.clicks.append((x,y))
        cell_value = self.model.get_cell_value(index)
        if index in self.model.cells_flagged:
            return None

        if cell_value in range(1, 9):
            self.reveal_cell(index, cell_value)

        elif (
                self.model.grid[y][x] == "m" 
                and self.model.game_state != "win"
                ):
            self.loss()

        else:
            self.reveal_zeroes(index)

#        Check for win condition
        cells_unrevealed = self.height * self.width - len(self.model.cells_revealed) 
        if cells_unrevealed == self.num_mines and self.model.game_state != "loss":
            self.win()

    def reveal_cell(self, index: Tuple[int, int], value: int or str):
        """Obtains cell value from model and passes the value to view."""

        if index in self.model.cells_flagged:
            return None
        else:
            self.model.cells_revealed.add(index)
            self.view.reveal_cell(index, value)

    def reveal_adjacent(self, index: Tuple[int, int]):
        """Reveals the 8 adjacent cells to the input cell's index."""

        for coords in get_adjacent(index):
            if (
                    0 <= coords[0] <= self.width - 1 
                    and 0 <= coords[1] <= self.height - 1
                    ):
                cell_value = self.model.get_cell_value(coords)
                self.reveal_cell(coords, cell_value)

    def reveal_zeroes(self, index: Tuple[int, int]):
        """Reveals all adjacent cells just until a mine is reached."""

        val = self.model.get_cell_value(index)

        if val == 0:
            self.reveal_cell(index, val)
            self.reveal_adjacent(index)

            for coords in get_adjacent(index):
                if (
                        0 <= coords[0] <= self.width - 1
                        and 0 <= coords[1] <= self.height - 1
                        and self.model.get_cell_value(coords) == 0
                        and coords not in self.model.revealed_zeroes
                        ):
                    self.model.revealed_zeroes.add(coords)
                    self.reveal_zeroes(coords)

    def update_flagged_cell(self, index: Tuple[int, int]):
        """Flag/unflag cells for possible mines. Does not reveal cell."""
        
        if (
                index not in self.model.cells_revealed 
                and index not in self.model.cells_flagged
                ):
            self.flgs.append((x,y))
            self.model.cells_flagged.add(index)
            self.view.flag_cell(index)

        elif (
                index not in self.model.cells_revealed 
                and index in self.model.cells_flagged
                ):
            self.flgs.remove((x,y))
            self.model.cells_flagged.remove(index)
            self.view.unflag_cell(index)

        self.update_mines()

    def update_mines(self):
        """Update mine counter."""

        mines_left = self.num_mines - len(self.model.cells_flagged)

        if mines_left >= 0:
            self.view.update_mines_left(mines_left)

    def win(self):
        """Sweet sweet victory."""

        self.model.game_state = "win"
        self.view.display_win()

    def loss(self):
        """Show loss, and reveal all cells."""

        self.model.game_state = "loss"
        self.view.display_loss()

#        Reveals all cells
        for row in range(self.height):
            for col in range(self.width):
                cell_value = self.model.get_cell_value((col,row))
                self.view.reveal_cell((col, row), cell_value)


class InitializeGame(Frame):
    """Sets up minesweepergame. Allows player to choose difficulty"""

    def __init__(self):
        self.root = Tk()  
        self.root.title('Minesweeper')

        self.root.geometry('400x400')
        self.create_view_choice()
        self.create_difficulty_widgets()
        self.load=None
        self.root.mainloop()

    def create_view_choice(self):
        "Creates widgets allowing player to choose a view type."""
        self.frm=Frame(self.root,bg="light green")
        self.frm.pack()
        self.root.configure(background="light green")
        self.view_label = Label(self.frm, text="Select the game type",width=20,fg='white',bg='blue')
        self.view_label.grid(row=0,column=0,columnspan=2,pady=20)
        self.view_types = ["GUI Game", "TEXT Game"]
        self.count=0
        def create_button(view_type):
            button = Button(self.frm, width=8, bg='grey', text=view_type)
            button.grid(row=1,column=self.count,pady=20,padx=20)
            self.count+=1
            return button

        self.view_widgets = [
                create_button(view_type) for view_type in self.view_types
                ] + [self.view_label]+[self.frm]
        self.loadBtn=Button(self.frm,text='Load Game', width=8, bg='grey',command=self.Load_Window)
        self.loadBtn.grid(row=2,column=0,pady=20,padx=20)
        self.quitBtn=Button(self.frm,text='Exit Game', width=8, bg='grey',command=self.quitting)
        self.quitBtn.grid(row=2,column=1,pady=20,padx=20)
        self.view_widgets.append(self.loadBtn)
        self.view_widgets.append(self.quitBtn)
        for i in range(2):
            def closure_helper(f, view_choice):
                    def g(_): 
                        f(view_choice)                    
                    return g
            self.view_widgets[i].bind("<Button>", closure_helper(
                    self.set_up_difficulty_widgets, self.view_types[i]))
    def quitting(self):
        self.root.destroy()

    def clearAll(self):
        slavs=self.root.slaves()
        for slav in slavs:
            slav.destroy()

    def Load_Window(self):
        self.root.destroy()
        self.root=Tk()
        self.root.geometry('400x400')
        self.names=['Save '+str(i) for i in range(5)]   #This list will have names of all save files
        self.SaveLabs=[Button(self.root,text=name,width=20) for name in self.names]    #Creating that many labels as save files
        for widg in self.SaveLabs:  #Displaying all those labels
            widg.pack(pady=20)
        
        #Now to binding the labels individually so that they can respond to button click individually
        self.SaveLabs[0].bind('<Button-1>',lambda x:self.Starting(0))
        self.SaveLabs[1].bind('<Button-1>',lambda x:self.Starting(1))
        self.SaveLabs[2].bind('<Button-1>',lambda x:self.Starting(2))
        self.SaveLabs[3].bind('<Button-1>',lambda x:self.Starting(3))
        self.SaveLabs[4].bind('<Button-1>',lambda x:self.Starting(4))

    #Pressing any save file will call Starting function
    def Starting(self,ind):
        if self.read('Saves\\Save '+str(ind)+'.txt')!=['']:#If savestatus file has 1 at the respective position as file like save 3 means at index 3 then load file
            #self.clear()
            self.data=self.read("Saves\\Save "+str(ind)+'.txt')   #Calling file read function
            print(self.data)
            self.LoadedData=self.splitting()    #This will convert the data to game readable format
            self.root.destroy()
            #self.root=Tk()
            Controller(*self.LoadedData[0],'Medium','GUI Game','Player vs Computer',load=self.LoadedData) #then game will start
   
        else:   #if respective save game status is 0 then display following message
            messagebox.showinfo('Warning!','This is empty')
    
    #Convet data to game readable format
    def splitting(self):
        a=[[] for i in range(4)]    #a list of 4 lists as each save file has four rows
        RCtup=self.data[0].split(',')   #splitting data with comma delimmiters
        a[0]=[int(RCtup[0]),int(RCtup[1]),int(RCtup[2])]  #converting first element as number of columns and number of rows
        hlp=self.data[1].split(',')
        if len(hlp)!=0 and hlp!=['']:    
            outLis=[]#This is a 2d list and will contain which label wil be filled with which color
            for i in range(0,len(hlp),2):#Here a[0][0] is actually number of columns, it is used as step size and len(hlp) means that many time as the number of colors in list hlp
                #inLis=[]#inner list is initially empty
                outLis.append((int(hlp[i]),int(hlp[i+1])))#final list of colors for different racks of color labels in the game
            a[1]=outLis
        #Filled=[]#This is a 2d list and will contain which label wil be filled with which color
        hlp=self.data[2].split(',')
        if len(hlp)!=0 and hlp!=['']:
            outLis=[]#This is a 2d list and will contain which label wil be filled with which color
            for i in range(0,len(hlp),2):#Here a[0][0] is actually number of columns, it is used as step size and len(hlp) means that many time as the number of colors in list hlp
                outLis.append((int(hlp[i]),int(hlp[i+1])))#final list of colors for different racks of color labels in the game
        hlp=self.data[3].split(',')
        if len(hlp)!=0 and hlp!=['']:
            outLis=[]#This is a 2d list and will contain which label wil be filled with which color
            for i in range(0,len(hlp),2):#Here a[0][0] is actually number of columns, it is used as step size and len(hlp) means that many time as the number of colors in list hlp
                outLis.append((int(hlp[i]),int(hlp[i+1])))#final list of colors for different racks of color labels in the game
            a[3]=outLis
        return a




    def LoadFile(self):

        fil=self.read()

            #--------------------Read File-------------#
    def read(self,directory,x=4):
        maz=open(directory,'r') #This will open file at path directory
        a=[]    #initial empty list
        for i in range(x):  #Loop will run as many time as x is
            c=maz.readline()    #Reading data line by line
            c=c.rstrip('\n')    #removing last element which is enter key
            a.append(c) #appending to list
            if a==['']:
                return a
        maz.close() #file is then closed
        return a 
    def create_difficulty_widgets(self):
        """Set up widgets at start of game for difficulty."""
        #self.clearAll()
        self.diff_Fram=Frame(self.root)
        self.diff_Fram.pack()
        self.diff_label = Label(self.diff_Fram, text="Choose a difficulty")
        self.difficulty = ("Easy", "Medium", "Hard")
        self.diffVar=StringVar()
        self.diffVar.set(self.difficulty[0])
        self.difMenu=OptionMenu( self.diff_Fram , self.diffVar , *self.difficulty)
        #self.difMenu.grid()
        def create_button(difficulty):
            button = Button(self.diff_Fram, width=7, bg='grey', text=difficulty)
            return button

        self.difficulty_widgets = [create_button(diff) 
                                    for diff in self.difficulty]
        self.difficulty_widgets = [self.diff_label] + self.difficulty_widgets

    def set_up_difficulty_widgets(self, view_type: str):
        """Removes view widgets. Sets up difficulty options for view chosen."""

        for widget in self.view_widgets:
            widget.destroy()

        if view_type == "TEXT Game":
            self.difficulty_widgets[0].grid()
            self.difficulty_widgets[1].grid()

        else:
            count=0
            for widget in self.difficulty_widgets:
                widget.grid(row=0,column=count)
                count+=1
            self.LabRow=Label(self.diff_Fram,text='Rows',bg='grey',width=10).grid(row=1,column=0,pady=10)
            self.LabCol=Label(self.diff_Fram,text='Columns',width=10,bg='grey').grid(row=2,column=0,pady=10)
            self.mines=Label(self.diff_Fram,text='Mines',width=10,bg='grey').grid(row=3,column=0,pady=10)
            self.varsNumR=StringVar()
            self.varsNumC=StringVar()
            self.varsNumM=StringVar()
            self.varsNumR.set(10)
            self.varsNumC.set(10)
            self.varsNumM.set(10)
            self.varsNumR.trace('w',self.validate)
            self.varsNumC.trace('w',self.validate)
            self.varsNumM.trace('w',self.validate)
            self.entRow=Entry(self.diff_Fram,textvariable=self.varsNumR,width=10).grid(row=1,column=1,pady=10)
            self.entCol=Entry(self.diff_Fram,textvariable=self.varsNumC,width=10).grid(row=2,column=1,pady=10)
            self.entMin=Entry(self.diff_Fram,textvariable=self.varsNumM,width=10).grid(row=3,column=1,pady=10)
            self.typ=['Player vs Computer','Computer vs Computer']
            self.typV=StringVar()
            self.typV.set(self.typ[0])
            self.PlayOption=OptionMenu( self.diff_Fram , self.typV , *self.typ).grid(row=4,column=1,pady=10)
            self.PlayOp=Label(self.diff_Fram,text='Select Type',bg='grey').grid(row=4,column=0,pady=10)
            
        self.bind_difficulty_widgets(view_type)

    def validate(self,*args):
        if not self.varsNumR.get().isnumeric():
            correctedr = ''.join(filter(str.isnumeric,self.varsNumR.get()))#only numeric data can be written as the rows can only be numeric
            self.varsNumR.set(correctedr)#Correct  with numerics only is set
        if self.varsNumR.get()!='':
            if int(self.varsNumR.get())>25:
                correctedr = ''.join(filter(str.isnumeric,self.varsNumR.get()))#only numeric data can be written as the rows can only be numeric
                while int(correctedr)>25:
                    correctedr=correctedr[:-1]
                self.varsNumR.set(correctedr)#Correct  with numerics only is set
                messagebox.showinfo('Warning!','You can select only between 10 and 25')
        if not self.varsNumC.get().isnumeric():
            correctedc = ''.join(filter(str.isnumeric,self.varsNumC.get()))#only numeric data can be written as the columns can only be numeric
            self.varsNumC.set(correctedc)#Correct  with numerics only is set
        if self.varsNumR.get()!='':
            if int(self.varsNumC.get())>25:
                correctedc = ''.join(filter(str.isnumeric,self.varsNumC.get()))#only numeric data can be written as the rows can only be numeric
                while int(correctedc)>25:
                    correctedc=correctedc[:-1]
                self.varsNumC.set(correctedc)#Correct age with numerics only is set
                messagebox.showinfo('Warning!','You can select only between 10 and 25')
        if not self.varsNumM.get().isnumeric():
            correctedm = ''.join(filter(str.isnumeric,self.varsNumM.get()))#only numeric data can be written as the columns can only be numeric
            self.varsNumM.set(correctedm)#Correct  with numerics only is set
        if self.varsNumM.get()!='':
            if int(self.varsNumM.get())>25:
                correctedm = ''.join(filter(str.isnumeric,self.varsNumM.get()))#only numeric data can be written as the rows can only be numeric
                while int(correctedm)>25:
                    correctedm=correctedm[:-1]
                self.varsNumM.set(correctedm)#Correct age with numerics only is set
                messagebox.showinfo('Warning!','You can select only between 10 and 25')
    
    def bind_difficulty_widgets(self, view_type: str):
        """Binds difficulty buttons."""

    
        def closure_helper(f, difficulty, view_type):
                def g(f,difficulty,view_type): 
                    #print(difficulty,'in')
                    f(difficulty, view_type)                    
                return g(f,difficulty,view_type)
        self.difficulty_widgets[1].bind(
                "<Button-1>", lambda x:closure_helper(self.init_game,self.difficulty[1- 1], view_type))
        self.difficulty_widgets[2].bind(
                "<Button-1>", lambda x:closure_helper(
                self.init_game,self.difficulty[2- 1], view_type))
        self.difficulty_widgets[3].bind(
                "<Button-1>", lambda x:closure_helper(
                self.init_game,self.difficulty[3- 1], view_type))


    def init_game(self, difficulty: str='Easy', view_type: str='TEXT Game'):
        """Begins game."""

        self.root.destroy()
        print(difficulty)
        if view_type!='TEXT Game':
            r,c,m=int(self.varsNumR.get()),int(self.varsNumC.get()),int(self.varsNumM.get())#,
            t=self.typV.get()
            return Controller(*{
                            'E': (r, c, m, difficulty, view_type,t),
                            'M': (r, c, m, difficulty, view_type,t),
                            'H': (r, c, m, difficulty, view_type,t)
                            }[difficulty[0]])

        else:
            r,c,m,t=10,10,10,'Player vs Computer'
        
            return Controller(*{
                                'E': (r, c, m, difficulty, view_type,t),
                                'M': (r, c, m, difficulty, view_type,t),
                                'H': (r, c, m, difficulty, view_type,t)
                                }[difficulty[0]])


if __name__ == "__main__":
    game = InitializeGame() 
