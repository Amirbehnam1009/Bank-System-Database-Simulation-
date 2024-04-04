import pyodbc
import datetime
import bcrypt
import tkinter 
from tkinter import messagebox 
_password =b'$2b$12$r6YcluRcDnHSU8n74j7RnO'
# a = bcrypt.hashpw("a".encode(), _password)
# print(a)
# a = bcrypt.hashpw("b".encode(), _password)
# print(a)
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=.;Database=bank;UID=sa;PWD=123;'
def test():
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        print("Connected successfully!")
    except Exception as e:
        print(f"Error: {e}")

def getType(type):
    if type == 1:
        return "card"
    if type == 2:
        return "satna"
    if type == 3:
        return "paya"
    

def getLimit(type):
    if type == 1:
        return 10000000
    if type == 2:
        return 50000000
    if type == 3:
        return 10000000000
def getStatus(type):
    if type == 1:
        return "ok"
    if type == 2:
        return "error - not enough money"
    if type == 3:
        return "error - limit"
def getW(title):
    c = tkinter.Tk()
    c.title(title)
    c.geometry("600x600")
    c['pady'] = 50
    c['pady'] = 50
    return c


def printAccountTransactionsW(account):
    c = getW('Account Transactions')
    tkinter.Label(c, text= "how many transactions to show? ").pack(pady=5)
    count = tkinter.Entry( c, width=80 )
    count.pack(pady=5)
    tkinter.Button(c, text='go!',bg="#008CBA", command=lambda: printAccountTransactions(c, account, int(count.get()))).pack(pady=5)

