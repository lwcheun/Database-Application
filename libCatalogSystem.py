##########################################################################################
#
#						CS631 - Data Management Systems Design
#
#					Group 2: Michael Lan, Leon Cheung, Zhenbo Qiao
#
##########################################################################################

##########################################################
#import tkinter as tk                # python 3
#from tkinter import font  as tkfont # python 3
from Tkinter import *
import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
import pdb, traceback, sys
import os
#from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)
import datetime
from datetime import date, timedelta, time
from datetime import datetime as dt 

#create method Conn inside each class and call every time use sql (b/c need to close conn when a single sql
#stm is done)

#create super dict w/ rows (each row is a category like Branch or Reader) and each row holds items for that
#category (IE Branch holds branch_id, etc.). pass superdict to each frame when init it?
#no- either destroy and recreate frame, or call method when viewing it to reset it and use new login accnt's info

#can't call changed self.reader_id from libraryapp or startpage b/c when readermenu init, only the init reader_id
#and the methods are passed into readermenu, so when readermenu calls self.controller, it's calling that init instance
#not the changed one! 

class LibraryApp(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
    self.title("Library System")
    #stack frames in container, raise frame when viewing
    self.container = tk.Frame(self)  
    self.container.pack(side="top", fill="both", expand=True)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)
    #self.geometry("1500x700")
    self.attributes("-fullscreen", True)

    self.frames = {}  #store frames in dict. key is page_name
    for F in (StartPage, ReaderMenu, AdminMenu):
        page_name = F.__name__
        frame = F(parent=self.container, controller=self)
        self.frames[page_name] = frame  # stack frames
        frame.grid(row=0, column=0, sticky="nsew")

    self.show_frame("StartPage")

    menubar = tk.Menu(self)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=self.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    self.config(menu=menubar)

  def get_page(self, page_class):
    return self.frames[page_class]

  def show_frame(self, page_name):
    frame = self.frames[page_name]
    frame.tkraise()  #display frame by raising it to the top
    frame.event_generate("<<ShowFrame>>")

  def dbConnect(self, sql_input, query_type):
    try:
      cnn = connection.MySQLConnection(  #connection isn't class within LibApp, so don't do self.connection
      user='root', 
      password='', 
      host='localhost', 
      database='CS631_Project')     
    except mysql.connector.Error as e:
      if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access Denied")
      else:
        print(e)  
    #cannot return cursor b/c: ReferenceError: weakly-referenced object no longer exists
    #either return cursor.fetchall() results using sql_input as param or return cursor, cnn
    #but insert uses cursor .
    if query_type == "fetch":
      cursor = cnn.cursor()  
      cursor.execute(sql_input)
      result = cursor.fetchall() 
      cursor.close()
      return result
    elif query_type == "commit":
      cursor = cnn.cursor()  
      cursor.execute(sql_input)
      cnn.commit()  #cnn is database, cursor is query
      cursor.close()
  

class StartPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    label = tk.Label(self, text="This is the start page", font=controller.title_font)
    self.widgets()
    self.reader_id = ''

  def widgets(self):
    Label(self, text='Admin Login').grid(row=0,column=0, pady=(100,0),padx=(100,0))
    Label(self, text='User ID:').grid(row=1,column=0, pady=(100,0),padx=(100,0))
    Label(self, text='Password:').grid(row=2,column=0,padx=(100,0))
    self.admin_input = Entry(self, textvariable=StringVar())
    self.admin_input.grid(row=1,column=1, pady=(100,0),padx=(100,200))
    self.passwd_input = Entry(self, show='*', textvariable=StringVar())
    self.passwd_input.grid(row=2,column=1,padx=(100,200))
    Button(self, text='Login', command = self.admin_login).grid(row=3,column=1,padx=(100,200))

    Label(self, text='Reader Login - Enter Card Number (ReaderID)').grid(row=0,column=2, pady=(100,0),padx=(100,0))
    Label(self, text='Card Number:').grid(row=1,column=2, pady=(100,0))
    self.cardnum_input = Entry(self, textvariable=StringVar())
    self.cardnum_input.grid(row=1,column=3, pady=(100,0))
    Button(self, text='Login', command = self.reader_login).grid(row=2,column=3, pady = (20,0))

    self.wrong_login = Listbox(self,height=2,width=20)
    self.wrong_login.grid(row=4,column=1,padx=(100,200),pady=30)

    self.wrong_login_reader = Listbox(self,height=2,width=20)
    self.wrong_login_reader.grid(row=3,column=3, pady=(30,0))

    """
    cwd = os.getcwd() 
    img = ImageTk.PhotoImage(Image.open(cwd + '\\' + "a.jpg"))
    panel = Label(self)
    panel.image = img #anchor
    panel.configure(image=img)  #REQUIRED, OR ELSE IMAGE WON'T SHOW UP
    panel.grid(row = 4, column = 3)
    """
  def admin_login(self):
    sql_input = "SELECT * FROM ADMIN WHERE ID = '%s' AND PASSWARD = '%s'" % (self.admin_input.get(), self.passwd_input.get())
    self.admin_arr = self.controller.dbConnect(sql_input, 'fetch')
    #from ADMIN select ADMIN_ID, PASSWD WHERE ADMIN_ID = admin_input.get()
    #if admin_input.get() is a tuple in relation 'admin' AND passwd is that tuple's passwd
    if self.admin_arr == []:
        self.wrong_login.delete(0,END)
        self.wrong_login.insert(END, "Invalid Login")
    else:
        self.wrong_login.delete(0,END)
        self.wrong_login_reader.delete(0,END)
        self.admin_input.delete(0,END)
        self.passwd_input.delete(0,END)
        self.cardnum_input.delete(0,END)
        self.controller.show_frame("AdminMenu")

  def reader_login(self):
    sql_input = "SELECT * FROM READER WHERE READERID = '%s'" % (self.cardnum_input.get())
    self.readerid_arr = self.controller.dbConnect(sql_input, 'fetch')
    if self.readerid_arr == []:
      self.wrong_login_reader.delete(0,END)
      self.wrong_login_reader.insert(END, "Invalid Login")
    else:
      self.reader_id = self.cardnum_input.get()  #cardnum_input.get() becomes ReaderID (used for reserve and borrow)
      self.wrong_login.delete(0,END)
      self.wrong_login_reader.delete(0,END)
      self.admin_input.delete(0,END)
      self.passwd_input.delete(0,END)
      self.cardnum_input.delete(0,END)
      self.controller.show_frame("ReaderMenu") 

  def get_reader_id(self):
    return self.reader_id            


