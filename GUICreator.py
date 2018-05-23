from tkinter import *

class Releaser:
    def __init__(self,items):
        print(items)
        self.level = 0
        self.body=[]
        self.output = 'demo.py'
        self.fd = open(self.output,'w')
        self.codelogic(items)
        self.codeblock(self.body)
    def write(self,line):
        self.fd.write(self.level*4*' ')
        self.fd.write(line)
        self.fd.write('\n')
    def close(self):
        self.fd.close()
    def codeblock(self,code):
        for item in code:
            if type(item)==type(''):
                self.write(item)
            else:
                self.level += 1
                self.codeblock(item)
                self.level -= 1
    def codelogic(self,items):
        #### import
        add = self.body.append
        add("from tkinter import *")
        add("from PIL import Image")
        add("")
        #### class GUI
        gui = []
        add("class GUI:")
        g = gui.append
        ## def__init__
        g("def __init__(self):")
        init = []
        t = init.append
        t("self.root = Tk()")
        # items
        for item in items:
            init += item[2].releaseList(item[0])
        t("self.root.mainloop()")
        g(init)# end init block
        add(gui)# end GUI block
        add("g = GUI()")
        
        
        

class Component:
    def __init__(self,canvas,t,location):
        self.type = t
        self.canvas = canvas
        self.loc = (int((location[0]+location[2])/2),int((location[1]+location[3])/2))
        self.vardict = {}
        self.infotext = ''
        self.textframe = None
        self.delim = '\n'
        self.releaseStrings = []
    def put(self,key,value):
        s = StringVar()
        s.set(value)
        self.vardict[key] = s
        self.resetInfotext(None)
    def resetInfotext(self,e):
        self.infotext = 'type:'+self.type+'\n'
        for key,value in self.vardict.items():
            self.infotext = self.infotext + key + ':' + value.get() + self.delim
        if self.textframe:
            self.canvas.delete(self.textframe)
        self.textframe = self.canvas.create_text(self.loc[0],self.loc[1],text=self.infotext)
    def modify(self,tk):
        f = Frame(tk,height=500)
        for k,v in self.vardict.items():
            Entry(f,textvariable=v).pack()
        b = Button(f,text='complete',command=f.place_forget)
        b.bind("<Button-1>",self.resetInfotext)
        b.pack()
        f.place(x=0,y=0)
        self.resetInfotext(None)

class LabelComp(Component):
    def __init__(self,canvas,location):
        Component.__init__(self,canvas,'Label',location)
        self.put('name','l')
        self.put('textvariable','t')
        self.put('text','zheshilabel')
        self.put('bg','white')
    def releaseList(self,location):
        res = []
        res.append('%s=StringVar()'%self.vardict['textvariable'].get())
        res.append('%s.set(\'%s\')'%(self.vardict['textvariable'].get(),self.vardict['text'].get()))
        l = location
        res.append('%s=Label(self.root,textvariable=%s,width=%s,height=%s,bg=\'%s\')'%(self.vardict['name'].get(),self.vardict['textvariable'].get(),round((l[2]-l[0])/10),round((l[3]-l[1])/20),self.vardict['bg'].get()))
        res.append('%s.place(x=%s,y=%s)'%(self.vardict['name'].get(),l[0],l[1]))
        return res

class EntryComp(Component):
    def __init__(self,canvas,location):
        Component.__init__(self,canvas,'Entry',location)
        self.put('name','e')
        self.put('textvariable','t')
        self.put('text','zheshientry')
    def releaseList(self):
        res = []
        res.append('%s=StringVar()'%self.vardict['textvariable'].get())
        res.append('%s.set(\'%s\')'%(self.vardict['textvariable'].get(),self.vardict['text'].get()))
        res.append('%s=Label(self.root,textvariable=%s)'%(self.vardict['name'].get(),self.vardict['textvariable'].get()))
        return res
        

class creatorGUI:
    def __init__(self):
        self.root = Tk()
        self.canvas = None
        self.cell = []
        self.component = []
        self.item = []
        self.leftdown = None
        self.rightdown = None
        self.resizeGUI(1200,900)
        self.root.mainloop()
    def resizeGUI(self,w,h):
        self.root.geometry(str(w)+"x"+str(h))
        if self.canvas!=None:
            self.canvas.pack_forget()
        self.canvas = Canvas(self.root,width=w,height=h,bg='white')
        self.canvas.bind("<ButtonPress-1>",self.b1down)
        self.canvas.bind("<ButtonRelease-1>",self.b1up)
        self.canvas.bind("<Button-2>",self.b2)
        self.canvas.bind("<ButtonPress-3>",self.b3down)
        self.canvas.bind("<ButtonRelease-3>",self.b3up)
        
        c = self.canvas
        c.create_rectangle(0,0,w-300,h,fill='gray')
        for i in range(25,w-300,25):
            c.create_line((i,0,i,h))
        for i in range(25,h,25):
            c.create_line((0,i,w-300,i))
        self.cell = []
        for i in range(0,w-300,25):
            for j in range(0,h,25):
                self.cell.append((i,j,i+25,j+25))

        # label component
        lc = (w-200,0,w-100,35)
        c.create_rectangle(lc[0],lc[1],lc[2],lc[3],fill='gray')
        c.create_text(int((lc[0]+lc[2])/2),int((lc[1]+lc[3])/2),text='Label')
        self.component.append([lc,'label'])
        # entry component
        ec = (w-200,50,w-100,85)
        c.create_rectangle(ec[0],ec[1],ec[2],ec[3],fill='gray')
        c.create_text(int((ec[0]+ec[2])/2),int((ec[1]+ec[3])/2),text='Entry')
        self.component.append([ec,'entry'])
        # button component
        bc = (w-200,100,w-100,135)
        c.create_rectangle(bc[0],bc[1],bc[2],bc[3],fill='gray')
        c.create_text(int((bc[0]+bc[2])/2),int((bc[1]+bc[3])/2),text='Button')
        self.component.append([bc,'button'])
        # picture component
        pc = (w-200,150,w-100,185)
        c.create_rectangle(pc[0],pc[1],pc[2],pc[3],fill='gray')
        c.create_text(int((pc[0]+pc[2])/2),int((pc[1]+pc[3])/2),text='Picture')
        self.component.append([pc,'picture'])

        #release button
        rbc = Button(self.root,width=10,height=3,text='release',command=self.release)
        
        self.canvas.pack()
        rbc.place(x=w-200,y=h-500)
    def release(self):
        r = Releaser(self.item)
        r.close()
##        for item in self.item:
##            if len(item)==3:
##                print(item[2].releaseList())
    def b1down(self,e):
        c = self.findComponent(e.x,e.y)
        if c>=0:
            self.leftdown = ['component',c]
            return
        c = self.findItem(e.x,e.y)
        if c>=0:
            self.leftdown = ['item',c]
            return
        c = self.findCell(e.x,e.y)
        if c:
            self.leftdown = ['cell',c]
            return
        self.leftdown = None
        return
    def b1up(self,e):
        down = self.leftdown
        up = None
        if self.findComponent(e.x,e.y)>=0:
            up = ['component',self.findComponent(e.x,e.y)]
        elif self.findItem(e.x,e.y)>=0:
            up = ['item',self.findItem(e.x,e.y)]
        elif self.findCell(e.x,e.y):
            up = ['cell',self.findCell(e.x,e.y)]
        else:
            up = None

        # none
        if down==None or up==None:
            print('none')
            return
        
        # click
        if down==up:
            print('click')
            if down[0]=='item':
                if len(self.item[down[1]])==3:
                    self.item[down[1]][2].modify(self.root)

        # component -> item
        com_type = ['label','entry','button','picture']
        if down[0]=='component' and up[0]=='item':
            i = up[1]
            if len(self.item[i])==3:
                print('component existed')
            else:
                if down[1]==0:
                    cmp = LabelComp(self.canvas,self.item[up[1]][0])
                else:
                    cmp = Component(self.canvas,str(com_type[down[1]]),self.item[up[1]][0])
                    cmp.put('text','zheshiyiduanwenzi')
                    cmp.put('fill','red')
                self.item[i].append(cmp)
                self.canvas.itemconfig(self.item[i][1],fill='pink')
            
        print(down,'->',up)
        
##        c = self.findCell(e.x,e.y)
##        if c:
##            self.canvas.create_rectangle(c[0],c[1],c[2],c[3],fill='blue')
    def b2(self,e):
        i = self.findItem(e.x,e.y)
        if i>=0:
            if len(self.item[i])==3:
                self.canvas.delete(self.item[i][2].textframe)
            self.canvas.delete(self.item[i][1])
            del self.item[i]  
    def b3down(self,e):
        self.rightdown = self.findCell(e.x,e.y)
    def b3up(self,e):
        c1 = self.rightdown
        c2 = self.findCell(e.x,e.y)
        x1 = min([c1[0],c1[2],c2[0],c2[2]])
        y1 = min([c1[1],c1[3],c2[1],c2[3]])
        x2 = max([c1[0],c1[2],c2[0],c2[2]])
        y2 = max([c1[1],c1[3],c2[1],c2[3]])
        it = self.canvas.create_rectangle(x1,y1,x2,y2,fill='white')
        self.item.append([(x1,y1,x2,y2),it])
    def findComponent(self,x,y):
        for i in range(len(self.component)):
            if x>=self.component[i][0][0] and x<=self.component[i][0][2] and y>=self.component[i][0][1] and y<=self.component[i][0][3]:
                return i
        return -1
    def findItem(self,x,y):
        for i in range(len(self.item)):
            if x>=self.item[i][0][0] and x<=self.item[i][0][2] and y>=self.item[i][0][1] and y<=self.item[i][0][3]:
                return i
        return -1
    def findCell(self,x,y):
        for item in self.cell:
            if x>=item[0] and x<=item[2] and y>=item[1] and y<=item[3]:
                return item
        return None


root = creatorGUI()
