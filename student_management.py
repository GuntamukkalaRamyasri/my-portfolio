import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------
def add_student():
    name = entry_name.get().strip()
    roll_no = entry_roll.get().strip()
    course = entry_course.get().strip()
    
    if not name or not roll_no or not course:
        messagebox.showwarning("Validation Error", "All fields are required.")
        return
    
    try:
        cursor.execute("INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
                       (name, roll_no, course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        view_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number must be unique.")

def view_students():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to update.")
        return
    
    values = tree.item(selected, "values")
    student_id = values[0]
    name = entry_name.get().strip()
    roll_no = entry_roll.get().strip()
    course = entry_course.get().strip()
    
    if not name or not roll_no or not course:
        messagebox.showwarning("Validation Error", "All fields are required.")
        return
    
    try:
        cursor.execute("""
            UPDATE students SET name=?, roll_no=?, course=? WHERE id=?
        """, (name, roll_no, course, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        clear_entries()
        view_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number must be unique.")

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")
        return
    values = tree.item(selected, "values")
    student_id = values[0]
    
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if confirm:
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Student deleted successfully!")
        clear_entries()
        view_students()

def on_tree_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_roll.delete(0, tk.END)
        entry_roll.insert(0, values[2])
        entry_course.delete(0, tk.END)
        entry_course.insert(0, values[3])

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_course.delete(0, tk.END)

# -----------------------------
# GUI setup
# -----------------------------
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Roll No").grid(row=1, column=0, padx=5, pady=5)
entry_roll = tk.Entry(frame)
entry_roll.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Course").grid(row=2, column=0, padx=5, pady=5)
entry_course = tk.Entry(frame)
entry_course.grid(row=2, column=1, padx=5, pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", width=12, command=add_student).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", width=12, command=update_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_student).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="View All", width=12, command=view_students).grid(row=0, column=3, padx=5)

tree = ttk.Treeview(root, columns=("ID", "Name", "Roll No", "Course"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Roll No", text="Roll No")
tree.heading("Course", text="Course")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_tree_select)

view_students()  # Load existing data on start

root.mainloop()
