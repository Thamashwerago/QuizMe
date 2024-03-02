#---import python GUI library and other library---
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

#---function area---
def showpage(page):
    page.tkraise()

def leave(window):
    window.destroy()

def login():
    global username
    loginUsername=str(loginusername.get())
    loginPassword=str(loginpassword.get())
    loginusername.delete(0, END)
    loginpassword.delete(0, END)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username='"+loginUsername+"' AND password='"+loginPassword+"'")
    result = cursor.fetchone()
    if result != None:
        username=result[0]
        if result[2]=="admin":
            showpage(adminpage)
        elif result[2]=="user":
            showpage(userpage)
    else:
        messagebox.showerror("ERROR","Invalid username and password")
    cursor.close()
    conn.close()

def register():
    registerUsername=str(registerusername.get())
    registerPassword=str(registerpassword.get())
    registerRepassword=str(registerrepassword.get())
    registerpassword.delete(0, END)
    registerrepassword.delete(0, END)
    if registerPassword != registerRepassword:
        messagebox.showerror("ERROR","password and Re-password are not same")
        return
    registerusername.delete(0, END)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username='"+registerUsername+"'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result != None:
        messagebox.showerror("ERROR","User exist")
        return
    if registerPassword == registerRepassword:
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        sql=("INSERT INTO user (username,password,status) VALUES (?,?,?)")
        val=(registerUsername,registerPassword,'user')
        cursor.execute(sql,val)
        conn.commit()
        if cursor.rowcount>0:
            messagebox.showinfo("DONE","User add successfully")
        else:
            messagebox.showerror("ERROR","Can't add user now")
        cursor.close()
        conn.close()
    else:
        messagebox.showerror("ERROR","password and Re-password are not same")

def uplodequiz():
    quizname=str(name.get())
    quizabout=str(about.get(1.0, END))
    name.delete(0, END)
    about.delete(1.0, END)
    data=[]
    window.filename = filedialog.askopenfilename(initialdir="C:/",title="Select quiz text file",filetypes=(("Text Files","*.txt"),("All File","*.*")))
    if window.filename == "":
        return
    f = open(window.filename,"r")
    txt=f.readline()
    if txt!="\n":
        if txt[-1:]=="\n":
            size=len(txt)
            txt=txt[:size-1]
        data.append(txt)
    while txt!="":
        txt=f.readline()
        if txt!="\n":
            if txt!="":
                if txt[-1:]=="\n":
                    size=len(txt)
                    txt=txt[:size-1]
                data.append(txt)
    f.close
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    sql=("INSERT INTO aboutquiz (quizname,about) VALUES (?,?)")
    val=(quizname,quizabout)
    cursor.execute(sql,val)
    conn.commit()
    cursor.close()
    conn.close()
    i=0
    while i<len(data):
        x=0
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        sql=("INSERT INTO quizes (quizname,question,answer1,answer2,answer3,answer4,correct) VALUES (?,?,?,?,?,?,?)")
        val=(quizname,data[i],data[i+1],data[i+2],data[i+3],data[i+4],data[i+5])
        cursor.execute(sql,val)
        conn.commit()
        x=cursor.rowcount
        cursor.close()
        conn.close()
        i=i+6
    if x>0:
        messagebox.showinfo("Uplode INFO","Uplode successfully")
    else:
        messagebox.showerror("ERROR","Incorrect data")
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        cursor.execute("DELETE FROM quizes WHERE quizname=(?)",quizname)
        conn.commit()
        cursor.execute("DELETE FROM aboutquiz WHERE quizname=(?)",quizname)
        conn.commit()
        cursor.close()
        conn.close()

def exitsubmit(window_1,window_2):
    leave(window_1)
    leave(window_2)

