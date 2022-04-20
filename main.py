import sqlite3
import tkinter as tk
import tksheet
from tkinter import N, S, E, W
from tkinter import TOP, BOTTOM, LEFT, RIGHT, END, ALL
from tkinter import *
from tkinter import ttk
import pandas as pd
import plotly.express as px
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



'''
DATABASE
'''
id_list = []
amount_list = []
category_list = []
dates_list = []
#Connect to SQL
con = sqlite3.connect('expensedb.db')
cursor = con.cursor()

#Create Table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses           
              (id integer PRIMARY KEY autoincrement, amount integer, category text, expense_date text)''') #if the database is already created it will pass this, if the database is not created for example a new user then the database will be created

con.commit()

#This Function Will Delete the selected itemm from the tree view and the Database!
def Delete():
    conn = sqlite3.connect("expensedb.db")
    cur = conn.cursor()
    for selected_item in my_tree.selection():
        print(selected_item)  # it prints the selected row id
        cur.execute("DELETE FROM expenses WHERE id=?", (my_tree.set(selected_item, '#1'),))
        conn.commit()
        my_tree.delete(selected_item)
        con.commit()

def query_db():
    for record in my_tree.get_children(): #Deletes every record
        my_tree.delete(record)

    cursor.execute("SELECT * from expenses")
    records = cursor.fetchall()
    for record in records: #we will then reinsert all records after deleting each records so that we can update the tree table to see the new ones
        my_tree.insert(parent='', index='end',text='', values=(record))
    con.commit()


'''
GRAB record
'''
def select_record(): #Will Focus on the clicked record within the tree
    selected = my_tree.focus()
    #Grab record values
    values = my_tree.item(selected, 'values')

#Add Data
def add_data():
    try:

        cursor.execute("INSERT INTO expenses VALUES(?, ?, ?, ?)", (id_entry.get().upper(), amount_entry.get().upper(), category_entry.get().upper(), date_entry.get())) #Insert the entries into the actual database
        con.commit()

    except:
        error_label['text'] = 'Error with Entry'

    #Clear the tree view tabe
    my_tree.delete(*my_tree.get_children()) #Once that is done we will delete the table

    query_db() #This will then refresh the tree record at the end





'''
GUI GUI GUI
'''
root = tk.Tk()
root.title('Expense Tracker')
root.geometry('1000x800')
root.resizable(False, False)

db = 'expensedb.sqlite'
tbl = 'bar'


#Tab
tabControl = ttk.Notebook(root)
data = ttk.Frame(tabControl)
tabControl.add(data, text='Data')
tabControl.pack(expand = 1, fill = 'both')


frame = tk.Frame(data, bg='gray', height=800, width=1000)
frame.pack()


title = tk.LabelFrame(frame, bg='black', width=500, height=100)
title.place(relx=.05, rely=0.05)
title_text = tk.Label(title, text='Expense Tracker', font='Helvetica 12 bold', justify='center')
title_text.place(relx=0.01, rely=0.25, relwidth=1)
id_label = tk.Label(frame, bg='gray', text='ID', font='Helvetica 10 bold')
id_label.place(relx=0.15, rely=0.65)
id_entry = tk.Entry(frame)
id_entry.place(relx=0.20, rely=0.65)

error_label = tk.Label(title, bg='black', fg='white')
error_label.place(relx=0.42, rely=0.65)



amount_label = tk.Label(frame, bg='gray', text='Amount', font='Helvetica 10 bold')
amount_label.place(relx=0.48, rely=0.65)
amount_entry = tk.Entry(frame)
amount_entry.place(relx=0.70, rely=0.65)




category_label = tk.Label(frame, bg='gray', text='Category', font='Helvetica 10 bold')
category_label.place(relx=0.07, rely=0.70)
category_entry = tk.Entry(frame)
category_entry.place(relx=0.20, rely=0.70)

date_label = tk.Label(frame, bg='gray', text='Date', font='Helvetica 10 bold')
date_label.place(relx=0.48, rely=0.70)
date_entry = tk.Entry(frame)
date_entry.place(relx=0.60, rely=0.70)


add_btn = tk.Button(frame, bg='black', fg='white', text='Add Expense', command=lambda :add_data())
add_btn.place(relx=0.40, rely=0.90, relwidth=0.20)

button = tk.Button(frame, bg='black', fg='white', text='Delete', command=lambda: [Delete(), query_db()])
button.place(relx=0.40, rely=0.84, relwidth=0.20)

plot_btn = tk.Button(frame, bg='black', fg='white', text='Check out most spent category!', command=lambda :plot())
plot_btn.place(relx=0.34, rely=0.95)

#Creating The tree view so the user can visualize their entries
my_tree = ttk.Treeview(frame)
my_tree['columns'] = ('ID', 'Amount', 'Category', 'Date')
#Formate Columns
my_tree.column('#0', width=20, minwidth=25)
my_tree.column('ID', anchor=W, width=120)
my_tree.column('Amount', anchor=CENTER, width=120)
my_tree.column('Category', anchor=W, width=120)
my_tree.column('Date', anchor=E, width=140)


'''
GRABBING RECORDS AND PLACING THEM INTO THE TREE
'''
#Grab All RECORDS
#cursor.execute("SELECT * from expenses")
#records = cursor.fetchall()


#Create headings
my_tree.heading('#0')
my_tree.heading('ID', text='ID', anchor=W)
my_tree.heading('Amount', text='Amount', anchor=CENTER)
my_tree.heading('Category', text='Category', anchor=W)
my_tree.heading('Date', text='Date', anchor=E)





#Add Data
#def add_data():
    #my_tree.insert(parent='', index='end',text='Test', values=(#entry.get, #entry.get, #entry.get))


my_tree.pack(pady=300, padx=20)
query_db()

def plot():

    #Put all data into seperate lists               #WE WILL USE THESE TO PLOT CEARTIN THINGS
    cursor.execute('SELECT id FROM expenses')
    ids = cursor.fetchall()
    for id in ids:
        id_list.append(id)

    cursor.execute('SELECT amount FROM expenses')
    amounts = cursor.fetchall()
    for amount in amounts:
        amount_list.append(amount)

    cursor.execute('SELECT category FROM expenses')
    categories = cursor.fetchall()
    for category in categories:
        category_list.append(' '.join(category))
    cursor.execute('SELECT expense_date FROM expenses')
    dates = cursor.fetchall()
    for date in dates:
        dates_list.append(' '.join(date))
    df = pd.DataFrame()
    df.insert(loc=0, column='ID', value=id_list)
    df.insert(loc=1, column='Amount', value=amount_list)
    df.insert(loc=2, column='Category', value=category_list)
    df.insert(loc=3, column='Date', value=category_list)

    category_types = df['Category'].value_counts()

    fig = px.pie(labels=category_types.index, values=category_types.values, title='Categories I spend money on',
                 names=category_types.index)
    fig.update_traces(textposition='outside', textinfo='percent+label')

    fig.show()




root.mainloop()
