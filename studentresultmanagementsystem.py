#Library import
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import mysql.connector

#Connect MySQL database
def connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="edutech",
        port=3306
    )
    return conn, conn.cursor()

#Calculate total marks and grade
def calculate_grade():
    try:
        m1 = int(mark1_entry.get())
        m2 = int(mark2_entry.get())
        m3 = int(mark3_entry.get())
        m4 = int(mark4_entry.get())
        m5 = int(mark5_entry.get())

        total = m1 + m2 + m3 + m4 + m5

        if total >= 450:
            grade = "A"
        elif total >= 350:
            grade = "B"
        elif total >= 250:
            grade = "C"
        else:
            grade = "F"

        total_mark_entry.config(state="normal")
        grade_entry.config(state="normal")

        total_mark_entry.delete(0, END)
        grade_entry.delete(0, END)

        total_mark_entry.insert(0, total)
        grade_entry.insert(0, grade)

        total_mark_entry.config(state="readonly")
        grade_entry.config(state="readonly")

        return total, grade

    except ValueError:
        messagebox.showerror("Error", "Please enter valid marks")
        return None, None

#Add student details and save to database
def add_student():
    try:
        total, grade = calculate_grade()
        if total is None:
            return

        conn, cursor = connection()

        name = stu_name_entry.get()

        cursor.execute(
            "INSERT INTO students (name, total_marks, grade) VALUES (%s, %s, %s)",
            (name, total, grade)
        )

        student_id = cursor.lastrowid

        marks = [
            ("Subject1", int(mark1_entry.get())),
            ("Subject2", int(mark2_entry.get())),
            ("Subject3", int(mark3_entry.get())),
            ("Subject4", int(mark4_entry.get())),
            ("Subject5", int(mark5_entry.get()))
        ]

        for subject, mark in marks:
            cursor.execute(
                "INSERT INTO marks (student_id, subject_name, marks) VALUES (%s, %s, %s)",
                (student_id, subject, mark)
            )

        conn.commit()
        conn.close()

        load_students()
        messagebox.showinfo("Success", "Student added and grade calculated successfully")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

#Clear all rows in Treeview
def clear_tree():
    for item in my_tree.get_children():
        my_tree.delete(item)  