class ReaderMenu(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.res_arr = [('Cliffordssssssssssssssssssssssssssss', str(i)) for i in range(11)]
    self.borr_arr = [('Cliffordssssssssssssssssssssssssssss', "12/1/17", "$10")]*11
    self.widgets()
    self.bind("<<ShowFrame>>", self.onShowFrame)
    self.cancel_id = '' 
    self.cancel_copy = '' 
    self.cancel_lib = '' 

  def onShowFrame(self, event):
    self.update_welcome_label() #b/c it's unchanged from init, but should change upon new login!
    self.update_print_reserved()
    self.update_print_borrowed()

  def update_welcome_label(self):
    self.wel.grid_forget()
    stpage = self.controller.get_page("StartPage")
    self.reader_id = stpage.get_reader_id()
    self.wel = Label( self, text="Welcome Reader %s" % self.reader_id)
    self.wel.grid(row=0, column = 1, pady = 20)

  def widgets(self):
    #print Reader info. reader can checkout from multiple branches
    stpage = self.controller.get_page("StartPage")
    self.wel = Label( self, text="Welcome Reader %s" % stpage.get_reader_id())
    self.wel.grid(row=0, column = 1, pady = 20)

    #display search results
    #padx to left for all widgets in col 0
    Label( self, text="Search Results").grid(row=1, column = 0, pady = 20)
    Label( self, text="Click Entry to Checkout").grid(row=1, column = 1, pady = 20, sticky=W)
    Label( self, text="DocID    CopyNo    LibID").grid(row=2, column = 0, padx=(20,0), sticky=W)  
    Label( self, text="Doc Title").grid(row=2, column = 1)
    Label( self, text="Publisher").grid(row=2, column = 2)
    Label( self, text="Status").grid(row=2, column = 3, sticky=E)
    self.search_display = Listbox(self, height = 10, width=76)  #MUST separate declare and .grid in 2 lines
    self.search_display.grid(row=3, column = 0, padx=(20,0), columnspan=4)
    scrollbar1 = Scrollbar(self)
    scrollbar1.grid(row=3, column=4, sticky=(N,S,W)) 
    self.search_display.configure(yscrollcommand=scrollbar1.set)   
    scrollbar1.configure(command=self.search_display.yview)

    scrollbar1b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar1b.grid(row=4, column=0, sticky=(N,E,W), padx=(20,0), columnspan=4)
    self.search_display.configure(xscrollcommand=scrollbar1b.set)  
    scrollbar1b.configure(command=self.search_display.xview)

    self.search_display.bind("<<ListboxSelect>>", self.searchresults_Selected)

    #User Query Goes Below
    Label( self, text="Enter Search Below").grid(row=4, column = 1, pady=(30,30), sticky = S)
    Label( self, text="Search by Doc ID").grid(row=5, column = 0, sticky = N)
    Label( self, text="Search by Title").grid(row=6, column = 0, sticky = N)
    Label( self, text="Search by Publisher").grid(row=7, column = 0, sticky = N)
    self.id_search = Entry(self, bd = 5)
    self.id_search.grid(row=5, column = 1, pady=(0,20)) 
    self.title_search = Entry(self, bd = 5)
    self.title_search.grid(row=6, column = 1, pady=(0,20))  
    self.pub_search = Entry(self, bd = 5)
    self.pub_search.grid(row=7, column = 1, pady=(0,20))  
    Button(self, text ="Search", command = self.print_search).grid(row=5, column = 2, sticky = N)
    Button(self, text ="View All", command = self.view_all).grid(row=6, column = 2, sticky = N)

    #checkout (borrow)
    tk.Label( self, text="Enter Doc ID").grid(row=8, column = 0, padx=(20, 0), pady=(30,10))
    tk.Label( self, text="Enter Copy No").grid(row=8, column = 1, pady=(30,10))
    tk.Label( self, text="Enter Lib ID").grid(row=8, column = 2, pady=(30,10))
    self.borr_id_entryText = tk.StringVar()
    self.borr_id_entry = tk.Entry(self, bd = 5, textvariable=self.borr_id_entryText)
    self.borr_id_entry.grid(row=9, column = 0, padx=(20, 0))
    self.borr_copy_entryText = tk.StringVar()
    self.borr_copy_entry = tk.Entry(self, bd = 5, textvariable=self.borr_copy_entryText)
    self.borr_copy_entry.grid(row=9, column = 1)
    self.borr_lib_entryText = tk.StringVar()
    self.borr_lib_entry = tk.Entry(self, bd = 5, textvariable=self.borr_lib_entryText)  
    self.borr_lib_entry.grid(row=9, column = 2)
    tk.Button(self, text ="Checkout", command = self.checkout).grid(row=9, column = 3, sticky = "WN")

    #display reserved documents
    tk.Label( self, text="Click in Search Results to Reserve").grid(row=1, column = 5, pady = 20, sticky=W)
    tk.Label( self, text="Doc Info").grid(row=2, column = 4, padx=(90, 0))
    tk.Label( self, text="Status").grid(row=2, column = 5, sticky=E)
    self.show_res = tk.Listbox(self, height = 10, width = 50)
    self.show_res.grid(row=3, column = 4, columnspan = 2, padx=(90, 0))
    scrollbar2 = Scrollbar(self)
    scrollbar2.grid(row=3, column=6, sticky=(N,S,W)) #can't do padx on scrollbar, so do it on left of new listbox
    self.show_res.configure(yscrollcommand=scrollbar2.set)   #apply scrollbar to listbox
    scrollbar2.configure(command=self.show_res.yview)

    scrollbar2b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar2b.grid(row=4, column=4, sticky=(N,E,W), padx=(90,0), columnspan=2)
    self.show_res.configure(xscrollcommand=scrollbar2b.set)  
    scrollbar2b.configure(command=self.show_res.xview)

    self.show_res.bind("<<ListboxSelect>>", self.res_selected)

    #reserve
    tk.Label(self, text="Enter Doc ID").grid(row=5, column = 4, pady=(0,20), sticky=E)
    tk.Label(self, text="Enter CopyNo").grid(row=6, column = 4, pady=(0,20), sticky=E)
    tk.Label(self, text="Enter LibID").grid(row=7, column = 4, pady=(0,20), sticky=E)
    self.res_id_entryText = tk.StringVar()
    self.res_id_entry = tk.Entry(self, bd = 5, textvariable=self.res_id_entryText)
    self.res_id_entry.grid(row=5, column = 5, pady=(0,20))  
    self.res_copy_entryText = tk.StringVar()
    self.res_copy_entry = tk.Entry(self, bd = 5, textvariable=self.res_copy_entryText)
    self.res_copy_entry.grid(row=6, column = 5, pady=(0,20)) 
    self.res_lib_entryText = tk.StringVar() 
    self.res_lib_entry = tk.Entry(self, bd = 5, textvariable=self.res_lib_entryText)
    self.res_lib_entry.grid(row=7, column = 5, pady=(0,20))  
    tk.Button(self, text ="Reserve", command = self.reserve).grid(row=8, column = 5,sticky=N)
    tk.Button(self, text ="Cancel Reservation", command = self.cancel_res).grid(row=9, column = 5,sticky=N)

    #display borrowed documents
    tk.Label( self, text="Click Entry Below to Return").grid(row=1, column = 7, pady = 20)
    tk.Label( self, text="Title").grid(row=2, column = 6, padx=(90, 0))
    tk.Label( self, text="Return Date").grid(row=2, column = 7)
    tk.Label( self, text="Fine").grid(row=2, column = 8)
    self.show_borr = tk.Listbox(self, height = 10, width = 60)
    self.show_borr.grid(row=3, column = 6, columnspan = 3, padx=(90, 0))
    scrollbar3 = Scrollbar(self)
    scrollbar3.grid(row=3, column=9, sticky=(N,S,W)) 
    self.show_borr.configure(yscrollcommand=scrollbar3.set) 
    scrollbar3.configure(command=self.show_borr.yview)

    scrollbar3b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar3b.grid(row=4, column=6, sticky=(E,W,N), padx=(90,0), columnspan=3)
    self.show_borr.configure(xscrollcommand=scrollbar3b.set)  
    scrollbar3b.configure(command=self.show_borr.xview)

    self.show_borr.bind("<<ListboxSelect>>", self.ReturnSelected)

    #return book
    tk.Label(self, text="Enter Doc ID").grid(row=5, column = 6, pady=(0,20), sticky=E)
    tk.Label(self, text="Enter CopyNo").grid(row=6, column = 6, pady=(0,20), sticky=E)
    tk.Label(self, text="Enter LibID").grid(row=7, column = 6, pady=(0,20), sticky=E)
    self.return_id_entryText = tk.StringVar()
    self.return_id_entry = tk.Entry(self, bd = 5, textvariable=self.return_id_entryText)  
    self.return_id_entry.grid(row=5, column = 7, pady=(0,20))
    self.return_copy_entryText = tk.StringVar()
    self.return_copy_entry = tk.Entry(self, bd = 5, textvariable=self.return_copy_entryText)
    self.return_copy_entry.grid(row=6, column = 7, pady=(0,20))
    self.return_lib_entryText = tk.StringVar()  
    self.return_lib_entry = tk.Entry(self, bd = 5, textvariable=self.return_lib_entryText) 
    self.return_lib_entry.grid(row=7, column = 7, pady=(0,20))
    tk.Button(self, text ="Return", command = self.return_book).grid(row=8, column = 7,sticky=N)

    tk.Button(self, text="Logout",
      command=self.logout).grid(row=0, column=0)  #put it last after defining Listboxes

  def popup_window(self, displayed_text):
    win = Toplevel()
    win_width = len(displayed_text)+500
    win.geometry('%sx100' % win_width)  #width by height
    self.center_popup(win)

    l = Label(win, text=displayed_text)
    l.config(font=(45))
    l.grid(row=1, column=1, sticky=NSEW)

    b = Button(win, text="Okay", command=win.destroy, width=3, height=1)
    b.grid(row=2, column=1, sticky=NSEW, pady=20)

    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(3, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(2, weight=1)

  def center_popup(self, toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

  def print_search(self):
    self.search_display.delete(0, END)
    id_query = self.id_search.get()
    title_query = self.title_search.get()
    pub_query = self.pub_search.get()

    #instructions to Leon: use variables _query above in the WHERE of the SQL query
    #join document, copy, publisher and then select attributes 'docid, title, pubname'
    #to check status, check if (docid, copyno, libid) in reserves or borrow. if in neither, it's avail
    #obtain a list of tuples: REQUIRES sql tuple to be organized as 'docid, title, publisher, status' in SELECT
    #call this list of tuples 'search_results'

    #search docs from ALL DOCUMENTS, not the branch's copies

    #either create status attr (update whenever reserve, etc) OR:
    #check status: EXISTS (selected tuple) IN RESERVED  --> return string or bool 
    #if (inres = false and inborr = false) {status = AVAIL }
    #if (inres = true and inborr = false) {status = ONHOLD }
    #if (inres = false and inborr = true) {status = CHKEDOUT }

    if id_query != '' and title_query != '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND TITLE = '%s' AND PUBNAME ='%s'" % (id_query, title_query, pub_query)
    elif id_query == '' and title_query != '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE TITLE = '%s' AND PUBNAME ='%s'" % (title_query, pub_query)
    elif id_query != '' and title_query == '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND PUBNAME ='%s'" % (id_query, pub_query)
    elif id_query != '' and title_query != '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND TITLE = '%s'" % (id_query, title_query)
    elif id_query != '' and title_query == '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s'" % (id_query)
    elif id_query == '' and title_query != '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE TITLE = '%s'" % (title_query)
    elif id_query == '' and title_query == '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER  WHERE PUBNAME ='%s'" % (pub_query)
    else:
      self.popup_window("Enter a Valid Entry")
      return

    self.search_results = self.controller.dbConnect(sql_input, "fetch")
    if self.search_results == []:
      self.search_display.insert(END, "NO RESULTS FOUND")
      return

    for i in range(len(self.search_results)):
      doc_id = self.search_results[i][0]
      copyno = self.search_results[i][1]  
      libid = self.search_results[i][2]  
      doc_title = self.search_results[i][3]  
      doc_pub = self.search_results[i][4]  
      doc_status = self.search_results[i][5]  
      self.search_display.insert(i, "ID:  %s" % doc_id + ' '*10 + "CopyNo:  %s" % copyno + ' '*10 + 
        "LibID:  %s" % libid + ' '*20 + "Title:  %s" % doc_title + ' '*20 + 
        "Pub:  %s" % doc_pub +  ' '*20 + "Status:  %s \n" % doc_status )
      #cannot do "sdf %s" + ' ' + "xcv %s" % (x,y)

  def view_all(self):
    self.search_display.delete(0, END)
    sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER"
    self.search_results = self.controller.dbConnect(sql_input, "fetch")
    if self.search_results == []:
      self.search_display.insert(END, "NO RESULTS FOUND")
      return
    for i in range(len(self.search_results)):
      doc_id = self.search_results[i][0]
      copyno = self.search_results[i][1]  
      libid = self.search_results[i][2]  
      doc_title = self.search_results[i][3]  
      doc_pub = self.search_results[i][4]  
      doc_status = self.search_results[i][5]  
      self.search_display.insert(i, "ID:  %s" % doc_id + ' '*10 + "CopyNo:  %s" % copyno + ' '*10 + 
        "LibID:  %s" % libid + ' '*20 + "Title:  %s" % doc_title + ' '*20 + 
        "Pub:  %s" % doc_pub +  ' '*20 + "Status:  %s \n" % doc_status )

  def update_print_reserved(self):  
    #initial login: print currently reserved books for that readerid
    #after checkout: if book in reserved, remove from reserved reln table
    #after reserve: add book to reserved table
    #from reln RESERVES get all tuple w/ readerid, put tuples into res_arr
    sql_input = "SELECT TITLE, STATUS, DOCID, COPYNO, LIBID FROM DOCUMENT NATURAL JOIN RESERVES NATURAL JOIN COPY WHERE READERID ='%s'" % (self.reader_id)
    self.res_arr = self.controller.dbConnect(sql_input, "fetch")

    self.show_res.delete(0, END)
    if self.res_arr != []:
      for i in range(len(self.res_arr)):
        if ("%s" % self.res_arr[i][1]) == "Reserved":
          title = self.res_arr[i][0]
          status = self.res_arr[i][1]
          docid = self.res_arr[i][2]
          copyno = self.res_arr[i][3]
          libid = self.res_arr[i][4]
          self.show_res.insert(i, "Title:  %s" %title + ' '*20  
            + "Status:  %s" %status + ' '*20
            + "DocID:  %s" %docid + ' '*20 
            + "CopyNo:  %s" %copyno + ' '*20  
            + "LibID:  %s" %libid + ' '*20 + '\n' )

  def update_print_borrowed(self):  
    #initial login: print currently borrowed books for that readerid
    #after checkout: add book to borrowed reln table
    #after return: remove book from borrowed reln table
    #from reln BORROWS get all tuple w/ readerid, put tuples into borr_arr
    sql_input = "SELECT TITLE, BDATE, FINE, DOCID, COPYNO, LIBID FROM DOCUMENT NATURAL JOIN BORROWS NATURAL JOIN FINE NATURAL JOIN COPY WHERE READERID ='%s' AND RDATE<=>NULL" % (self.reader_id)
    self.borr_arr = self.controller.dbConnect(sql_input, "fetch")
  
    #borrows keeps track of ALL documents ever borrowed. it does not delete a tuple if it was returned
    #instead, it sets rdate to a not null val when it's returned
    if self.borr_arr != []:
      self.show_borr.delete(0, END)
      overdue_books = 0
      fine_total = 0
      for i in range(len(self.borr_arr)):
        #if self.borr_arr[i][6] == None:  #not returned yet
          #year = int(self.borr_arr[i][1][0:4])
          #month = int(self.borr_arr[i][1][5:7])
          #day = int(self.borr_arr[i][1][8::])
          #due_date = datetime.date(year,month,day) + datetime.timedelta(days=20)
        title = self.borr_arr[i][0]
        retDate = self.borr_arr[i][1]
        x = dt.strptime(retDate, '%Y-%m-%d').date() # converts to date format YYYY-MM-DD for manipulation
        due_date = x + datetime.timedelta(days=20)  # Adds 20 days to from date of borrow (BDATE)
        fine = self.borr_arr[i][2]
        todays_date = datetime.date.today()
        delta = todays_date - due_date    # Calculates the difference from Current date to Due date
        days_late = delta.days  # can be pos or neg | neg means not yet late

        docid = self.borr_arr[i][3]
        copyno = self.borr_arr[i][4]
        libid = self.borr_arr[i][5]
        if days_late > 0:   #if late then show fees 
          overdue_books += 1
          fine_calc = days_late * 0.20
          fine_total += fine_calc
          self.show_borr.insert(i, "Title:  %s" %title + ' '*20  + "Return By:  %s" %due_date 
            + ' '*20  + "Fine:  %s"  %fine_calc + ' '*20 
            + "DocID:  %s" %docid + ' '*20 
            + "CopyNo:  %s" %copyno + ' '*20  
            + "LibID:  %s" %libid + ' '*20 + '\n' )
        else:
          self.show_borr.insert(i, "Title:  %s" %title + ' '*20  + "Return By:  %s" %due_date 
            + ' '*20  + "Fine: 0" + ' '*20 
            + "DocID:  %s" %docid + ' '*20 
            + "CopyNo:  %s" %copyno + ' '*20  
            + "LibID:  %s" %libid + ' '*20 + '\n' )
    sql_input2 = "UPDATE FINE SET FINE='%s', OVERDUE='%s' WHERE READERID='%s'" % (fine_total, overdue_books, self.reader_id)
    self.controller.dbConnect(sql_input2, "commit")  

  #can only checkout if: 1) available, or 2) reserved by reader
  #if 2), then delete reader's reservation and insert tuple in borrows
  #integr constraints ALSO NEEDS TO PREVENT DUPLICATES IN KEY FIELD
  def searchresults_Selected(self, e):
    curr_sel_row = int(self.search_display.curselection()[0])
    selection = self.search_display.get(curr_sel_row).split()
    self.borr_id_entry.delete(0,END)
    self.borr_copy_entry.delete(0,END)
    self.borr_lib_entry.delete(0,END)
    self.borr_id_entryText.set(selection[1])
    self.borr_copy_entryText.set(selection[3])
    self.borr_lib_entryText.set(selection[5])
    self.res_id_entry.delete(0,END)
    self.res_copy_entry.delete(0,END)
    self.res_lib_entry.delete(0,END)
    self.res_id_entryText.set(selection[1])
    self.res_copy_entryText.set(selection[3])
    self.res_lib_entryText.set(selection[5])

  def res_selected(self, e):
    curr_sel_row = int(self.show_res.curselection()[0])
    selection = self.show_res.get(curr_sel_row).split()
    self.borr_id_entry.delete(0,END)
    self.borr_copy_entry.delete(0,END)
    self.borr_lib_entry.delete(0,END)
    self.borr_id_entryText.set(selection[-5])
    self.borr_copy_entryText.set(selection[-3])
    self.borr_lib_entryText.set(selection[-1])
    self.cancel_id = selection[-5]
    self.cancel_copy = selection[-3]
    self.cancel_lib = selection[-1]

  def checkout(self):
    self.check_cancel_time()
    sql_input = "SELECT * FROM BORROWS WHERE READERID = '%s'  AND RDATE<=>NULL" % self.reader_id
    #where rdate is not null to only obtain ones currently checked out (not returned yet)
    check_num_borr = self.controller.dbConnect(sql_input, 'fetch') 
    if len(check_num_borr) >= 10:
      self.popup_window("Cannot Borrow More: Max Limit of 10 Docs Reached")
      return  #no else actions, so can put this and return at front instead of nesting if-else
    new_id_entry = self.borr_id_entry.get() 
    new_copy_entry = self.borr_copy_entry.get() 
    new_lib_entry = self.borr_lib_entry.get() 
    today = datetime.date.today()   #current date for use at checkout; must import datetime 
    if new_id_entry != '' and new_copy_entry != '' and new_lib_entry != '': #check all fields filled in
        #check if a tuple with the 3 entered attributes exists in COPY
        sql_input1 = "SELECT * FROM COPY WHERE DOCID = '%s' AND COPYNO = '%s' AND LIBID = '%s'" % (new_id_entry, new_copy_entry, new_lib_entry)
        check_result = self.controller.dbConnect(sql_input1, 'fetch')
        if check_result != []:
          sql_input2 = "SELECT STATUS FROM COPY WHERE DOCID = '%s' AND COPYNO = '%s' AND LIBID = '%s'" % (new_id_entry, new_copy_entry, new_lib_entry)
          status_result = self.controller.dbConnect(sql_input2, 'fetch') 
          sql_input3 = "SELECT * FROM RESERVES WHERE READERID='%s' AND DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (self.reader_id, new_id_entry, new_copy_entry, new_lib_entry)
          reserve_result = self.controller.dbConnect(sql_input3, 'fetch')
          if (status_result[0][0] == "Reserved" and reserve_result != []):
            status_bool = True                 
          elif status_result[0][0] == "Available":  #[0][0] to get string from unicode in list
            status_bool = True #check if status is available in copy    
          else: status_bool = False
          if status_bool == True: #True is case sensitive
            #bornumber is auto increment in the DB, so it's integer. prevents duplicate entries in key field
            # Need to import datetime to get current date; RDATE is null until returned, so no input necessary
            sql_input4 = "INSERT INTO BORROWS (READERID, DOCID, COPYNO, LIBID, BDATE) VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.reader_id,  new_id_entry, new_copy_entry, new_lib_entry, today)
            self.controller.dbConnect(sql_input4, 'commit')
            sql_input5 = "SELECT FREQUENCY FROM COPY WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (new_id_entry, new_copy_entry, new_lib_entry)
            freq_result = self.controller.dbConnect(sql_input5, 'fetch')
            freq_borr = freq_result[0][0]
            sql_input6 = "UPDATE COPY SET STATUS='%s', FREQUENCY='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Borrowed", str(freq_borr+1), new_id_entry, new_copy_entry, new_lib_entry)
            self.controller.dbConnect(sql_input6, 'commit')
            if reserve_result != []:
              sql_input7 = "DELETE FROM RESERVES WHERE READERID='%s' AND DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (self.reader_id, new_id_entry, new_copy_entry, new_lib_entry)
              self.controller.dbConnect(sql_input7, 'commit')
            self.view_all()
            self.update_print_reserved()
            self.update_print_borrowed()
            self.popup_window("Successfully borrowed- See Search Results")
          else: #not avail
            self.popup_window("Not Available for Checkout")
        else:   #copy doesn't exist
          self.popup_window("Entry does not exist")
    else:   #not all fields filled in
      self.popup_window("Enter a Valid Entry") 

  def check_cancel_time(self):
    sql_input = "SELECT DTIME, RESNUMBER FROM RESERVES WHERE READERID = '%s'" % self.reader_id
    check_valid = self.controller.dbConnect(sql_input, 'fetch') 
    if dt.now().time() > time(18,0):  #if current time is greater than 6pm
      for tup_time in check_valid:
        #x = dt.strptime(tup_time[0][0:-1], '%Y-%m-%d %H:%M:%S')
        #threshold = dt.combine(dt.now().date(), time(18,0))
        get_date = tup_time[0].split()[0]
        tuple_date = dt.strptime(get_date, '%Y-%m-%d').date()
        if tuple_date < dt.now().date(): #checked out before current day
          #nat join to get resnum's corr tuple in copy before deleting!!!
          sql_get_copy = "SELECT FREQUENCY, DOCID, COPYNO, LIBID FROM COPY NATURAL JOIN RESERVES WHERE RESNUMBER='%s'" % (tup_time[1])
          copy_result = self.controller.dbConnect(sql_get_copy, 'fetch')
          sql_input_2 = "UPDATE COPY SET STATUS='%s', FREQUENCY='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Available", str(copy_result[0][0]), copy_result[0][1], copy_result[0][2], copy_result[0][3])
          self.controller.dbConnect(sql_input_2, 'commit')
          sql_input = "DELETE FROM RESERVES WHERE RESNUMBER = '%s'" % (tup_time[1])
          self.controller.dbConnect(sql_input, 'commit')
        else:  #checked out in current day
          get_time = tup_time[0].split()[1][0:-1]
          tuple_time = dt.strptime(get_time, '%H:%M:%S').time()
          if tuple_time < time(23,0):  #checked out before 6pm of current day
            #nat join to get resnum's corr tuple in copy before deleting!!!
            sql_get_copy = "SELECT FREQUENCY, DOCID, COPYNO, LIBID FROM COPY NATURAL JOIN RESERVES WHERE RESNUMBER='%s'" % (tup_time[1])
            copy_result = self.controller.dbConnect(sql_get_copy, 'fetch')
            sql_input_2 = "UPDATE COPY SET STATUS='%s', FREQUENCY='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Available", str(copy_result[0][0]), copy_result[0][1], copy_result[0][2], copy_result[0][3])
            self.controller.dbConnect(sql_input_2, 'commit')
            sql_input = "DELETE FROM RESERVES WHERE RESNUMBER = '%s'" % (tup_time[1])
            self.controller.dbConnect(sql_input, 'commit')
    self.view_all()
    self.update_print_reserved()

  #no way to un-reserve (not a requirement)
  def reserve(self):
    self.check_cancel_time()
    sql_input = "SELECT * FROM RESERVES WHERE READERID = '%s'" % self.reader_id
    check_valid = self.controller.dbConnect(sql_input, 'fetch') 
    if len(check_valid) >= 10:
      self.popup_window("Cannot Reserve More: Max Limit of 10 Docs Reached")
      return  
    new_id_entry = self.res_id_entry.get() 
    new_copy_entry = self.res_copy_entry.get() 
    new_lib_entry = self.res_lib_entry.get()
    currtime = datetime.datetime.now()     #import datetime
    if new_id_entry != '' and new_copy_entry != '' and new_lib_entry != '': #check all fields filled in
      sql_input1 = "SELECT * FROM COPY WHERE DOCID = '%s' AND COPYNO = '%s' AND LIBID = '%s'" % (new_id_entry, new_copy_entry, new_lib_entry)
      check_result = self.controller.dbConnect(sql_input1, 'fetch')
      if check_result != []:
        sql_input2 = "SELECT STATUS FROM COPY WHERE DOCID = '%s' AND COPYNO = '%s' AND LIBID = '%s'" % (new_id_entry, new_copy_entry, new_lib_entry)
        status_result = self.controller.dbConnect(sql_input2, 'fetch') 
        if status_result[0][0] == "Available":  #[0][0] to get string from unicode in list
          #resnumber is auto increment in the DB, so it's integer. prevents duplicate entries in key field
          sql_input3 = "INSERT INTO RESERVES (READERID, DOCID, COPYNO, LIBID, DTIME) VALUES ('%s', '%s', '%s', '%s', '%s')" %(self.reader_id,  new_id_entry, new_copy_entry, new_lib_entry, currtime)
          self.controller.dbConnect(sql_input3, 'commit') 
          sql_input4 = "UPDATE COPY SET STATUS='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Reserved", new_id_entry, new_copy_entry, new_lib_entry)
          self.controller.dbConnect(sql_input4, 'commit')  #change copy status to 'reserved'
          self.view_all()
          self.update_print_reserved()
          self.popup_window("Successfully reserved- See Search Results")  
        else:  #not avail
            self.popup_window("Not Available for Reserve")      
      else:   #copy doesn't exist
        self.popup_window("Entry does not exist")
    else:   #not all fields filled in
      self.popup_window("Enter a Valid Entry")  

  def cancel_res(self):
    if self.cancel_id != '' and self.cancel_copy != '' and self.cancel_lib != '':
      sql_input = "DELETE FROM RESERVES WHERE READERID='%s' AND DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (self.reader_id, self.cancel_id, self.cancel_copy, self.cancel_lib)
      self.controller.dbConnect(sql_input, 'commit')

      sql_input_freq = "SELECT FREQUENCY FROM COPY WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (self.cancel_id, self.cancel_copy, self.cancel_lib)
      freq_result = self.controller.dbConnect(sql_input_freq, 'fetch')
      freq_borr = freq_result[0][0]

      sql_input_2 = "UPDATE COPY SET STATUS='%s', FREQUENCY='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Available", str(freq_borr), self.cancel_id, self.cancel_copy, self.cancel_lib)
      self.controller.dbConnect(sql_input_2, 'commit')
      self.update_print_reserved()
      self.cancel_id = ''  #not sel anymore so set vars to 0
      self.cancel_copy = '' 
      self.cancel_lib != ''
      self.popup_window("Successfully cancelled- See Search Results")
    else:
      self.popup_window("Select Entry from Reserve to Cancel")
  
  #change book's status from 'checkedout' to 'avail' in COPIES
  #delete book from BORROWS table
  def ReturnSelected(self, e):
    curr_sel_row = int(self.show_borr.curselection()[0])
    selection = self.show_borr.get(curr_sel_row).split()
    self.return_id_entry.delete(0,END)
    self.return_copy_entry.delete(0,END)
    self.return_lib_entry.delete(0,END)
    self.return_id_entryText.set(selection[-5])
    self.return_copy_entryText.set(selection[-3])
    self.return_lib_entryText.set(selection[-1])

  #update copy's position? or keep it in same position every time
  def return_book(self):
    ret_id_entry = self.return_id_entry.get()  #use in WHERE
    ret_copy_entry = self.return_copy_entry.get()
    ret_lib_entry = self. return_lib_entry.get()
    today = datetime.date.today()     #import datetime
    if ret_id_entry != '' and ret_copy_entry != '' and ret_lib_entry != '': #check all fields filled in
      sql_input1 = "SELECT * FROM BORROWS WHERE READERID='%s' AND DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (self.reader_id, ret_id_entry, ret_copy_entry, ret_lib_entry)
      check_result = self.controller.dbConnect(sql_input1, 'fetch')
      if check_result != []:
        sql_input2 = "SELECT STATUS FROM COPY WHERE DOCID = '%s' AND COPYNO = '%s' AND LIBID = '%s'" % (ret_id_entry, ret_copy_entry, ret_lib_entry)
        status_result = self.controller.dbConnect(sql_input2, 'fetch') 
        if status_result[0][0] == "Borrowed":  #[0][0] to get string from unicode in list
          status_bool = True #check if status is borrowed in copy | This is an extra check for integrity constraints
          sql_input3 = "UPDATE BORROWS SET RDATE='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % (today, ret_id_entry, ret_copy_entry, ret_lib_entry)
          self.controller.dbConnect(sql_input3, 'commit')          
          sql_input4 = "UPDATE COPY SET STATUS='%s' WHERE DOCID='%s' AND COPYNO='%s' AND LIBID='%s'" % ("Available", ret_id_entry, ret_copy_entry, ret_lib_entry)
          self.controller.dbConnect(sql_input4, 'commit')
          self.view_all()  #since copy status was changed
          self.update_print_borrowed()     
          self.popup_window("Successfully returned- See Search Results")     
      else:
        self.popup_window("Entry does not exist")
    else:  
      self.popup_window("Enter a Valid Entry")   

  def logout(self): 
    for widget in self.winfo_children():
      if widget.winfo_class() == 'Entry' or widget.winfo_class() == 'Listbox':
        widget.delete(0,END)
    self.controller.show_frame("StartPage")

