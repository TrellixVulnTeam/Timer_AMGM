from app import app,db
from models import user ,days
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from flask import Flask,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from datetime import datetime,date,time

app.secret_key='zzz'

class MyModelView(ModelView):
    def is_accessible(self):
        return True

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return True

Admin = Admin(app, index_view=MyAdminIndexView())
Admin.add_view(MyModelView(user, db.session))
Admin.add_view(MyModelView(days, db.session))
time = 0
@app.route("/")
def index():
    d=datetime.now()
    days=d.day
    month = d.strftime("%B")
    Dict=dict()
    work=[]
    all_users = user.query.all()
    for us in all_users: 
        Dict={us.username:us.work_hours}
        work.append(Dict)
    return render_template('index.html',time = time,user=all_users,work=work,days=days,month= month)

global user_name

class main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.repeat_pass = StringVar()
        self.work_hours = StringVar()
        self.widgets()
    def login(self):
        global user_name
        global timer
        user_name = self.username.get()
        find_user = user.query.filter(user.username== self.username.get() and user.password == self.password.get()).first()

        if find_user:
            now = datetime.now()
            current_day = now.strftime("%d/%b/%Y")
            name = self.username.get()
            name_label.config(text=name)
            root.deiconify()
            self.master.destroy()
            update = user.query.filter(user.username == user_name).first()
            day = days.query.filter(days.user_id == update.id).order_by(days.id.desc()).first()
            time = day.work_hours
            day_part=day.day.split('/')
            time_part = time.split(":")
            if int(now.day) == int(day_part[0]) :
                if len(time_part) == 3:
                    time_part[0] = int(time_part[0])
                    time_part[1] = int(time_part[1])
                    time_part[2] = int(time_part[2])
                    timer = time_part
                timeText.configure(text=time)
            else:
                timeText.configure(text="00:00:00")
                new_day = days(user_id = update.id, day= current_day, work_hours = "00:00:00")
                db.session.add(new_day)
                db.session.commit()
        else:
            messagebox.showerror('Oops!', 'User Not Found.')

    def new_user(self):
 
        if user.query.filter(user.username == self.n_username.get()).first():
            messagebox.showerror('Error!', 'Username Taken Try a Diffrent One.')
        elif self.n_password.get() != self.repeat_pass.get():
            messagebox.showerror('Error!', 'Passwords must match!.')
        else:
            messagebox.showinfo('Success!', 'Account Created!')
            self.log()
            new_user = user(username=self.n_username.get(),password=self.n_password.get(),work_hours='00:00:00')
            db.session.add(new_user)
            db.session.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.repeat_pass.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    

    def widgets(self):
        self.head = ttk.Label(self.master, text='LOGIN', background='gray94', font=('helvetica', 25))
        self.head.pack(pady=15)
        self.logf = ttk.Frame(self.master)
        ttk.Label(self.logf, text='Username: ', font=('Helvetica', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.logf, textvariable=self.username, font=('', 15)).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.logf, text='Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.logf, textvariable=self.password, font=('', 15), show='*').grid(row=1, column=1,padx=10, pady=5)
        ttk.Button(self.logf, text=' Login ', command=self.login).grid(padx=10, pady=10)
        ttk.Button(self.logf, text=' Create Account ', command=self.cr).grid(row=2, column=1)
        self.master.resizable(0, 0)
        self.logf.pack()

        self.crf = ttk.Frame(self.master)
        ttk.Label(self.crf, text='Username: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.n_username, font=('', 15)).grid(row=0, column=1,padx=10, pady=5)
        ttk.Label(self.crf, text='Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.n_password, font=('', 15), show='*').grid(row=1, column=1,padx=10, pady=5)
        ttk.Label(self.crf, text='Repeat Password: ', font=('', 15)).grid(sticky=E,padx=10)
        ttk.Entry(self.crf, textvariable=self.repeat_pass, font=('', 15), show='*').grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self.crf, text='Create Account', command=self.new_user).grid(padx=10, pady=10)
        ttk.Button(self.crf, text='Go to Login', command=self.log).grid(row=3, column=1)


def update_time():
    if state:
        global timer
        global user_name
        timer[2] += 1
        if timer[2] > 59:
            timer[2] = 0
            timer[1] += 1
        if timer[1] > 59:
            timer[0] += 1
            timer[1] = 0
            
    
        time_string = pattern.format(timer[0], timer[1], timer[2])     
        timeText.configure(text=time_string)
        autosave(timer[2])
    root.after(1000, update_time)
   
    

def autosave(seconds):
    if seconds != 59:
        return  True
    now=datetime.now()
    time = timeFormat(timer[0])+':'+timeFormat(timer[1])+':'+timeFormat(timer[2])
        
    update = user.query.filter(user.username == user_name).first()
    update.work_hours = time
    day = days.query.filter(db.and_(days.user_id == update.id, days.day == now.day)).first()
    day.work_hours = time
    db.session.commit()
    

def start(event=''):
    global state
    state = True
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%d/%b/%Y")
    update = user.query.filter(user.username == user_name).first()
    update.start_time = current_time
    day = days.query.filter(days.user_id == update.id).first()
    if  day is None: 
        new_day = days(user_id = update.id, day= current_day, work_hours = "00:00:00" )
        db.session.add(new_day)
        db.session.commit()


time = None

def pause():
    global state
    global time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if messagebox.askokcancel("Pause", "Do You want to pause timer?"):
        state = False
        
        time = timeFormat(timer[0])+':'+timeFormat(timer[1])+':'+timeFormat(timer[2])
        
        update = user.query.filter(user.username == user_name).first()
        update.work_hours = time
        update.end_time = current_time
        day = days.query.filter(db.and_(days.user_id == update.id, days.day == now.day)).first()
        day.work_hours = time
        db.session.commit()
        
def timeFormat(time):
    if time < 10:
        return '0' + str(time)
    else:
        return str(time)
    
        
        
       


def reset():
    global timer
    if messagebox.askokcancel("Reset", "Do You want to reset timer?"):
        timer = [0, 0, 0]
        timeText.configure(text='00:00:00')


def exist():
    if messagebox.askokcancel("Exit", "Are You sure?"):
        root.destroy()




state = False

root = ThemedTk(theme='arc')
root.title('Timer')
root.iconbitmap('python.ico')
root.geometry("400x300+500+150")
root.resizable(False, False)
timer = [0, 0, 0]
pattern = '{0:02d}:{1:02d}:{2:02d}'

top_frame = ttk.Frame(root)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor='n')

btn_start = ttk.Button(top_frame, text='Start', command=start)
btn_start.place(relx=0.40, relwidth=0.25, relheight=1)

lower_frame = ttk.Frame(root)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

name_label = ttk.Label(lower_frame, text="", font=("Helvetica", 12))
name_label.pack()

timeText = ttk.Label(lower_frame, text="", font=("Helvetica", 30))
timeText.pack()

pauseButton = ttk.Button(lower_frame, text='Pause', command=pause)
pauseButton.pack()

resetButton = ttk.Button(lower_frame, text='Reset', command=reset)
resetButton.pack()

quitButton = ttk.Button(lower_frame, text='Quit', command=exist)
quitButton.pack()

main(Toplevel())
update_time()
root.withdraw()
root.mainloop()