#Load student records from database
def load_students():
    clear_tree()
    conn, cursor = connection()

    query = """
    SELECT 
        s.student_id,
        s.name,
        MAX(CASE WHEN m.subject_name='Subject1' THEN m.marks END),
        MAX(CASE WHEN m.subject_name='Subject2' THEN m.marks END),
        MAX(CASE WHEN m.subject_name='Subject3' THEN m.marks END),
        MAX(CASE WHEN m.subject_name='Subject4' THEN m.marks END),
        MAX(CASE WHEN m.subject_name='Subject5' THEN m.marks END),
        s.total_marks,
        s.grade
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    GROUP BY s.student_id, s.name, s.total_marks, s.grade
    ORDER BY s.student_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        my_tree.insert("", END, values=row)

#Display selected student data in input fields
def selectData(event=None):
    selected = my_tree.selection()
    if not selected:
        return
    values = my_tree.item(selected[0])['values']

    reset()

    stu_id_entry.config(state="normal")
    stu_id_entry.insert(0, values[0])
    stu_name_entry.insert(0, values[1])
    mark1_entry.insert(0, values[2])
    mark2_entry.insert(0, values[3])
    mark3_entry.insert(0, values[4])
    mark4_entry.insert(0, values[5])
    mark5_entry.insert(0, values[6])
    total_mark_entry.config(state="normal")
    total_mark_entry.insert(0, values[7])
    grade_entry.config(state="normal")
    grade_entry.insert(0, values[8])
    stu_id_entry.config(state="readonly")
    total_mark_entry.config(state="readonly")
    grade_entry.config(state="readonly")


#Clears all input fields
def reset():
    stu_id_entry.config(state="normal")
    stu_id_entry.delete(0,END)
    stu_name_entry.delete(0,END)
    mark1_entry.delete(0,END)
    mark2_entry.delete(0,END)
    mark3_entry.delete(0,END)
    mark4_entry.delete(0,END)
    mark5_entry.delete(0,END)
    total_mark_entry.config(state="normal")
    total_mark_entry.delete(0,END)
    grade_entry.config(state="normal")
    grade_entry.delete(0,END)
    stu_id_entry.config(state="readonly")
    total_mark_entry.config(state="readonly")
    grade_entry.config(state="readonly")


#Create main application window
root = tk.Tk()
root.title("Student result management system")
root.geometry("1200x700")

#Main label
mainLabel = tk.Label(root,text="Student result management system",font=("Arial Bold",30),fg="blue")
mainLabel.grid(row=0, column=0, columnspan=8, rowspan=2, padx=270, pady=30)

#Create labels
stu_id = tk.Label(root,text="Student ID",font=("Arial Bold", 15))
stu_id.grid(row=3,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

stu_name = tk.Label(root,text="Student Name",font=("Arial Bold", 15))
stu_name.grid(row=5,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

mark1 = tk.Label(root,text="Mark 1",font=("Arial Bold", 15))
mark1.grid(row=7,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

mark2 = tk.Label(root,text="Mark 2",font=("Arial Bold", 15))
mark2.grid(row=9,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

mark3 = tk.Label(root,text="Mark 3",font=("Arial Bold", 15))
mark3.grid(row=11,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

mark4 = tk.Label(root,text="Mark 4",font=("Arial Bold", 15))
mark4.grid(row=13,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

mark5 = tk.Label(root,text="Mark 5",font=("Arial Bold", 15))
mark5.grid(row=15,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

total_mark = tk.Label(root,text="Total mark",font=("Arial Bold", 15))
total_mark.grid(row=17,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

grade = tk.Label(root,text="Grade",font=("Arial Bold", 15))
grade.grid(row=19,column=0,columnspan=1,rowspan=1,padx=70,pady=5)

#Inputs
stu_id_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5,state="readonly")
stu_id_entry.grid(row=3,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

stu_name_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
stu_name_entry.grid(row=5,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

mark1_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
mark1_entry.grid(row=7,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

mark2_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
mark2_entry.grid(row=9,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

mark3_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
mark3_entry.grid(row=11,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

mark4_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
mark4_entry.grid(row=13,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

mark5_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5)
mark5_entry.grid(row=15,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

total_mark_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5,state="readonly")
total_mark_entry.grid(row=17,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

grade_entry = tk.Entry(root,font=("Arial Bold",15),width=50,bd=5,state="readonly")
grade_entry.grid(row=19,column=1,columnspan=1,rowspan=1,padx=0,pady=0)

#Create buttons
addbtn = tk.Button(root,text="Add Student",font=("Arial Bold",12),width=20,command=add_student)
addbtn.grid(row=7,column=3,columnspan=1,rowspan=1,padx=20)

savebtn = tk.Button(root,text="Reload",font=("Arial Bold",12),width=20,command=reset)
savebtn.grid(row=9,column=3,columnspan=1,rowspan=1,padx=20)

exitbtn = tk.Button(root,text="Exit",font=("Arial Bold",12),width=20,command=root.destroy)
exitbtn.grid(row=11,column=3,columnspan=1,rowspan=1,padx=20)

#Create a tree view (for display data)
my_tree = ttk.Treeview(root)
style = ttk.Style()
style.configure("Treeview.Heading",background="#ffffff", foreground="#000000",font=("Arial Bold",15))

my_tree['columns'] = (
    "Student ID", "Student Name",
    "Mark1", "Mark2", "Mark3", "Mark4", "Mark5",
    "Total Mark", "Grade"
)

my_tree.column("#0", width=0, stretch=tk.NO)
my_tree.column("Student ID", width=130, anchor="center")
my_tree.column("Student Name", width=250, anchor="center")
my_tree.column("Mark1", width=100, anchor="center")
my_tree.column("Mark2", width=100, anchor="center")
my_tree.column("Mark3", width=100, anchor="center")
my_tree.column("Mark4", width=100, anchor="center")
my_tree.column("Mark5", width=100, anchor="center")
my_tree.column("Total Mark", width=120, anchor="center")
my_tree.column("Grade", width=80, anchor="center")

my_tree.heading("Student ID", text="Student ID", anchor="center")
my_tree.heading("Student Name", text="Student Name", anchor="center")
my_tree.heading("Mark1", text="Mark 1", anchor="center")
my_tree.heading("Mark2", text="Mark 2", anchor="center")
my_tree.heading("Mark3", text="Mark 3", anchor="center")
my_tree.heading("Mark4", text="Mark 4", anchor="center")
my_tree.heading("Mark5", text="Mark 5", anchor="center")
my_tree.heading("Total Mark", text="Total Mark", anchor="center")
my_tree.heading("Grade", text="Grade", anchor="center")
my_tree.heading("Grade",text="Grade",anchor="center")

my_tree.grid(row=20, column=0, padx=20, pady=40, columnspan=8,rowspan=8)

my_tree.bind("<ButtonRelease-1>", selectData)

load_students()

#execute
root.mainloop()