# -*- coding:utf-8 -*-
#Simple Cal
#######################

from Tkinter import *
import Tkinter   

from operator import add

def frame(root, side):
    w = Frame(root)
    w.pack(side=side, expand=YES, fill=BOTH)
    return w
#end of def

def button(root, side, text = None, textvariable= None, command=None):
    w = Button(root, text=text, textvariable=textvariable, command=command)
    w.pack(side=side, expand=YES, fill=BOTH)
    return w
#end of def

class cvsBoard(Frame):
    def __init__(self,cvsMap,map_nr):
        Frame.__init__(self)
        self.cvsMap = cvsMap
        self.map_nr = map_nr
        self.master.geometry('+500+300')    
        self.option_add('*Font', 'Courier 8 bold')
        self.pack(expand=YES, fill=BOTH)
        self.master.title('Board')
        self.master.iconname('board')
        
        display = StringVar()
        self.display = display
        Entry(self, relief=SUNKEN, textvariable=display).pack(side=TOP, expand=YES, fill=BOTH)
        self.btnTexts = []
        for i in xrange(cvsMap.h):
            rowF = frame(self,TOP)
            btnTextli = []
            for j in xrange(cvsMap.w):
                v = StringVar()
                v.set(self.getStr(i,j))
                btnTextli.append(v)
                btn = button(rowF,LEFT,textvariable = v)
                btn.bind('<ButtonRelease-1>',lambda e,i=i,j=j: self.setPos(i,j))
                btn.bind('<ButtonRelease-2>',lambda e,i=i,j=j: self.blockPos(i,j))
                btn.bind('<ButtonRelease-3>',lambda e,i=i,j=j: self.clearPos(i,j))
            self.btnTexts.append(btnTextli)
            #end of for
        #end of for
        
        ioF = frame(self,TOP)
        button(ioF, LEFT, text = 'Evaluate!', command = lambda display = display:self.getEva(display))
        button(ioF, LEFT, text = 'Reset!', command = self.Reset)
        button(ioF, LEFT, text = 'OutPut!', command = self.getResult)
    #end of def
    def getEva(self,display):
        from vs_astar import a_star
        from vs_astar import getPath
        havePath = False
        pathli = []
        for g in self.cvsMap.gli:
            for s in self.cvsMap.sli:
                r = a_star(s, g, cvsMap)
                if r == -1:
                    continue
                havePath = True
                pathli.append(getPath(r))
            # end of for
        # end of for
        if not havePath:
            display.set("ERROR: NO PATH")
        else:
            display.set(reduce(add, (len(x) for x in pathli)))
            # show the path on map
            for path in pathli:
                for pos in path:
                    self.btnTexts[pos[0]][pos[1]].set('  P  ')
            
    # end of def
    def Reset(self):
        for i in xrange(cvsMap.h):
            for j in xrange(cvsMap.w):
                self.btnTexts[i][j].set(self.getStr(i, j))
    def getStr(self,i,j):
        if self.cvsMap.mmap[i][j] == '0':
            return '     '
        if self.cvsMap.mmap[i][j] == 't':
            tower = cvsMap.tdict[(i,j)]
            return 't:'+str(tower.stren) + ',' + str(tower.t)
        if self.cvsMap.mmap[i][j] == 's':
            return 'sssss'
        if self.cvsMap.mmap[i][j] == 'g':
            return 'ggggg'
        if self.cvsMap.mmap[i][j] == '1':
            return 'X X X'
        else:
            return self.cvsMap.mmap[i][j]+'    '
    def blockPos(self,i,j):
        from solve import Tower 
        #print 'INFO:',i,j
        if self.cvsMap.mmap[i][j] == '0':
            cvsMap.addTower(Tower(i,j,0,0))
            self.btnTexts[i][j].set(self.getStr(i, j)) # reset string
        pass 
    def clearPos(self,i,j):
        if self.cvsMap.mmap[i][j] == 't':
            cvsMap.delTower(i,j)
            self.btnTexts[i][j].set(self.getStr(i, j)) # reset string
    def setPos(self,i,j):
        from solve import Tower 
        if self.cvsMap.mmap[i][j] == 't':
            cvsMap.delTower(i,j)
            self.btnTexts[i][j].set(self.getStr(i, j)) # reset string
        elif self.cvsMap.mmap[i][j] == '0':
            d = MyDialog(self,i,j)        # 生成对话框
            self.wait_window(d.top)       # 等待对话框结束
            try:
                #tkMessageBox.showinfo('Python','You input stren,t:\n' + d.get()) 
                inputs = d.get().split(',');
            except Exception:
                return
            cvsMap.addTower(Tower(i,
                                  j,
                                  int(inputs[0]),
                                  int(inputs[1])))
            self.btnTexts[i][j].set(self.getStr(i, j)) # reset string
        else:
            pass
        #end of if
    #end of def
    
    def getResult(self):
        #self.destroy()
        self.quit()
        print 'Here!'
        return cvsMap  # will it get here?
        pass
    #end of def
#end of class

class MyDialog:                                                                         # 定义对话框类
        def __init__(self, root,i,j):                                                   # 对话框初始化
                self.top = Tkinter.Toplevel(root)                                       # 生成Toplevel组件
                label = Tkinter.Label(self.top, text='Please Input tower for %d,%d'%(i,j))                    # 生成标签组件
                label.pack()
                self.entry = Tkinter.Entry(self.top)                                    # 生成文本框组件
                self.entry.pack()
                self.entry.focus()                                                      # 让文本框获得焦点
                btn = Tkinter.Button(self.top, text='Ok',                               # 生成按钮
                                        command=self.Ok)                                # 设置按钮事件处理函数
                self.top.bind('<Return>',lambda e:self.Ok(),'+')
                self.top.geometry('300x100+500+200')     
                btn.pack()
        def Ok(self):                                                                   # 定义按钮事件处理函数
                self.input = self.entry.get()                                           # 获取文本框中内容，保存为input
                self.top.destroy()                                                      # 销毁对话框
        def get(self):                                                                  # 返回在文本框输入的内容
                return self.input


if __name__ == '__main__':
    from solve import readMapInput
    s = int(raw_input())
    cvsMap,l = readMapInput()    
    cvsBoard(cvsMap,10).mainloop()