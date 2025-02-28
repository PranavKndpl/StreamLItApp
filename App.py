import streamlit as st
import sqlite3 #freecode camp
from streamlit_option_menu import option_menu

def connect_db():
    conn = sqlite3.connect("mydb.db")
    return conn

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    # create_table_query = '''
    # CREATE TABLE IF NOT EXISTS Students (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     age INTEGER,
    #     email TEXT
    # );
    # '''
    cur.execute("CREATE TABLE IF NOT EXISTS Student(name text,password text,roll int primary key,branch text)")
    conn.commit()
    conn.close()

def addRecord(data):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Student(name,Password,roll,branch) values(?,?,?,?)",data)
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("user already exists")
        conn.close()
    else:
        st.success("User registered succesfully") #st.success(data)

def view_record():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Student")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def display():
    data = view_record()
    # st.write(data)

    headers = ["Name", "Password", "Roll Number", "Branch"]

    data_dicts = [
        {headers[0]: row[0], headers[1]: row[1], headers[2]: row[2], headers[3]: row[3]}
        for row in data
    ]

    st.table(data_dicts)

    # st.table(data)

def signup():
    st.title("Registration Page")
    name = st.text_input("Enter your user Name")
    Password = st.text_input("Enter your user Password",type="password")
    Repass = st.text_input("Enter your Password again",type="password")
    roll = st.text_input("Enter your user Roll Number",max_chars=7)
    
    branch = st.selectbox("Select Branch",options=["","CSE","CSE-Aiml","CSIT","ECE"])

    st.radio("Gender",options=["Male","Female"])


    if roll and not roll.isdigit():
        st.error("Roll number must be numeric.")

    if st.button("Sign-Up"):
        if Password != Repass:
            st.error("Password do not match.")
        else:
            addRecord((name,Password,roll,branch))
   

create_table()

with st.sidebar:
    selected = option_menu('Navigation', ['Sign-Up', 'Sign In', 'Search User', 'Reset Password', 'Delete User', 'View All'])

if selected == "Sign-Up":
    signup()


else:
    display()


# reset pass, delete user,delete student record, search record