class AdminMenu(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.branch_id = StringVar(self)
    self.branch_id.set('L001') # default branch
    self.branch_ids_arr = self.get_branch_ids_arr()
    self.branch_info = self.get_branch_info()[0]
    self.widgets()
    self.bind("<<ShowFrame>>", self.onShowFrame)

  def onShowFrame(self, event):
    self.update_readers()
    self.branch_ids_arr = self.get_branch_ids_arr()
    self.branch_info = self.get_branch_info()
    #print(self.branch_ids_arr)  #in unicode

  def set_branch_id(self, value):
    self.branch_id.set(value[0])
    self.update_branch_label()

  def set_reader_type(self,value):
    self.selected_read_type.set(value)

  def popup_window(self, displayed_text):
    win = Toplevel()
    win_width = len(displayed_text)+500
    win.geometry('%sx100' % win_width)  #width by height
    self.center_popup(win)

    l = Label(win, text=displayed_text)
    l.config(font=(45))
    l.grid(row=1, column=1, sticky=NSEW)

    b = Button(win, text="Okay", command=win.destroy, width=3, height=1)
    b.grid(row=2, column=1, sticky=NSEW, pady=20)

    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(3, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(2, weight=1)

  def center_popup(self, toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

  def update_branch_label(self):
    self.branch_lab.grid_forget()
    self.branch_info = self.get_branch_info()[0]  #no need to [0] on showFrame and it works; but [0] req here
    self.branch_lab = Label( self, text="Library Name: %s   |  Location: %s" % (self.branch_info[0], 
        self.branch_info[1]))
    self.branch_lab.grid(row=0, column = 4, pady = 20, columnspan = 5, sticky=W, padx = 30)

  def widgets(self):
    Label( self, text="Welcome Admin").grid(row=0, column = 1, pady = 20)

    Label(self, text="Choose a Branch by Lib ID").grid(row = 0, column = 2)
    popupMenu = OptionMenu(self, self.branch_id, *self.branch_ids_arr, command = self.set_branch_id)
    popupMenu.grid(row = 0, column =3)
    self.branch_lab = Label( self, text="Library Name: %s   |  Location: %s" % (self.branch_info[0], 
        self.branch_info[1]))
    self.branch_lab.grid(row=0, column = 4, pady = 20, columnspan = 5, sticky=W, padx = 30)

    #display search results   #row 3: display windows
    Label( self, text="Search Results").grid(row=1, column = 0, pady = 20)
    Label( self, text="Click Entry to Add to Branch").grid(row=1, column = 1, pady = 20)
    #padx to left for all widgets in col 0
    Label( self, text="DocID    CopyNo    LibID").grid(row=2, column = 0, padx=(20,0), sticky=W)  
    Label( self, text="Doc Title").grid(row=2, column = 1)
    Label( self, text="Publisher").grid(row=2, column = 2)
    Label( self, text="Status").grid(row=2, column = 3, sticky=E)
    self.search_display = Listbox(self, height = 10, width=90)  #MUST separate declare and .grid in 2 lines
    #MUST separate declare and .grid in 2 lines
    self.search_display.grid(row=3, column = 0, padx=(20,0), columnspan=4)
    scrollbar1 = Scrollbar(self)
    scrollbar1.grid(row=3, column=4, sticky=(N,S,W)) #, rowspan=4
    self.search_display.configure(yscrollcommand=scrollbar1.set)   #apply scrollbar to listbox
    scrollbar1.configure(command=self.search_display.yview)

    scrollbar1b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar1b.grid(row=4, column=0, sticky=(E,W,N), padx=(20,0), columnspan=4)
    self.search_display.configure(xscrollcommand=scrollbar1b.set)   #apply scrollbar to listbox
    scrollbar1b.configure(command=self.search_display.xview)

    self.search_display.bind("<<ListboxSelect>>", self.AddSelected)

    #User Query Goes Below
    Label( self, text="Enter Search Below").grid(row=4, column = 1, pady=(30,30), sticky = S)
    Label( self, text="Search by Doc ID").grid(row=5, column = 0, sticky = N)
    Label( self, text="Search by Title").grid(row=6, column = 0, sticky = N)
    Label( self, text="Search by Publisher").grid(row=7, column = 0, sticky = N)
    self.id_search = Entry(self, bd = 5)
    self.id_search.grid(row=5, column = 1, pady=(0,20)) 
    self.title_search = Entry(self, bd = 5)
    self.title_search.grid(row=6, column = 1, pady=(0,20))  
    self.pub_search = Entry(self, bd = 5)
    self.pub_search.grid(row=7, column = 1, pady=(0,20))  
    Button(self, text ="Search", command = self.print_search).grid(row=5, column = 2, sticky = N)
    Button(self, text ="View All", command = self.view_all).grid(row=6, column = 2, sticky = N)
    Button(self, text ="View All in Current Branch", command = self.view_by_libid).grid(row=7, column = 2, sticky = N)

    #add doc copy from Documents
    Label( self, text="Manage Branch Copies").grid(row=8, column = 1, pady=(20,0))
    Label( self, text="Enter DocID to add").grid(row=9, column = 0)
    self.new_idText = tk.StringVar()
    self.new_id = Entry(self, bd = 5, textvariable=self.new_idText)
    self.new_id.grid(row=9, column = 1, sticky = N, pady=(10,0))  
    Button(self, text ="Add Copy to Current Branch", command = self.add_doc).grid(row=9, column = 2)
    #Button(self, text ="Delete Entry", command = self.getDate).grid(row=9, column = 2)  

    #print 10 most frequent borrowers, or most borr books, or most pop books
    Label( self, text="Name").grid(row=2, column = 4, sticky = "SE")
    Label( self, text="Rank").grid(row=2, column = 5, sticky = "SE")
    self.display_rank  = Listbox(self, height = 10, width = 45)
    self.display_rank.grid(row=3, column = 4, columnspan=2, padx=(100, 0))   
    scrollbar2 = Scrollbar(self)
    scrollbar2.grid(row=3, column=6, sticky=(N,S,W)) 
    self.display_rank.configure(yscrollcommand=scrollbar2.set) 
    scrollbar2.configure(command=self.display_rank.yview)

    scrollbar2b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar2b.grid(row=4, column=4, sticky=(E,W,N), padx=(100,0), columnspan=2)
    self.display_rank.configure(xscrollcommand=scrollbar2b.set) 
    scrollbar2b.configure(command=self.display_rank.xview)

    Button(self, text ="10 Most Frequent Borrowers in Current Branch", command = self.most_freq_borrowers).grid(row=2, column = 6, sticky=S, padx=(45, 0), columnspan = 2)
    Button(self, text ="10 Most Borrowed Books in Current Branch", command = self.most_borr_books).grid(row=3, column = 6, padx=(45, 0), columnspan = 2)
    Button(self, text ="10 Most Popular Books in Current Year", command = self.most_pop_books).grid(row=4, column = 6, sticky=N, padx=(45, 0), columnspan = 2)

    #prints readers and their avg fines
    Label( self, text="Reader Info").grid(row=4, column = 4, sticky = "SE")
    Label( self, text="Avg Fine").grid(row=4, column = 5, sticky = "SE")
    self.display_readers = Listbox(self, height = 10, width = 45)
    self.display_readers.grid(row=5, column = 4, rowspan = 4, columnspan = 2, padx=(100, 0), sticky=N)  
    scrollbar3 = Scrollbar(self)
    scrollbar3.grid(row=5, column=6, sticky=(N,S,W), rowspan = 4) 
    self.display_readers.configure(yscrollcommand=scrollbar3.set)
    scrollbar3.configure(command=self.display_readers.yview)

    scrollbar3b = Scrollbar(self, orient=HORIZONTAL)
    scrollbar3b.grid(row=9, column=4, sticky=(E,W,N), padx=(100,0), columnspan=2)
    self.display_readers.configure(xscrollcommand=scrollbar3b.set)  
    scrollbar3b.configure(command=self.display_readers.xview)

    #add new reader: Rname, rtype, address. Auto assign ID
    reader_types = ["citizen", "student", "senior citizen", "staff"]
    self.selected_read_type = StringVar(self)
    self.selected_read_type.set(reader_types[0])
    Label( self, text="Enter New Reader").grid(row=5, column = 7, padx=(20, 0), pady=(0,10))
    Label( self, text="Name").grid(row=6, column = 6, padx=(20, 0), pady=(0,10), sticky="NE")
    Label( self, text="Address").grid(row=7, column = 6, padx=(20, 0), pady=(0,10), sticky="NE")
    Label( self, text="Type").grid(row=8, column = 6, padx=(20, 0), pady=(0,10), sticky="NE")
    self.new_reader_name = Entry(self, bd = 5)
    self.new_reader_name.grid(row=6, column = 7, pady=(0,10), padx=(20,0), sticky=N)  
    self.new_reader_addr = Entry(self, bd = 5)
    self.new_reader_addr.grid(row=7, column = 7, pady=(0,10), padx=(20,0), sticky=N)  
    reader_type_menu = OptionMenu(self, self.selected_read_type, *reader_types, command = self.set_reader_type)
    reader_type_menu.grid(row = 8, column =7, sticky=N)
    Button(self, text ="Add Reader", command = self.add_reader).grid(row=9, column = 7, pady = 20)

    tk.Button(self, text="Logout",
      command=self.logout).grid(row=0, column=0)  #put it last after defining Listboxes

  def print_search(self):
    self.search_display.delete(0, END)
    id_query = self.id_search.get()
    title_query = self.title_search.get()
    pub_query = self.pub_search.get()

    if id_query != '' and title_query != '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND TITLE = '%s' AND PUBNAME ='%s'" % (id_query, title_query, pub_query)
    elif id_query == '' and title_query != '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE TITLE = '%s' AND PUBNAME ='%s'" % (title_query, pub_query)
    elif id_query != '' and title_query == '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND PUBNAME ='%s'" % (id_query, pub_query)
    elif id_query != '' and title_query != '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s' AND TITLE = '%s'" % (id_query, title_query)
    elif id_query != '' and title_query == '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE DOCID='%s'" % (id_query)
    elif id_query == '' and title_query != '' and pub_query == '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE TITLE = '%s'" % (title_query)
    elif id_query == '' and title_query == '' and pub_query != '':
      sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER  WHERE PUBNAME ='%s'" % (pub_query)
    else:
      self.popup_window("Enter a Valid Entry")
      return

    self.search_results = self.controller.dbConnect(sql_input, "fetch")
    if self.search_results == []:
      self.search_display.insert(END, "NO RESULTS FOUND")
      return

    for i in range(len(self.search_results)):
      doc_id = self.search_results[i][0]
      copyno = self.search_results[i][1]  
      libid = self.search_results[i][2]  
      doc_title = self.search_results[i][3]  
      doc_pub = self.search_results[i][4]  
      doc_status = self.search_results[i][5]  
      self.search_display.insert(i, "ID:  %s" % doc_id + ' '*10 + "CopyNo:  %s" % copyno + ' '*10 + 
        "LibID:  %s" % libid + ' '*20 + "Title:  %s" % doc_title + ' '*20 + 
        "Pub:  %s" % doc_pub +  ' '*20 + "Status:  %s \n" % doc_status )
      #cannot do "sdf %s" + ' ' + "xcv %s" % (x,y)

  def view_all(self):
    self.search_display.delete(0, END)
    sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER"
    self.search_results = self.controller.dbConnect(sql_input, "fetch")
    if self.search_results == []:
      self.search_display.insert(END, "NO RESULTS FOUND")
      return
    for i in range(len(self.search_results)):
      doc_id = self.search_results[i][0]
      copyno = self.search_results[i][1]  
      libid = self.search_results[i][2]  
      doc_title = self.search_results[i][3]  
      doc_pub = self.search_results[i][4]  
      doc_status = self.search_results[i][5]  
      self.search_display.insert(i, "ID:  %s" % doc_id + ' '*10 + "CopyNo:  %s" % copyno + ' '*10 + 
        "LibID:  %s" % libid + ' '*20 + "Title:  %s" % doc_title + ' '*20 + 
        "Pub:  %s" % doc_pub +  ' '*20 + "Status:  %s \n" % doc_status )

  def view_by_libid(self):
    self.search_display.delete(0, END)
    sql_input = "SELECT DOCID, COPYNO, LIBID, TITLE, PUBNAME, STATUS FROM DOCUMENT NATURAL JOIN COPY NATURAL JOIN PUBLISHER WHERE LIBID ='%s'" % (self.branch_id.get())
    self.search_results = self.controller.dbConnect(sql_input, "fetch")
    if self.search_results == []:
      self.search_display.insert(END, "NO RESULTS FOUND")
      return
    for i in range(len(self.search_results)):
      doc_id = self.search_results[i][0]
      copyno = self.search_results[i][1]  
      libid = self.search_results[i][2]  
      doc_title = self.search_results[i][3]  
      doc_pub = self.search_results[i][4]  
      doc_status = self.search_results[i][5]  
      self.search_display.insert(i, "ID:  %s" % doc_id + ' '*10 + "CopyNo:  %s" % copyno + ' '*10 + 
        "LibID:  %s" % libid + ' '*20 + "Title:  %s" % doc_title + ' '*20 + 
        "Pub:  %s" % doc_pub +  ' '*20 + "Status:  %s \n" % doc_status )

  def AddSelected(self, e):
    curr_sel_row = int(self.search_display.curselection()[0])
    selection = self.search_display.get(curr_sel_row).split()
    self.new_id.delete(0,END)
    self.new_idText.set(selection[1])

  #INSERT those tuples into COPIES such that libid is SELECTED LIBID BRANCH
  def add_doc(self):
    new_entry = self.new_id.get()
    if new_entry != '':  #prevent adding tuple w/ empty strings
      #select tuple from DOCUMENT where doc_id = new_entry
      sql_input1 = "SELECT * FROM DOCUMENT WHERE DOCID='%s'" % (new_entry)  
      result1 = self.controller.dbConnect(sql_input1, 'fetch')
      if result1 != []:  #check if docid is in Documents
        #using max, get current highest copyno of entered docid and +1 to get new copyno
        sql_input2 = "SELECT MAX(COPYNO) FROM COPY WHERE DOCID='%s' AND LIBID='%s'" % (new_entry, self.branch_id.get()) 
        result2 = self.controller.dbConnect(sql_input2, 'fetch')
        resultCopyNo = result2[0][0]    #b/c is int type in DB, it's int type in python. will be printed as string
        position = self.branch_id.get()[0] + self.branch_id.get()[-1] + new_entry[0:2] + str(resultCopyNo)[0:2]
        sql_input3 = "INSERT INTO COPY (DOCID, COPYNO, LIBID, POSITION, STATUS, FREQUENCY) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %(new_entry, str(resultCopyNo+1), self.branch_id.get(), position, "Available", 0)
        self.controller.dbConnect(sql_input3, 'commit')    
        self.popup_window("Successfully added- See Search Results")
        self.view_by_libid()
      else:
        self.popup_window("Enter a Valid Doc ID")
    else:
      self.popup_window("Enter a Valid Doc ID")

  #ONLY GET READERS FROM THE SELECTED BRANCH
  def most_freq_borrowers(self):
    sql_input = "SELECT RNAME, COUNT(*) FROM READER NATURAL JOIN BORROWS WHERE LIBID = '%s' GROUP BY LIBID, READERID ORDER BY READERID DESC" % self.branch_id.get()
    self.most_freqborr_arr = self.controller.dbConnect(sql_input, 'fetch')
    self.display_rank.delete(0, END)
    for i in range(len(self.most_freqborr_arr)):
      self.display_rank.insert(i, "Reader:  " + self.most_freqborr_arr[i][0] + ' '*40 + "Rank: " + str(i+1) + 
        ' '*40  + "Num of Books borrowed: " + str(self.most_freqborr_arr[i][1]) +'\n')
  
  #ONLY GET BOOKS FROM THE SELECTED BRANCH
  def most_borr_books(self):
    sql_input = "SELECT TITLE FROM BORROWS NATURAL JOIN DOCUMENT NATURAL JOIN BOOK WHERE LIBID = '%s' GROUP BY DOCID ORDER BY COUNT(*) DESC" % self.branch_id.get()
    self.most_borrbooks_arr = self.controller.dbConnect(sql_input, 'fetch')  
    self.display_rank.delete(0, END)
    for i in range(len(self.most_borrbooks_arr)):
      self.display_rank.insert(i, "Book:  " + self.most_borrbooks_arr[i][0] + ' '*40 + "Rank: " + str(i+1) + '\n')

  #get most pop books of the year (not specific to branch)
  def most_pop_books(self):
    sql_input = "SELECT TITLE FROM BORROWS NATURAL JOIN DOCUMENT NATURAL JOIN BOOK WHERE BDATE LIKE '2017%' GROUP BY DOCID ORDER BY COUNT(*) DESC"
    self.most_popbooks_arr = self.controller.dbConnect(sql_input, 'fetch')   
    self.display_rank.delete(0, END)
    for i in range(len(self.most_popbooks_arr)):
      self.display_rank.insert(i, "Book:  " + self.most_popbooks_arr[i][0] + ' '*40 + "Rank: " + str(i+1) + '\n')   

  def add_reader(self):
    new_reader_name_input = self.new_reader_name.get()
    new_reader_type_input = self.selected_read_type.get()
    new_reader_addr_input = self.new_reader_addr.get()
    #reader ID auto increments when added so no need to specify it in this code
    #prevent adding tuple w/ empty strings
    if new_reader_name_input != '' and new_reader_type_input != '' and new_reader_addr_input != '':
      sql_input = "INSERT INTO READER (RTYPE, RNAME, ADDRESS) VALUES ('%s', '%s', '%s')" %(new_reader_type_input, new_reader_name_input, new_reader_addr_input)
      self.controller.dbConnect(sql_input, 'commit')    
      #database has trigger to also add to fine
      self.popup_window("Successfully Added Reader")
      self.update_readers()
    else:
      self.popup_window("Not enough entries")

  def update_readers(self):  
    self.display_readers.delete(0, END)# Retrieves the all the BDATES of books not yet returned
    sql_input = "SELECT READERID, RNAME, RTYPE, ADDRESS, FINE / OVERDUE AS AVERAGE FROM FINE NATURAL JOIN READER WHERE OVERDUE != 0 GROUP BY READERID"
    self.readers_arr = self.controller.dbConnect(sql_input, 'fetch')     
    #calculate avg fine
    #NOT BRANCH SPECIFIC- DISPLAYS READERS FROM ALL BRANCHES
    self.display_readers.insert(0, "Readers with Fines:" + '\n')
    for i in range(len(self.readers_arr)):
      reader_id = self.readers_arr[i][0]
      reader_name = self.readers_arr[i][1]
      rtype = self.readers_arr[i][2]
      addr = self.readers_arr[i][3]
      fine_avg = self.readers_arr[i][4]
      self.display_readers.insert(i+1, "ReaderID:  %s" % reader_id + ' '*10 
        + "Name:  %s" % reader_name + ' '*20
        + "Fine:  %s" % format(fine_avg, '.2f') + ' '*20
        + "Type:  %s" % rtype + ' '*20
        + "Address:  %s" % addr)
    i+=2
    self.display_readers.insert(i, "")
    i+=1
    self.display_readers.insert(i, "Readers with no Fines:")
    sql_input_2 = "SELECT READERID, RNAME, RTYPE, ADDRESS FROM READER NATURAL JOIN FINE WHERE FINE IS NULL"
    self.readers_arr = self.controller.dbConnect(sql_input_2, 'fetch')  
    for j in range(len(self.readers_arr)):
      reader_id = self.readers_arr[j][0]
      reader_name = self.readers_arr[j][1]
      rtype = self.readers_arr[j][2]
      addr = self.readers_arr[j][3]
      self.display_readers.insert(j+i+1, "ReaderID:  %s" % reader_id + ' '*10 
        + "Name:  %s" % reader_name + ' '*20
        + "Type:  %s" % rtype + ' '*20
        + "Address:  %s" % addr)   

  def get_branch_ids_arr(self):
    sql_input = "SELECT LIBID FROM BRANCH"
    return self.controller.dbConnect(sql_input, 'fetch')  

  def get_branch_info(self):
    sql_input = "SELECT LNAME, LLOCATION FROM BRANCH WHERE LIBID='%s'" % self.branch_id.get()
    return self.controller.dbConnect(sql_input, 'fetch')  

  def logout(self): 
    for widget in self.winfo_children():
      if widget.winfo_class() == 'Entry' or widget.winfo_class() == 'Listbox':
        widget.delete(0,END)
    self.controller.show_frame("StartPage")


def main():
  app = LibraryApp()
  app.mainloop()

if __name__ == "__main__":
  try:
    main()
  except:
    type, value, tb = sys.exc_info()
    traceback.print_exc()
    pdb.post_mortem(tb)