def printAccountTransactions(m:tkinter,account, i):
    #i = int(input("how many transactions you want to see?"))
    m.destroy()
    c = getW('Account Transactions')
    query = "select top({1}) [Id],[From],[To],[Money],[Type],[DateTime],[Status] from [dbo].[Transactions] where [from] = '{0}' or [to] = '{0}' order by  [DateTime] desc"
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query.format(account, i))
    all = cursor.fetchall()

    tkinter.Label(c, text= "id ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 0, pady = 2)
    tkinter.Label(c, text= "from ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 1, pady = 2)
    tkinter.Label(c, text= "to ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 2, pady = 2)
    tkinter.Label(c, text= "money ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 3, pady = 2)
    tkinter.Label(c, text= "type ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 4, pady = 2)
    tkinter.Label(c, text= "datetime ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 5, pady = 2)
    tkinter.Label(c, text= "status ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 6, pady = 2)
    for index, x in enumerate(all):
        tkinter.Label(c, text= x[0]) .grid(row = index+1, column = 0, pady = 2)
        tkinter.Label(c, text= x[1]) .grid(row = index+1, column = 1, pady = 2)
        tkinter.Label(c, text= x[2]) .grid(row = index+1, column = 2, pady = 2)
        tkinter.Label(c, text= x[3]) .grid(row = index+1, column = 3, pady = 2)
        tkinter.Label(c, text= getType(x[4])) .grid(row = index+1, column = 4, pady = 2)
        tkinter.Label(c, text= x[5]) .grid(row = index+1, column = 5, pady = 2)
        tkinter.Label(c, text= getStatus(x[6])) .grid(row = index+1, column = 6, pady = 2)
def getaccount(nationalcode, fr):
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute("select top(1) id from  [dbo].[Accounts] where id = '{0}' and nationalcode = '{1}'".format(fr, nationalcode))
    res = cursor.fetchval()
    if res:
        return res
    return None
def transferW(m:tkinter,fr,type):
    c = getW("from:{0}".format(fr))
    tkinter.Label(c, text= "money") .pack(pady=5)
    money = tkinter.Entry( c, width=80 )
    money.pack(pady=5)
    
    tkinter.Label(c, text= "from:{0}".format(fr)) .pack(pady=5)
    tkinter.Label(c, text= "to") .pack(pady=5)
    to = tkinter.Entry( c, width=80 )
    to.pack(pady=5)
    tkinter.Button(c, text='go!', bg="#008CBA", command=lambda: transfer(c,fr,to.get(),type, money.get())).pack(pady=5)
    m.destroy()
def transfer(m:tkinter.Tk,fr,to, type, money):
    if not money:
        messagebox.showerror("transfer","money is invalid")
    money = int(money)
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    
    types =  "CardNumber"
    if type==3 or type == 2:
        types = "Sheba"
    cursor.execute("select id from  [dbo].[Accounts] where [{1}] = '{0}'".format(to, types))
    res = cursor.fetchval()
    if  not res:
        messagebox.showerror("transfer","wrong destination")
        return False
    to = res


    query = "select SUM([money]) from  [dbo].[Transactions] where [from] = '{0}' and [datetime] < '{1}' and type = {2}"
    cnxn = pyodbc.connect(connection_string)
    
    now = datetime.datetime.utcnow()
    cursor.execute(query.format(fr, now.strftime('%Y-%m-%d 00:00:00'), type))
    sum = cursor.fetchval()
    if not sum:
        sum = 0
    
    query = "select [money] from  [dbo].[Accounts] where [Id] = '{0}'"
    cursor.execute(query.format(fr))
    exsistingMoney = int(cursor.fetchval())

    if money > exsistingMoney:
        messagebox.showerror("transfer"," not enough money")
        query = "INSERT INTO [dbo].[Transactions] ([From],[To],[Money],[Type],[DateTime],[Status])VALUES('{0}','{1}',{2},{3},'{4}',{5})".format(fr,to,money,type,now,2)
        cursor.execute(query)
        cursor.commit()
        return False
    if money + sum > getLimit(type):
        messagebox.showerror("transfer","you read the limit")
        query = "INSERT INTO [dbo].[Transactions] ([From],[To],[Money],[Type],[DateTime],[Status])VALUES('{0}','{1}',{2},{3},'{4}',{5})".format(fr,to,money,type,now,3)
        cursor.execute(query)
        cursor.commit()
        return False
    query = "INSERT INTO [dbo].[Transactions] ([From],[To],[Money],[Type],[DateTime],[Status])VALUES('{0}','{1}',{2},{3},'{4}',{5}); ".format(fr,to,money,type,now,1)
    cursor.execute(query)
    cursor.commit()
    cursor.execute("select  IDENT_CURRENT('[dbo].[Transactions]')")
    id = cursor.fetchval() 
    cursor.execute("update [dbo].[Accounts] set [Money] = ([Money] -{2}) where id = '{0}';update [dbo].[Accounts] set [Money] = ([Money] +{2}) where id = '{1}';".format(fr,to, money))
    cursor.commit()
    messagebox.showinfo("transfer","ok! your code is: {0}".format(id))
    m.destroy()
    return True
def addAccountW(nationalcode):
    c = getW('add Account')
    tkinter.Label(c, text="Money:").pack(pady=5)
    money = tkinter.Entry( c, width=80 )
    money.pack(pady=5)
    tkinter.Button(c, text='Add account', bg="#04AA6D", width=50, command=lambda:  addAccount(c,nationalcode, money.get())).pack(pady=5)
    m.mainloop()
def addAccount(m:tkinter.Tk, nationalcode, money):
    query = "INSERT INTO [dbo].[Accounts] ([NationalCode],[CardNumber],[Sheba],[money]) VALUES ('{0}','','','{1}')"
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query.format(nationalcode, money))
    cursor.commit()
    messagebox.showinfo("Add account","OK!")
    m.destroy()
def viewAllAccountW(m:tkinter.Tk, nationalcode):
    all = getAllAccount(nationalcode)
    c = getW('accounts')
    tkinter.Label(c, text= "account id ",font=('Arial',14,'bold') ,  borderwidth=2, relief="groove").grid(row = 0, column = 0, pady = 2)
    tkinter.Label(c, text= "cardnumber      ",font=('Arial',14,'bold')  ,  borderwidth=2, relief="groove").grid(row = 0, column = 1, pady = 2)
    tkinter.Label(c, text= "sheba                   ",font=('Arial',14,'bold')  ,  borderwidth=2, relief="groove").grid(row = 0, column = 2, pady = 2)
    tkinter.Label(c, text= "money         ",font=('Arial',14,'bold')  ,  borderwidth=2, relief="groove").grid(row = 0, column = 3, pady = 2)
    for index, x in enumerate(all):
        tkinter.Label(c, text= x[0]) .grid(row = 2*index+1, column = 0, pady = 2)
        tkinter.Label(c, text= x[1] ) .grid(row = 2*index+1, column = 1, pady = 2 )
        tkinter.Label(c, text= x[2]) .grid(row = 2*index+1, column = 2, pady = 2 )
        tkinter.Label(c, text= x[3]) .grid(row = 2*index+1, column = 3, pady = 2 )

        tkinter.Button(c, text='card to card', command=lambda a=x[0]:transferW(c,a,1)).grid(row = 2*index+2, column = 0, pady = 2 )
        tkinter.Button(c, text='satna', command=lambda a=x[0]:transferW(c,a,2)).grid(row = 2*index+2, column = 2, pady = 2 )
        tkinter.Button(c, text='paya', command=lambda a=x[0]:transferW(c,a,3)).grid(row = 2*index+2, column = 1, pady = 2 )

        tkinter.Button(c, text='transactions', command=lambda a=x[0]:printAccountTransactionsW(a)).grid(row = 2*index+2, column = 3, pady = 2 )
    c.protocol("WM_DELETE_WINDOW", lambda:openclose(m,c))


def getAllAccount(nationalcode):
    query = "select [Id],[CardNumber],[Sheba],[Money] from [dbo].[Accounts] where nationalcode = '{0}'"
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query.format(nationalcode))
    all = cursor.fetchall()
    #print("Account Number       cardNumber                    Sheba    Money($)")
    #print("#{0:13} {1:16} {2:24}   {3}$".format(x[0],x[1],x[2],x[3]))
    cnxn.close()
    return all

def viewSingleTransactionW(nationalcode):
    c = getW('viewSingleTransaction')
    tkinter.Label(c, text= "transaction code? ").pack(pady=5)
    id = tkinter.Entry( c, width=80 )
    id.pack(pady=5)
    my_string_var = tkinter.StringVar()
    my_string_var.set('------------------------------')
    res = tkinter.Label(c, text=  "----------------------")
    res.pack(pady=5)
    
    tkinter.Button(c, text='go!',bg="#f44336", command=lambda: res.config(text = viewSingleTransaction(nationalcode,int(id.get()))) ).pack(pady=5)
    #tkinter.Button(c, text='go!', command=lambda my_string_var = my_string_var: my_string_var.set("hi") ).pack(pady=5)


def viewSingleTransaction(nationalcode, id):
    query = "select top(1) [Id],[From],[To],[Money],[Type],[DateTime],[Status] from [dbo].[Transactions] where [id] = {0}  and ([from] in (select id from [dbo].[Accounts] where  [dbo].[Accounts].[NationalCode] = '{1}' ) or [to] in (select id from [dbo].[Accounts] where  [dbo].[Accounts].[NationalCode] = '{1}' ) )".format(id, nationalcode )
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    if row:
        return "id:{0} from:{1}, to:{2}, money:{3}, type:{4}, datetime:{5}, status:{6}".format(row[0],row[1],row[2],row[3],getType(row[4]),row[5],getStatus(row[6]))
    return "not found"
def login(m:tkinter.Tk, nationalcode, password):
    query = "select top (1) [NationalCode],[name],[lastname] from [dbo].[Users] where [NationalCode] = '{0}' and [Password]='{1}'"
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query.format(nationalcode, bcrypt.hashpw(password.encode(), _password).decode()))
    row = cursor.fetchone()
    cnxn.close()

    if row:
        messagebox.showinfo("login","you logged in!")
        m.withdraw()
        c = getW("welcome {0} {1}".format(row[1],row[2]))
        tkinter.Button(c, text='add account',bg="#04AA6D", width=50, command=  lambda:addAccountW(nationalcode) ).pack(pady=5)
        tkinter.Button(c, text='view accounts', bg="#008CBA" , width=50, command=  lambda: viewAllAccountW(c,nationalcode)).pack(pady=5)
        tkinter.Button(c, text='view Single Transaction', bg="#f44336",width=50, command=  lambda: viewSingleTransactionW(nationalcode)).pack(pady=5)
        return True
    else :
        messagebox.showerror("login","national code or password is wrong")
        return False

def registerW():
    c = getW("register")
    tkinter.Label(c, text= "name") .pack(pady=5)
    name = tkinter.Entry( c, width=80)
    name.pack(pady=5)
    tkinter.Label(c, text= "lastname") .pack(pady=5)
    lastname = tkinter.Entry( c, width=80)
    lastname.pack(pady=5)

    tkinter.Label(c, text= "nationalcode") .pack(pady=5)
    nationalcode = tkinter.Entry( c, width=80)
    nationalcode.pack(pady=5)

    tkinter.Label(c, text= "password") .pack(pady=5)
    password = tkinter.Entry( c, width=80)
    password.pack(pady=5)
    tkinter.Button(c, text='register',bg="#04AA6D", command=  lambda:register(c, name.get(),lastname.get(),nationalcode.get(),password.get()) ).pack(pady=5)
    c.mainloop()


def register(m:tkinter.Tk,name,lastname,nationalcode,password ):
    if not name:
        messagebox.showerror("transfer","money is invalid")
        return
    if not lastname:
        messagebox.showerror("transfer","lastname is invalid")
        return
    if not nationalcode:
        messagebox.showerror("transfer","nationalcode is invalid")
        return
    if not password:
        messagebox.showerror("transfer","password is invalid")
        return

    try:
       query = "INSERT INTO [dbo].[Users] ([NationalCode] ,[Name] ,[LastName] ,[Password]) VALUES ('{0}','{1}','{2}','{3}')"
       cnxn = pyodbc.connect(connection_string)
       cursor = cnxn.cursor()
       cursor.execute(query.format(nationalcode, name,lastname, bcrypt.hashpw(password.encode(), _password).decode()))
       cursor.commit()
       messagebox.showinfo("registre","Done, please login!")
       m.destroy()
    except Exception as e:
       messagebox.showerror(f"***Error: {e}")
    cnxn.close()
def openclose(a:tkinter.Tk,b:tkinter.Tk):
    a.deiconify()
    b.destroy()
def loginW(m:tkinter.Tk):
    m.withdraw()
    c=getW('login')
    c.protocol("WM_DELETE_WINDOW", lambda:openclose(m,c))
   

    tkinter.Label(c, text="National Code:").pack(pady=5)
    entry = tkinter.Entry( c, width=80 )
    entry.pack(pady=5)
    tkinter.Label(c, text="password:").pack(pady=5)
    entry2 = tkinter.Entry( c, width=80 )
    entry2.pack(pady=5)
    tkinter.Button(c, text='login',bg="#04AA6D", width=50, command=  lambda: login(c,entry.get(),entry2.get())).pack(pady=5)
    c.mainloop()




m=getW('Banking system')
button = tkinter.Button(m, text='Login',bg="#04AA6D", width=50, command=lambda: loginW(m)).pack(pady=5)
button = tkinter.Button(m, text='Register',bg="#008CBA", width=50, command=lambda: registerW()).pack(pady=5)
m.mainloop()









# while(True):
#     i = input('1)register\n2)login  ')
#     if i == '1':
#         register()
#     if i == '2':
#         nationalcode = login()
#         if nationalcode:
#             while(True):
#                 i = input('1)add account\n2)view all Accounts\n3)select account\n0)log out  ')
#                 if i == '1':
#                     addAccount(nationalcode)
#                 if i == '2':
#                     viewAllAccount(nationalcode)
#                 if i == '3':
#                     viewAllAccount(nationalcode)
#                     i = input("account number: ")
#                     account = getaccount(nationalcode,i)
#                     if account:
#                         while(True):
#                             i = input('1)card to card\n2)satna\n3)paya\n4)view all transactions\n0)back ')
#                             if i =='1':
#                                 transfer(account, input("to"),1)
#                             if i =='2':
#                                 transfer(account, input("to"),2)
#                             if i =='3':
#                                 transfer(account, input("to"),3)
#                             if i =='0':
#                                 break
#                             if i =='4':
#                                 printAccountTransactions(account)
#                     else:
#                         print("***account not found")
#                 if i =='0':
#                     break
#         else :
#             print("***user not found")
    


    





