from tkinter import *

class creatorGUI:
    def __init__(self):
        self.root = Tk()
        self.canvas = None
        self.cell = None
        self.resizeGUI(1200,900)
        self.root.mainloop()
    def resizeGUI(self,w,h):
        self.root.geometry(str(w)+"x"+str(h))
        if self.canvas!=None:
            self.canvas.pack_forget()
        self.canvas = Canvas(self.root,width=w,height=h,bg='white')
        self.canvas.bind("<ButtonPress-1>",self.b1down)
        
        c = self.canvas
        c.create_rectangle(0,0,w-300,h,fill='gray')
        for i in range(50,w-300,50):
            c.create_line((i,0,i,h))
        for i in range(50,h,50):
            c.create_line((0,i,w-300,i))
        self.cell = []
        for i in range(0,w-300,50):
            for j in range(0,h,50):
                self.cell.append((i,j,i+50,j+50))

        l = (w-200,0,w-100,35)
        c.create_rectangle(l[0],l[1],l[2],l[3],fill='gray')
        c.create_text(int((l[0]+l[2])/2),int((l[1]+l[3])/2),text='Label')
        self.canvas.pack()
    def b1down(self,e):
        print(e.x,e.y)
        c = self.findCell(e.x,e.y)
        self.canvas.create_rectangle(c[0],c[1],c[2],c[3],fill='red')
    def findCell(self,x,y):
        for item in self.cell:
            if x>=item[0] and x<=item[2] and y>=item[1] and y<=item[3]:
                return item
        return None

root = creatorGUI()
