import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ==================== FUNCTION TO LOAD SUBJECTS FROM DATABASE ====================
def load_subjects():
    # Clear current list display
    subjects_list.delete(*subjects_list.get_children())
    
    # Connect to the database and create table if it doesn't exist
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS subjects (name TEXT UNIQUE, email TEXT)")
    
    # Fetch all subject records and insert them into the table view
    cursor.execute("SELECT name, email FROM subjects")
    for row in cursor.fetchall():
        subjects_list.insert("", "end", values=row)
    
    conn.close()

# ==================== FUNCTION TO ADD NEW SUBJECT ====================
def add_subject():
    subject = subject_entry.get().strip()
    email = email_entry.get().strip()

    # Validate input
    if not subject or not email:
        messagebox.showwarning("Missing Info", "Please fill in both subject and email.")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    try:
        # Try inserting new subject and email
        cursor.execute("INSERT INTO subjects (name, email) VALUES (?, ?)", (subject, email))
        conn.commit()
        load_subjects()  # Refresh the table view
        messagebox.showinfo("Success", f"Subject '{subject}' added.")
        subject_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        # Catch duplicate subjects
        messagebox.showerror("Error", f"Subject '{subject}' already exists.")
    conn.close()

# ==================== FUNCTION TO UPDATE PROFESSOR EMAIL ====================
def update_email():
    selected = subjects_list.selection()
    if not selected:
        messagebox.showwarning("Select Subject", "Please select a subject to update.")
        return

    # Get selected subject
    item = subjects_list.item(selected[0])
    subject = item["values"][0]
    new_email = email_entry.get().strip()

    if not new_email:
        messagebox.showwarning("Missing Email", "Please enter a new email address.")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE subjects SET email = ? WHERE name = ?", (new_email, subject))
    conn.commit()
    conn.close()

    load_subjects()  # Refresh table
    messagebox.showinfo("Updated", f"Email for '{subject}' updated.")

# ==================== FUNCTION TO DELETE SUBJECT ====================
def delete_subject():
    selected = subjects_list.selection()
    if not selected:
        messagebox.showwarning("Select Subject", "Please select a subject to delete.")
        return

    item = subjects_list.item(selected[0])
    subject = item["values"][0]

    # Confirm deletion
    confirm = messagebox.askyesno("Confirm Delete", f"Delete subject '{subject}'?")
    if not confirm:
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE name = ?", (subject,))
    conn.commit()
    conn.close()

    load_subjects()  # Refresh the table
    messagebox.showinfo("Deleted", f"Subject '{subject}' deleted.")

# ==================== GUI SETUP ====================
root = tk.Tk()
root.title("Manage Subjects and Professor Emails")
root.geometry("500x450")
root.configure(bg="#f0f0f0")

# Subject name entry
tk.Label(root, text="Subject Name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
subject_entry = tk.Entry(root, font=("Arial", 12))
subject_entry.pack()

# Professor email entry
tk.Label(root, text="Professor Email:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
email_entry = tk.Entry(root, font=("Arial", 12))
email_entry.pack()

# Buttons for add, update, delete
tk.Button(root, text="Add Subject", command=add_subject, font=("Arial", 12), bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Update Email", command=update_email, font=("Arial", 12), bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Delete Subject", command=delete_subject, font=("Arial", 12), bg="red", fg="white").pack(pady=5)

# Table to show subjects and emails
columns = ("Subject", "Email")
subjects_list = ttk.Treeview(root, columns=columns, show="headings")

# Set column headers
for col in columns:
    subjects_list.heading(col, text=col)

subjects_list.pack(pady=10, expand=True, fill="both")

# Load initial data
load_subjects()

# Start GUI event loop
root.mainloop()