def submitquiz(window,quizname,ans,que):
    submitquizwindow=Toplevel()
    submitquizwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    submitquizwindow.iconphoto(False,icon)
    submitquizwindow.geometry("1000x600")
    submitquizwindow.config(bg='#1F2835')
    minisubmitquizwindow=Frame(submitquizwindow,background='#1F2835')
    minisubmitquizwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    score=0
    queno=0
    quizname=quizname[0]
    while len(que)>queno:
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        cursor.execute("SELECT correct FROM quizes WHERE quizname=(?) AND question=(?)",(str(quizname),str(que[queno])))
        result = cursor.fetchone()
        if result[0] == ans[queno].get():
            score=score+1
        queno=queno+1
    cursor.close()
    conn.close()
    score=score*(100/queno)
    score=round(score,2)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO userscore (username,quizname,score) VALUES (?,?,?)",(str(username),str(quizname),str(score)))
    conn.commit()
    cursor.close()
    conn.close()
    Label(minisubmitquizwindow,text="Your Score",font='times 24',bg='#1F2835',fg='#E6E9F9').pack(pady=10)
    Label(minisubmitquizwindow,text=score,font='times 24',bg='#1F2835',fg='#E6E9F9').pack(pady=10)
    Button(minisubmitquizwindow,text="Done",command=lambda:exitsubmit(submitquizwindow,window),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def startquiz(window,quizname):
    leave(window)
    startquizwindow=Toplevel()
    startquizwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    startquizwindow.iconphoto(False,icon)
    startquizwindow.geometry("1000x600")
    startquizwindow.state('zoomed')
    
    mainframe=Frame(startquizwindow,bg='#E6E9F9')
    mainframe.pack(fill=BOTH,expand=1)
    canvas=Canvas(mainframe,bg='#E6E9F9')
    canvas.pack(side=LEFT,fill=BOTH,expand=1)
    scrollbar=ttk.Scrollbar(mainframe,orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    windowframe=Frame(canvas,bg='#E6E9F9')
    canvas.create_window((0,0),window=windowframe,anchor="nw")
    
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT question,answer1,answer2,answer3,answer4 FROM quizes WHERE quizname=(?)",quizname)
    results = cursor.fetchall()
    ans=[]
    que=[]
    i=0
    r=0
    for result in results:
        ans.append("")
        ans[r]=StringVar()
        que.append(result[0])
        question="("+str(r+1)+") "+result[0]
        Label(windowframe,text=question,font='times 16',fg='#1F2835',bg='#E6E9F9').grid(row=i,column=0,sticky="W")
        Radiobutton(windowframe, text=result[1], variable=ans[r], value=result[1],font='times 16',fg='#1F2835',bg='#E6E9F9').grid(row=i+1,column=0,sticky="W")
        Radiobutton(windowframe, text=result[2], variable=ans[r], value=result[2],font='times 16',fg='#1F2835',bg='#E6E9F9').grid(row=i+2,column=0,sticky="W")
        Radiobutton(windowframe, text=result[3], variable=ans[r], value=result[3],font='times 16',fg='#1F2835',bg='#E6E9F9').grid(row=i+3,column=0,sticky="W")
        Radiobutton(windowframe, text=result[4], variable=ans[r], value=result[4],font='times 16',fg='#1F2835',bg='#E6E9F9').grid(row=i+4,column=0,sticky="W")
        Label(windowframe,text="",bg='#E6E9F9').grid(row=i+5,column=0)
        i=i+6
        r=r+1
    cursor.close()
    conn.close()
    Label(windowframe,text="",bg='#E6E9F9').grid(row=i,column=0)
    Label(windowframe,text="",bg='#E6E9F9').grid(row=i+1,column=0)
    Label(windowframe,text="",bg='#E6E9F9').grid(row=i+2,column=0)
    Button(windowframe,text="Submit",command=lambda:submitquiz(startquizwindow,quizname,ans,que),font='times 16 bold',bg='#9CBCEA',fg='#060146').grid(row=i+3,column=0,pady=10,padx=100)
    Button(windowframe,text="Cancel",command=lambda:leave(startquizwindow),font='times 16 bold',bg='#9CBCEA',fg='#060146').grid(row=i+3,column=1,pady=10,padx=100)

def startquizprompt(window,name):
    if name == "":
        return
    quizname=[]
    quizname.append(name)
    leave(window)
    quizpromptwindow=Toplevel()
    quizpromptwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    quizpromptwindow.iconphoto(False,icon)
    quizpromptwindow.geometry("1000x600")
    quizpromptwindow.config(bg='#1F2835')
    miniquizpromptwindow=Frame(quizpromptwindow,background='#1F2835')
    miniquizpromptwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM aboutquiz WHERE quizname=(?)",quizname)
    result = cursor.fetchone()
    Label(miniquizpromptwindow,text=result[0],font='times 24',bg='#1F2835',fg='#E6E9F9').pack(pady=10)
    Label(miniquizpromptwindow,text=result[1],font='times 24',bg='#1F2835',fg='#E6E9F9').pack(pady=10)
    cursor.close()
    conn.close()
    Button(miniquizpromptwindow,text="Start",command=lambda:startquiz(quizpromptwindow,quizname),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)
    Button(miniquizpromptwindow,text="Cancel",command=lambda:leave(quizpromptwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def getquizes():
    quizwindow=Toplevel()
    quizwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    quizwindow.iconphoto(False,icon)
    quizwindow.geometry("1000x600")
    quizwindow.config(bg='#1F2835')
    miniquizwindow=Frame(quizwindow,background='#1F2835')
    miniquizwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    frame=Frame(miniquizwindow,bg='#E6E9F9')
    scrollbar=Scrollbar(frame,orient=VERTICAL,bg='#E6E9F9')
    listbox=Listbox(frame,yscrollcommand=scrollbar.set,font='times 20',bg='#E6E9F9',fg='#060146',width=50,selectbackground='#5660A1')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    frame.pack()
    listbox.pack(pady=10)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT quizname FROM aboutquiz")
    results = cursor.fetchall()
    for result in results:
        listbox.insert(END,result[0])
    cursor.close()
    conn.close()
    Button(miniquizwindow,text="Get Quiz",command=lambda:startquizprompt(quizwindow,listbox.get(ANCHOR)),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)
    Button(miniquizwindow,text="Cancel",command=lambda:leave(quizwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def showresults(name):
    if name == "":
        return
    user=[]
    user.append(name)
    resultwindow=Toplevel()
    resultwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    resultwindow.iconphoto(False,icon)
    resultwindow.geometry("1000x600")
    resultwindow.config(bg='#1F2835')
    miniresultwindow=Frame(resultwindow,background='#1F2835')
    miniresultwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    frame=Frame(miniresultwindow,bg='#E6E9F9')
    scrollbar=Scrollbar(frame,orient=VERTICAL,bg='#E6E9F9')
    listbox=Listbox(frame,yscrollcommand=scrollbar.set,font='times 20',bg='#E6E9F9',fg='#060146',width=50,selectbackground='#5660A1')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    Label(miniresultwindow,text="Quiz Name        Score",font='times 18',bg='#1F2835',fg='#E6E9F9').pack(pady=10)
    frame.pack()
    listbox.pack(pady=10)
    
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT quizname,score FROM userscore WHERE username=(?)",(user))
    results = cursor.fetchall()
    for result in results:
        txt=result[0]+"    "+result[1]
        listbox.insert(END,txt)
    cursor.close()
    conn.close()
    Button(miniresultwindow,text="Exit",command=lambda:leave(resultwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def deletequiz(window,name):
    if name == "":
        return
    confirm=messagebox.askokcancel("Are You Sure","Do you want to delete this quiz?")
    if confirm == 1:
        quizname=[]
        quizname.append(name)
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        cursor.execute("DELETE FROM quizes WHERE quizname=(?)",quizname)
        conn.commit()
        cursor.execute("DELETE FROM aboutquiz WHERE quizname=(?)",quizname)
        conn.commit()
        cursor.execute("DELETE FROM userscore WHERE quizname=(?)",quizname)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Delete quiz","Quiz delete successfully")
        leave(window)
    elif confirm == 0:
        return

def deletequizpromp():
    deletequizwindow=Toplevel()
    deletequizwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    deletequizwindow.iconphoto(False,icon)
    deletequizwindow.geometry("1000x600")
    deletequizwindow.config(bg='#1F2835')
    minideletequizwindow=Frame(deletequizwindow,background='#1F2835')
    minideletequizwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    frame=Frame(minideletequizwindow,bg='#E6E9F9')
    scrollbar=Scrollbar(frame,orient=VERTICAL,bg='#E6E9F9')
    listbox=Listbox(frame,yscrollcommand=scrollbar.set,font='times 20',bg='#E6E9F9',fg='#060146',width=50,selectbackground='#5660A1')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    frame.pack()
    listbox.pack(pady=10)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT quizname FROM aboutquiz")
    results = cursor.fetchall()
    for result in results:
        listbox.insert(END,result[0])
    cursor.close()
    conn.close()
    Button(minideletequizwindow,text="Delete",command=lambda:deletequiz(deletequizwindow,listbox.get(ANCHOR)),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)
    Button(minideletequizwindow,text="Cancel",command=lambda:leave(deletequizwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def deleteuser(window,name):
    if name == "":
        return
    confirm=messagebox.askokcancel("Are You Sure","Do you want to delete this user?")
    if confirm == 1:
        username=[]
        username.append(name)
        conn = sqlite3.connect('quiz_me')
        cursor=conn.cursor()
        cursor.execute("DELETE FROM user WHERE username=(?)",username)
        conn.commit()
        cursor.execute("DELETE FROM userscore WHERE username=(?)",username)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Delete User","User delete successfully")
        leave(window)
    elif confirm == 0:
        return

def deleteuserpromp():
    deleteuserwindow=Toplevel()
    deleteuserwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    deleteuserwindow.iconphoto(False,icon)
    deleteuserwindow.geometry("1000x600")
    deleteuserwindow.config(bg='#1F2835')
    minideleteuserwindow=Frame(deleteuserwindow,background='#1F2835')
    minideleteuserwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    frame=Frame(minideleteuserwindow,bg='#E6E9F9')
    scrollbar=Scrollbar(frame,orient=VERTICAL,bg='#E6E9F9')
    listbox=Listbox(frame,yscrollcommand=scrollbar.set,font='times 20',bg='#E6E9F9',fg='#060146',width=50,selectbackground='#5660A1')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    frame.pack()
    listbox.pack(pady=10)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT username FROM user WHERE status='user'")
    results = cursor.fetchall()
    for result in results:
        listbox.insert(END,result[0])
    cursor.close()
    conn.close()
    Button(minideleteuserwindow,text="Delete",command=lambda:deleteuser(deleteuserwindow,listbox.get(ANCHOR)),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)
    Button(minideleteuserwindow,text="Cancel",command=lambda:leave(deleteuserwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

def showuser():
    showuserwindow=Toplevel()
    showuserwindow.title("Quiz Me")
    icon = PhotoImage(file = 'pic.png')
    showuserwindow.iconphoto(False,icon)
    showuserwindow.geometry("1000x600")
    showuserwindow.config(bg='#1F2835')
    minishowuserwindow=Frame(showuserwindow,background='#1F2835')
    minishowuserwindow.place(relx=0.5,rely=0.5,anchor=CENTER)
    
    frame=Frame(minishowuserwindow,bg='#E6E9F9')
    scrollbar=Scrollbar(frame,orient=VERTICAL,bg='#E6E9F9')
    listbox=Listbox(frame,yscrollcommand=scrollbar.set,font='times 20',bg='#E6E9F9',fg='#060146',width=50,selectbackground='#5660A1')
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    frame.pack()
    listbox.pack(pady=10)
    conn = sqlite3.connect('quiz_me')
    cursor=conn.cursor()
    cursor.execute("SELECT username FROM user WHERE status='user'")
    results = cursor.fetchall()
    for result in results:
        listbox.insert(END,result[0])
    cursor.close()
    conn.close()
    Button(minishowuserwindow,text="User Score",command=lambda:showresults(listbox.get(ANCHOR)),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)
    Button(minishowuserwindow,text="Cancel",command=lambda:leave(showuserwindow),font='times 18 bold',bg='#9CBCEA',fg='#060146').pack(pady=10)

#---configuring window---
window = Tk()
window.title("Quiz Me")
icon = PhotoImage(file = 'pic.png')
window.iconphoto(False,icon)
window.geometry("1000x600")
window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
window.state('zoomed')

#---define programme pages---
startpage = Frame(window,background='#1F2835')
loginpage = Frame(window,background='#1F2835')
registerpage = Frame(window,background='#1F2835')
userpage = Frame(window,background='#1F2835')
adminpage = Frame(window,background='#1F2835')
quizpage = Frame(window,background='#1F2835')
uplodequizpage = Frame(window,background='#1F2835')
adminuserpage = Frame(window,background='#1F2835')

#---put pages into window---
for page in (startpage,loginpage,registerpage,userpage,adminpage,quizpage,uplodequizpage,adminuserpage):
    page.grid(row=0,column=0,sticky="nsew")

#---startpage---
ministartpage=Frame(startpage,background='#1F2835')
ministartpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Button(ministartpage,text="LOGIN",command=lambda:showpage(loginpage),height=2,width=20,font='times 24 bold',bg='#9CBCEA',fg='#060146',relief=RAISED).pack(pady=5)
Button(ministartpage,text="EXIT",command=lambda:leave(window),height=2,width=20,font='times 24 bold',bg='#9CBCEA',fg='#060146',relief=RAISED).pack(pady=5)

#---loginpage---
miniloginpage=Frame(loginpage,background='#1F2835')
miniloginpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Label(miniloginpage,text="Username:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=0,column=0,pady=5,padx=10)
loginusername=Entry(miniloginpage,font='times 20',bg='#E6E9F9',fg='#060146')
loginusername.grid(row=0,column=1,pady=5)
Label(miniloginpage,text="Password:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=1,column=0,pady=5,padx=10)
loginpassword=Entry(miniloginpage,font='times 20',bg='#E6E9F9',fg='#060146')
loginpassword.grid(row=1,column=1,pady=5)
Button(miniloginpage,text="Login",command=login,font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=2,column=0,pady=20)
Button(miniloginpage,text="Cancel",command=lambda:showpage(startpage),font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=2,column=1,pady=20)

#---registerpage---
miniregisterpage=Frame(registerpage,background='#1F2835')
miniregisterpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Label(miniregisterpage,text="Username:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=1,column=0,pady=10)
registerusername=Entry(miniregisterpage,font='times 20',bg='#E6E9F9',fg='#060146')
registerusername.grid(row=1,column=1,pady=10)
Label(miniregisterpage,text="Password:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=2,column=0,pady=10)
registerpassword=Entry(miniregisterpage,font='times 20',bg='#E6E9F9',fg='#060146')
registerpassword.grid(row=2,column=1,pady=10)
Label(miniregisterpage,text="Re-password:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=3,column=0,pady=10)
registerrepassword=Entry(miniregisterpage,font='times 20',bg='#E6E9F9',fg='#060146')
registerrepassword.grid(row=3,column=1,pady=10)
Button(miniregisterpage,text="Cancel",command=lambda:showpage(adminuserpage),font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=4,column=0,pady=10)
Button(miniregisterpage,text="Register",command=register,font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=4,column=1,pady=10)

#--adminpage--
miniadminpage=Frame(adminpage,background='#1F2835')
miniadminpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Button(miniadminpage,text="Manage Quizes",command=lambda:showpage(quizpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=2).grid(row=0,column=0,pady=10)
Button(miniadminpage,text="Manage Users",command=lambda:showpage(adminuserpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=8).grid(row=1,column=0,pady=10)
Button(miniadminpage,text="Logout",command=lambda:showpage(startpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=52).grid(row=2,column=0,pady=10)
Button(miniadminpage,text="EXIT",command=lambda:leave(window),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=61).grid(row=3,column=0,pady=10)

#--userpage--
miniuserpage=Frame(userpage,background='#1F2835')
miniuserpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Button(miniuserpage,text="Get Quiz",command=getquizes,font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=10).grid(row=0,column=0,pady=10)
Button(miniuserpage,text="Results",command=lambda:showresults(username),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=20).grid(row=1,column=0,pady=10)
Button(miniuserpage,text="Logout",command=lambda:showpage(startpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=21).grid(row=2,column=0,pady=10)
Button(miniuserpage,text="EXIT",command=lambda:leave(window),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=30).grid(row=3,column=0,pady=10)

#---quizpage---
miniquizpage=Frame(quizpage,background='#1F2835')
miniquizpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Button(miniquizpage,text="Add Quiz",command=lambda:showpage(uplodequizpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=13).grid(row=0,column=0,pady=10)
Button(miniquizpage,text="Open Quiz",command=getquizes,font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=6).grid(row=1,column=0,pady=10)
Button(miniquizpage,text="Delete Quiz",command=deletequizpromp,font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=2,column=0,pady=10)
Button(miniquizpage,text="Back",command=lambda:showpage(adminpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=42).grid(row=3,column=0,pady=10)

#--uplodequizpage--
miniuplodequizpage=Frame(uplodequizpage,background='#1F2835')
miniuplodequizpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Label(miniuplodequizpage,text="Quiz name:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=0,column=0,pady=10)
name = Entry(miniuplodequizpage,font='times 20',bg='#E6E9F9',fg='#060146')
name.grid(row=0,column=1,pady=10)
Label(miniuplodequizpage,text="About:",font='times 24',bg='#1F2835',fg='#E6E9F9').grid(row=1,column=0,pady=10)
about=Text(miniuplodequizpage,height=4,width=30,font='times 20',bg='#E6E9F9',fg='#060146')
about.grid(row=1,column=1,pady=10)
Button(miniuplodequizpage,text="Cancel",command=lambda:showpage(quizpage),font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=2,column=0,pady=10)
Button(miniuplodequizpage,text="Uplode File",command=uplodequiz,font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=2,column=1,pady=10)

#---adminuserpage---
miniadminuserpage=Frame(adminuserpage,background='#1F2835')
miniadminuserpage.place(relx=0.5,rely=0.5,anchor=CENTER)
Button(miniadminuserpage,text="Show Users",command=showuser,font='times 18 bold',bg='#9CBCEA',fg='#060146').grid(row=0,column=0,pady=10)
Button(miniadminuserpage,text="ADD User",command=lambda:showpage(registerpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=9).grid(row=1,column=0,pady=10)
Button(miniadminuserpage,text="Delete User",command=deleteuserpromp,font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=2).grid(row=2,column=0,pady=10)
Button(miniadminuserpage,text="Back",command=lambda:showpage(adminpage),font='times 18 bold',bg='#9CBCEA',fg='#060146',padx=43).grid(row=3,column=0,pady=10)

#---start programme---
showpage(startpage)

#---end programme---
window.mainloop()