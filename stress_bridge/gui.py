import time
from tkinter import *

class Application(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.pile1 = Label(self.master)
        self.pile1.place(x=750,y=200)
        self.pile2 = Label(self.master)
        self.pile2.place(x=600,y=200)
        self.photos = {}
        self.hand = []
        self.selected = None
        for value in range(1,14):
            for suit in ["c","d","h","s"]:
                name = str(value)+suit
                p = PhotoImage(file=f"res/{name}.png").subsample(5)
                self.photos[name] = p
                
       

    def displayPileCards(self,p1,p2):

        if len(p1) > 0:
            card1 = p1[-1]
            value1, suit1 =  card1["value"], card1["suit"]
            name1 = str(value1)+str(suit1)
            w1 = self.pile1
            p1 = self.photos[name1]
            w1.configure(image=p1)

        if len(p2) > 0:
            card2 = p2[-1]
            value2, suit2 =  card2["value"], card2["suit"]
            name2 = str(value2)+str(suit2)
            w2 = self.pile2
            p2 = self.photos[name2]
            w2.configure(image=p2)


    def displayHand(self, cards):

        for l in self.hand:
            l.destroy()

        self.hand = []

        x = 300
        dx = 70
        y = 600

        for card in cards:
            name = str(card["value"])+card["suit"]
            img = self.photos[name]
            label = Label(self.master,image=img)
            label.place(x=x,y=y)
            label.bind("<Enter>",self.enter)
            label.bind("<Button-1>",self.click)
            label.bind("<Leave>",self.leave)
            self.hand.append(label)
            x += dx
  
    
    def enter(self,event):
        y = int(event.widget.place_info()["y"])
        event.widget.place(y=y-35)

    def click(self,event):
        self.selected = self.hand.index(event.widget)

    def leave(self,event):
        y = int(event.widget.place_info()["y"])
        event.widget.place(y=y+35)

'''
    
if __name__ == '__main__':
    root = Tk()
    root.geometry("1920x1080+0+0")
    app = Application(master=root)
    cards = []
    app.displayHand(cards)
    app.mainloop()

'''


