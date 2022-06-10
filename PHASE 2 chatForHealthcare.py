#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Importing the libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import webbrowser
from PIL import ImageTk, Image
import hashlib
import re
import numpy as np
import pandas as pd


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_name = re.compile(r'([a-z]+)( [a-z]+)*( [a-z]+)*$',re.IGNORECASE)
class HyperlinkManager:
      
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Importing the dataset
training_dataset = pd.read_csv('https://raw.githubusercontent.com/aryanveturekar/Health-Care-Chat-Bot/master/Training.csv')
test_dataset = pd.read_csv('https://raw.githubusercontent.com/aryanveturekar/Health-Care-Chat-Bot/master/Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"
                
#                ans = input()
                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                strData=""
                present_disease = print_disease(tree_.value[node])
#                print( "You may have " +  present_disease )
#                print()
                strData="You may have :" +  str(present_disease)
               
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                
                red_cols = dimensionality_reduction.columns 
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
#                print("symptoms present  " + str(list(symptoms_present)))
#                print()
                strData="symptoms present:  " + str(list(symptoms_present))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print("symptoms given "  +  str(list(symptoms_given)) )  
#                print()
                strData="symptoms given: "  +  str(list(symptoms_given))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
#                print("confidence level is " + str(confidence_level))
#                print()
                strData="confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print('The model suggests:')
#                print()
                strData='The model suggests:'
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                row = doctors[doctors['disease'] == present_disease[0]]
#                print('Consult ', str(row['name'].values))
#                print()
                strData='Consult '+ str(row['name'].values)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print('Visit ', str(row['link'].values))
                #print(present_disease[0])
                hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                strData='Visit '+ str(row['link'].values[0])
                def click1():
                    webbrowser.open_new(str(row['link'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                #QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                yield strData
        
def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        #print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []   
#        recurse(0, 1)
    

def execute_bot():
#    print("Please reply with yes/Yes or no/No for the following symptoms")    
    tree_to_code(classifier,cols)



# This section of code to be run after scraping the data

# doc_dataset = pd.read_csv('E:\Chatbot Project\Health-Care-Chat-Bot-master\doctors_dataset.csv', names = ['Name', 'Description'])

doc_dataset = pd.read_csv('https://raw.githubusercontent.com/aryanveturekar/Health-Care-Chat-Bot/master/doctors_dataset.csv', names = ['Name', 'Description'])



diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']


doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']




# Execute the bot and see it in Action
#execute_bot()


class QuestionDigonosis(Frame):
    objIter=None
    objRef=None
    def __init__(self,master=None):
        
        master.title("Question")
        # root.iconbitmap("")
        master.state("z")
        master.title("Register")
        master.geometry("600x400")
        # master.minsize(700,400)
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        self["bg"]="light blue"
        self.createWidget()
        self.iterObj=None

    def createWidget(self):
        self.btnStart = Button(self, text="Start",width=12,bg="bisque", command=self.btnStart_Click)
        self.btnStart.grid(row=27, column=1,columnspan=20,sticky="e")
        self.lblQuestion=Label(self,text="Question",width=12,bg="bisque")
        self.lblQuestion.grid(row=0,column=0,rowspan=4)

        self.lblDigonosis = Label(self, text="Digonosis",width=12,bg="bisque")
        self.lblDigonosis.grid(row=4, column=0,sticky="n",pady=5)

        # self.varQuestion=StringVar()
        self.txtQuestion = Text(self, width=100,height=6, font="bold 16")
        self.txtQuestion.grid(row=0, column=1,rowspan=4,columnspan=20)

        self.varDiagonosis=StringVar()
        self.txtDigonosis =Text(self, width=100,height=19, font='bold 16')
        self.txtDigonosis.grid(row=4, column=1,columnspan=20,rowspan=20,pady=5)

        self.btnNo=Button(self,text="No",width=12,bg="bisque", command=self.btnNo_Click)
        self.btnNo.grid(row=25,column=0)
        self.btnYes = Button(self, text="Yes",width=12,bg="bisque", command=self.btnYes_Click)
        self.btnYes.grid(row=25, column=1,columnspan=20,sticky="e")

        self.btnClear = Button(self, text="Clear",width=12,bg="bisque", command=self.btnClear_Click)
        self.btnClear.grid(row=27, column=0)
        # self.btnStart = Button(self, text="Start",width=12,bg="bisque", command=self.btnStart_Click)
        # self.btnStart.grid(row=27, column=1,columnspan=20,sticky="e")
    def btnNo_Click(self):
        global val,ans
        global val,ans
        ans='no'
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0,END)
        self.txtQuestion.insert(END,str1+"\n")
        
    def btnYes_Click(self):
        global val,ans
        ans='yes'
        messagebox.showinfo("Success", "you want another help to click start")
        self.txtDigonosis.delete(0.0,END)
        str1=QuestionDigonosis.objIter.__next__()
        
#        self.txtDigonosis.insert(END,str1+"\n")
        
    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")                  
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")


class MainForm(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.state("z")
        # master.geometry("350x450")
        master.title("Account Login")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Health Care Chatbot", bg="PeachPuff2", width="300", height="2", font=("Calibri", 13))
        self.lblMsg.pack(pady=20)
        self.btnLogin=Button(self, text="Login", height="2", width="300", command = self.lblLogin_Click, font=("calibri", 13))
        self.btnLogin.pack(pady=20)
        self.btnRegister=Button(self, text="Register", height="2", width="300", command = self.btnRegister_Click, font=("calibri", 13))
        self.btnRegister.pack(pady=20)
        self.lblTeam=Label(self, text="Made by:", bg="slateblue4", width = "250", height = "1", font=("Calibri", 15))
        self.lblTeam.pack()
        self.lblTeam1=Label(self, text="Raushan Raaz", bg="RoyalBlue1", width = "250", height = "1", font=("Calibri", 15))
        self.lblTeam1.pack()
        self.lblTeam2=Label(self, text="Arjun Sharma", bg="RoyalBlue2", width = "250", height = "1", font=("Calibri", 15))
        self.lblTeam2.pack()
        self.lblTeam3=Label(self, text="Nameera Meraj", bg="RoyalBlue3", width = "250", height = "1", font=("Calibri", 15))
        self.lblTeam3.pack()
        # frame = Frame(self,width=600, height=400)
        # frame.pack()
        # frame.place(anchor='center', relx=0.5, rely=0.5)
        # img = ImageTk.PhotoImage(Image.open("forest.jpg"))
        # self.lblimage=Label(frame, image = img)
        # self.lblimage.pack()
        
    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()



        
class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("300x250")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Please enter details below to login",bg="light blue", font=("calibri", 15))
        self.lblMsg.pack(pady=20)
        self.username=Label(self, text="Username * ", font=("calibri", 13))
        self.username.pack(pady=20)
        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify, font=("calibri", 15))
        self.username_login_entry.pack()
        self.password=Label(self, text="Password * ", font=("calibri", 13))
        self.password.pack(pady=20)
        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*', font=("calibri", 15))
        self.password_login_entry.pack()
        # self.lblSucess=Label(self, text="forget password", fg="green", font=("calibri", 11))
        # self.lblSucess.pack()
        self.btnLogin=Button(self, text="Login", width=10, height=2, command=self.btnLogin_Click, font=("calibri", 15))
        self.btnLogin.pack(pady=30)
        self.btnRegister=Button(self, text="Register", height="3", width="300", command = self.btnRegister_Click, font=("calibri", 15))
        self.btnRegister.pack(pady=20)

        # self.btnRegister=Button(self, text="Login", width=10, height=1, command=self.register_user)
        # self.btnRegister.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(Login.main_Root)
        frmSignUp = SignUp(Login.main_Root)
        frmSignUp.pack()

    def btnLogin_Click(self):
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()
        
#        messagebox.showinfo("Failure", self.username1+":"+password1)
        list_of_files = os.listdir()
        # dataset="data.csv"
        # list_of_files = csv.reader(dataset)
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Sucess","Login Sucessful")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
            else:
                messagebox.showinfo("Failure", "Login Details are wrong try again")
        else:
            messagebox.showinfo("Failure", "User not found try from another user\n or sign up for new user")


class SignUp(Frame):
    main_Root=None
    print("SignUp Class")
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        SignUp.main_Root=master
        master.title("Register")
        super().__init__(master=master)
        master.title("Register")
        master.geometry("350x450")
        self.createWidget()
    def createWidget(self):
        self.lblMsg=Label(self, text="Please enter details below", bg="light blue", font=("calibri", 13))
        self.lblMsg.pack(pady=20)
        self.username_lable = Label(self, text="Username * ", font=("calibri", 13))
        self.username_lable.pack(pady=20)
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username, font=("calibri", 15))
        self.username_entry.pack()

        self.fname_lable = Label(self, text="Full Name *", font=("calibri", 13))
        self.fname_lable.pack(pady=20)
        self.fname = StringVar()
        self.fname_entry = Entry(self, textvariable=self.fname, font=("calibri", 15))
        self.fname_entry.pack()

        self.mNumber_lable = Label(self, text="Mobile Number (do not use +91) *", font=("calibri", 13))
        self.mNumber_lable.pack(pady=20)
        self.mNumber = StringVar()
        self.mNumber_entry = Entry(self, textvariable=self.mNumber, font=("calibri", 15))
        self.mNumber_entry.pack()
        

        self.email_lable = Label(self, text="Email *", font=("calibri", 13))
        self.email_lable.pack(pady=20)
        self.email = StringVar()
        self.email_entry = Entry(self, textvariable=self.email, font=("calibri", 15))
        self.email_entry.pack()

        self.password_lable = Label(self, text="Password * ", font=("calibri", 13))
        self.password_lable.pack(pady=20)
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*', font=("calibri", 15))
        self.password_entry.pack()

        self.conform_password_lable = Label(self, text="Conform Password * ", font=("calibri", 13))
        self.conform_password_lable.pack(pady=20)
        self.conform_password = StringVar()
        self.conform_password_entry = Entry(self, textvariable=self.conform_password, show='*', font=("calibri", 15))
        self.conform_password_entry.pack()
        self.btnRegister=Button(self, text="Register", width=10, height=1, bg="light blue", command=self.register_user , font=("calibri", 13))
        self.btnRegister.pack(pady=20)
        # self.btnHome=Button(self, text="Home", width=10, height=1,  command = self.btnHome_Click)
        # self.btnHome.pack()

    def btnHome_Click(self):
        self.destroyPackWidget(SignUp.main_Root)
        frmMainForm = frmMainForm(SignUp.main_Root)
        frmMainForm.pack()

    def register_user(self):
        # mlock=md5(passentry)
        def checkname(fullName):
            if fullName =='':
                messagebox.showwarning("Failure","Enter the Name")
                return FALSE
            if regex_name.search(fullName):
                return True
            else:
                messagebox.showwarning("Failure","Please Enter Valid Name")
                return False
        def checkemail(email):
            if email =='':
                messagebox.showwarning("Failure","Enter the Email ID")
                return FALSE
            if re.fullmatch(regex, email):
                return True
            else:
                messagebox.showwarning("Failure", "Please Enter Valid Email Id")
                return False
        def mob(num):
            # num=int(num)
            if num =='':
                messagebox.showwarning("Failure","Enter the Mobile Number")
                return FALSE
            if len(num)==10:
                num=int(num)
                if num>6123456789:
                    return True
                else:
                    messagebox.showwarning("Failure","Please Enter Valid Mobile Number")
                    return False
            else:
                messagebox.showwarning("Failure","mobile number is nessasry")
                return False
        def checkuser(user):
            if user =='':
                messagebox.showwarning("Failure","Enter the Username")
                return False
            if (len(user) <= 4):
                messagebox.showerror("Failure","Enter Valid User Name /n enter username more than 4 character") 
                return False
#             file=open("data.txt", "r")
#             # if (file==True):
#             for username in file:
#                 if user==username:
#                     messagebox.showerror("Failure",'User Name Already Exist')
#                     print(file.read())
#                     file.close()
#                 return False
                
            else:
                # messagebox.showerror("Failure",'User Name Not valid')
               # file.close()
                return True
        def checkPassword(passEntry,cpassEntry):
            if passEntry =='':
                messagebox.showwarning("Failure","Enter The Password")
                return False
            if passEntry != cpassEntry:
                messagebox.showwarning("Failure","Password Not Match")
                return False
            
            if len(passEntry) < 7:
                messagebox.showerror("Failure","Enter Valid Password")
                return False
            return True

        uentry=self.username_entry.get()
        passentry=self.password_entry.get()
        cpassentry=self.conform_password_entry.get()
        emailentry=self.email_entry.get()
        mobentry=self.mNumber_entry.get()
        fentry=self.fname_entry.get()
#         if checkuser(uentry):
        if checkPassword(passentry,cpassentry) and checkuser(uentry) and mob(mobentry) and checkemail(emailentry) and checkname(fentry):
            # valid = validate_email(emailentry)
            # emailentry = valid.email
            file1 = open("data.txt", "a")
            l = os.listdir()
            if(uentry in l):
                messagebox.showerror("Error","username already exist:")
            else:
                file = open(self.username_entry.get(), "w")
                # file.write(uentry + "," + passentry + ","+ emailentry + "," + mobentry + "," +fentry + "\n" )
                file.write(uentry + "\n" + passentry + "\n"+ emailentry + "\n" + mobentry + "\n" +fentry )
                file1.write(uentry +" \n")
                file.close()


                self.destroyPackWidget(SignUp.main_Root)

                self.lblSucess=Label(root, text="Registration Success", fg="green", font=("calibri", 11))
                self.lblSucess.pack()

                        # frmMainForm.pack()

                        # self.btnSucess=Button(root, text="Click Here to proceed", command=self.btnSucess_Click)
                        # self.btnSucess.pack()

                self.btnLogin=Button(root, text="Login",  command = self.lblLogin_Click)
                self.btnLogin.pack()


    def btnSucess_Click(self):
        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)
        frmQuestion.pack()

    def lblLogin_Click(self):
        self.destroyPackWidget(SignUp.main_Root)
        frmLogin=Login(SignUp.main_Root)
        frmLogin.pack()


root=Tk()

frmMainForm=MainForm(root)
frmMainForm.pack()
root.mainloop()


# In[ ]:




