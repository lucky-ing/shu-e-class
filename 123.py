
import re,os,time
from tkinter import *
import tkinter.messagebox as tkmessagebox
from selenium import webdriver
import threading
from bs4 import BeautifulSoup
#print(os.getcwd())
class shuclass(object):
    def __init__(self,master):
        self.master=master
        self.loginframe=LabelFrame(self.master,width=60,text='login')
        self.loginframe.grid(row=0,column=0,rowspan=4,columnspan=4)
        self.id_label=Label(self.loginframe,text='学号',width=10)
        self.id_label.grid(row=0,column=0,columnspan=1)
        self.id=Text(self.loginframe,width=20,height=1)
        self.id.grid(row=0, column=2,columnspan=3)
        self.pwd_label = Label(self.loginframe, text='密码', width=10)
        self.pwd_label.grid(row=1, column=0, columnspan=1)
        self.pwd = Text(self.loginframe, width=20,height=1)
        self.pwd.grid(row=1, column=2, columnspan=3)
        Label(self.loginframe,width=5,text='浏览器：').grid(row=2,column=0,columnspan=2)
        self.browserlist = ['Firefox', 'Edge']
        self.browserVar = StringVar(value=self.browserlist)
        self.browserVar.set('Firefox')
        self.browsermenu = OptionMenu(self.loginframe, self.browserVar, *self.browserlist)
        self.browsermenu.config(width=7)
        self.browsermenu.grid(row=2, column=2, columnspan=2)
        Label(self.loginframe,width=8,text='时长：').grid(row=3, column=0, columnspan=2)
        self.timemax=Text(self.loginframe,width=6,height=1)
        self.timemax.grid(row=3, column=2, columnspan=1)
        self.timemax.insert(END,'120')
        Label(self.loginframe, width=8, text='分钟').grid(row=3, column=3, columnspan=1)


        self.time_lable=Label(self.master,width=16,text='本次登录的时间为：',justify=CENTER)
        self.time_lable.grid(row=4,column=0,columnspan=2)
        self.time=Label(self.master,width=4,text='0')
        self.time.grid(row=4, column=2, columnspan=1)
        self.start=Button(self.master,width=10,text='开始',command=self.start)
        self.start.grid(row=5,column=0,columnspan=2)
        self.close=Button(self.master,width=10,text='结束',command=self.close)
        self.close.grid(row=5,column=2,columnspan=2)
        self.clock=threading.Event()
        self.clock.clear()
        self.p = threading.Thread(target=self.refresh, args=())

    def start(self):
        self.clock.set()
        self.p = threading.Thread(target=self.refresh, args=())
        self.p.start()
    def refresh(self):
        self.time_limit=0
        self.time_limit=int(self.timemax.get(0.0,END))
        if self.browserVar.get()=='edge':
            self.drive=webdriver.Edge()
        else:
            if self.browserVar.get() == 'Firefox':
                self.drive = webdriver.Firefox()
        try:
            self.drive.get('http://202.121.199.138/CSCI')
            time.sleep(1)
            self.drive.get('http://202.121.199.138/Course/login.asp?type=1')
            time.sleep(1)
        except:
            tkmessagebox.showerror('browser error!', 'we cannot open the browser ,please make sure you have choose the right browser!')
            return
        if self.drive.find_element_by_name('id'):
            id=self.drive.find_element_by_name('id')
            id.clear()
            id_num=self.id.get(0.0,END)
            pwd_num=self.pwd.get(0.0,END)
            #print(id_num)
            #print(pwd_num)
            id.send_keys(id_num)
            pwd =self.drive.find_element_by_name('pwd')
            pwd.clear()
            pwd.send_keys(pwd_num)
            search=self.drive.find_element_by_name('enter')
            search.click()
        else:
            print('error!')
        #print('12222222222222222222')
        time.sleep(2)

        try:
            self.drive.switch_to_frame('carnoc')
        except :
            tkmessagebox.showerror('open error!','we cannot open this page ,please make sure your password is right!')
            return
        talk=self.drive.find_element_by_link_text("进入讨论区")
        talk.click()
        p=0
        time.sleep(1)
        self.drive.switch_to_default_content()
        self.drive.switch_to_frame('main')
        print(self.clock.is_set())
        while True and self.clock.is_set()==True:
            time.sleep(2)
            lists=self.drive.find_element_by_class_name('list')
            list0=lists.find_element_by_class_name('listtitle')
            title=list0.find_elements_by_tag_name('a')[1]
            title.click()
            time.sleep(1)
            if self.drive.find_element_by_link_text('[2]'):
                next=self.drive.find_element_by_link_text('[2]')
                next.click()
            time.sleep(1)
            back=self.drive.find_element_by_link_text('讨论区首页')
            back.click()
            time.sleep(1)
            p+=1
            if p%2==0:
                self.drive.switch_to_default_content()
                self.drive.switch_to_frame('carnoc')
                self.time_num=self.drive.find_element_by_id('TimeInfo')
                print(self.time_num.text)
                time_0=int(self.time_num.text)
                self.time['text']=str(self.time_num.text)
                self.drive.switch_to_default_content()
                self.drive.switch_to_frame('main')
                p=0
                if time_0>self.time_limit:
                    break

        self.drive.close()
    def close(self):
        self.clock.clear()
        if self.p.is_alive()==True:
            self.clock.clear()
            time.sleep(2)
        self.master.quit()
if __name__=='__main__':
    master =Tk()
    aa=shuclass(master)
    mainloop()