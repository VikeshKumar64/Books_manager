import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vikesh@1234",
            database="vikeshdb"
        )
        return db
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# ---------------- LOGIN WINDOW ----------------
def login_window():
    def check_login():
        username = user_entry.get()
        password = pass_entry.get()

        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            db.close()

            if result:
                messagebox.showinfo("Success", "Login Successful!")
                root.destroy()
                main_window()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")

    root = tk.Tk()
    root.title("Library Login")
    root.geometry("350x250")
    root.config(bg="#e0f7fa")

    tk.Label(root, text="Username:", bg="#e0f7fa", font=("Arial", 12)).pack(pady=10)
    user_entry = tk.Entry(root)
    user_entry.pack()

    tk.Label(root, text="Password:", bg="#e0f7fa", font=("Arial", 12)).pack(pady=10)
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    tk.Button(root, text="Login", command=check_login, bg="#00796b", fg="white", width=10).pack(pady=20)
    root.mainloop()

# ---------------- MAIN WINDOW ----------------
def main_window():
    win = tk.Tk()
    win.title("Library Management System")
    win.geometry("900x650")
    win.config(bg="#fafafa")

    tab_control = ttk.Notebook(win)

    # Tabs
    book_tab = ttk.Frame(tab_control)
    student_tab = ttk.Frame(tab_control)
    issue_tab = ttk.Frame(tab_control)
    tab_control.add(book_tab, text="Books")
    tab_control.add(student_tab, text="Students")
    tab_control.add(issue_tab, text="Issue/Return")
    tab_control.pack(expand=1, fill="both")

    # ---------------- BOOK TAB ----------------
    def add_book():
        title = title_entry.get()
        author = author_entry.get()
        copies = copies_entry.get()
        if not (title and author and copies):
            messagebox.showwarning("Input Error", "All fields required!")
            return
        
        try:
            copies = int(copies)
            if copies < 0:
                messagebox.showwarning("Input Error", "Copies cannot be negative!")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Copies must be a number!")
            return

        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO books (title, author, copies) VALUES (%s,%s,%s)", (title, author, copies))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Book Added Successfully")
            clear_book_entries()
            show_books()

    def delete_book():
        book_id = book_id_entry.get()
        if not book_id:
            messagebox.showwarning("Input Error", "Enter Book ID!")
            return
        
        try:
            book_id = int(book_id)
        except ValueError:
            messagebox.showwarning("Input Error", "Book ID must be a number!")
            return
            
        db = connect_db()
        if db:
            cursor = db.cursor()
            
            # Check if book exists
            cursor.execute("SELECT * FROM books WHERE book_id=%s", (book_id,))
            book = cursor.fetchone()
            
            if not book:
                messagebox.showerror("Error", "Book ID not found!")
                db.close()
                return
            
            # Check if book is currently issued (NOT returned)
            cursor.execute("SELECT * FROM issued_books WHERE book_id=%s AND return_date IS NULL", (book_id,))
            issued_books = cursor.fetchall()
            
            if issued_books:
                messagebox.showerror("Error", "Cannot delete book! It is currently issued to students.")
                db.close()
                return
            
            # Delete the book (this will also delete issued book records due to CASCADE)
            cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
            db.commit()
            db.close()
            messagebox.showinfo("Deleted", "Book Deleted Successfully")
            clear_book_entries()
            show_books()

    def clear_book_entries():
        book_id_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        copies_entry.delete(0, tk.END)

    def show_books():
        for row in book_table.get_children():
            book_table.delete(row)
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM books")
            for row in cursor.fetchall():
                book_table.insert('', 'end', values=row)
            db.close()

    # Book Tab Layout
    book_frame = tk.Frame(book_tab)
    book_frame.pack(padx=10, pady=10, fill=tk.X)

    tk.Label(book_frame, text="Book ID (for delete)").grid(row=0, column=0, sticky=tk.W, pady=5)
    book_id_entry = tk.Entry(book_frame, width=30)
    book_id_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(book_frame, text="Title *").grid(row=1, column=0, sticky=tk.W, pady=5)
    title_entry = tk.Entry(book_frame, width=30)
    title_entry.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(book_frame, text="Author *").grid(row=2, column=0, sticky=tk.W, pady=5)
    author_entry = tk.Entry(book_frame, width=30)
    author_entry.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(book_frame, text="Copies *").grid(row=3, column=0, sticky=tk.W, pady=5)
    copies_entry = tk.Entry(book_frame, width=30)
    copies_entry.grid(row=3, column=1, pady=5, padx=5)

    button_frame = tk.Frame(book_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="Add Book", command=add_book, bg="#4caf50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Delete Book", command=delete_book, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Show Books", command=show_books, bg="#2196f3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_book_entries, bg="#ff9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)

    # Books Table
    table_frame = tk.Frame(book_tab)
    table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    book_table = ttk.Treeview(table_frame, columns=("ID", "Title", "Author", "Copies"), show='headings')
    book_table.heading("ID", text="ID")
    book_table.heading("Title", text="Title")
    book_table.heading("Author", text="Author")
    book_table.heading("Copies", text="Copies")
    
    book_table.column("ID", width=50)
    book_table.column("Title", width=200)
    book_table.column("Author", width=150)
    book_table.column("Copies", width=80)
    
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=book_table.yview)
    book_table.configure(yscrollcommand=scrollbar.set)
    
    book_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    show_books()

    # ---------------- STUDENT TAB ----------------
    def add_student():
        name = name_entry.get()
        roll = roll_entry.get()
        if not (name and roll):
            messagebox.showwarning("Input Error", "All fields required!")
            return
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO students (name, roll_no) VALUES (%s,%s)", (name, roll))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Student Added Successfully")
            clear_student_entries()
            show_students()

    def clear_student_entries():
        name_entry.delete(0, tk.END)
        roll_entry.delete(0, tk.END)

    def show_students():
        for row in student_table.get_children():
            student_table.delete(row)
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM students")
            for row in cursor.fetchall():
                student_table.insert('', 'end', values=row)
            db.close()

    # Student Tab Layout
    student_frame = tk.Frame(student_tab)
    student_frame.pack(padx=10, pady=10, fill=tk.X)

    tk.Label(student_frame, text="Name *").grid(row=0, column=0, sticky=tk.W, pady=5)
    name_entry = tk.Entry(student_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(student_frame, text="Roll No *").grid(row=1, column=0, sticky=tk.W, pady=5)
    roll_entry = tk.Entry(student_frame, width=30)
    roll_entry.grid(row=1, column=1, pady=5, padx=5)

    student_button_frame = tk.Frame(student_frame)
    student_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(student_button_frame, text="Add Student", command=add_student, bg="#4caf50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(student_button_frame, text="Show Students", command=show_students, bg="#2196f3", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(student_button_frame, text="Clear", command=clear_student_entries, bg="#ff9800", fg="white", width=15).pack(side=tk.LEFT, padx=5)

    # Students Table
    student_table_frame = tk.Frame(student_tab)
    student_table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    student_table = ttk.Treeview(student_table_frame, columns=("ID", "Name", "Roll"), show='headings')
    student_table.heading("ID", text="ID")
    student_table.heading("Name", text="Name")
    student_table.heading("Roll", text="Roll No")
    
    student_table.column("ID", width=50)
    student_table.column("Name", width=200)
    student_table.column("Roll", width=150)
    
    student_scrollbar = ttk.Scrollbar(student_table_frame, orient=tk.VERTICAL, command=student_table.yview)
    student_table.configure(yscrollcommand=student_scrollbar.set)
    
    student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    student_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    show_students()

    # ---------------- ISSUE / RETURN TAB ----------------
    def issue_book():
        sid = student_id_entry.get()
        bid = issue_book_id_entry.get()
        if not (sid and bid):
            messagebox.showwarning("Input Error", "All fields required!")
            return
        
        try:
            sid = int(sid)
            bid = int(bid)
        except ValueError:
            messagebox.showwarning("Input Error", "Student ID and Book ID must be numbers!")
            return

        db = connect_db()
        if db:
            cursor = db.cursor()
            
            # Check if student exists
            cursor.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student ID not found!")
                db.close()
                return
            
            # Check if book exists and has available copies
            cursor.execute("SELECT * FROM books WHERE book_id=%s", (bid,))
            book = cursor.fetchone()
            if not book:
                messagebox.showerror("Error", "Book ID not found!")
                db.close()
                return
            
            if book[3] <= 0:  # copies
                messagebox.showerror("Error", "No copies available for this book!")
                db.close()
                return
            
            # Check if student already has this book issued and not returned
            cursor.execute("SELECT * FROM issued_books WHERE student_id=%s AND book_id=%s AND return_date IS NULL", (sid, bid))
            existing_issue = cursor.fetchone()
            if existing_issue:
                messagebox.showerror("Error", "This student already has this book issued!")
                db.close()
                return
            
            # Issue the book
            cursor.execute("INSERT INTO issued_books (student_id, book_id, issue_date) VALUES (%s,%s,%s)",
                           (sid, bid, date.today()))
            cursor.execute("UPDATE books SET copies=copies-1 WHERE book_id=%s", (bid,))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Book Issued Successfully")
            clear_issue_entries()
            show_issued_books()

    def return_book():
        iid = issue_id_entry.get()
        if not iid:
            messagebox.showwarning("Input Error", "Enter Issue ID!")
            return
        
        try:
            iid = int(iid)
        except ValueError:
            messagebox.showwarning("Input Error", "Issue ID must be a number!")
            return
            
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("SELECT book_id FROM issued_books WHERE issue_id=%s AND return_date IS NULL", (iid,))
            data = cursor.fetchone()
            if data:
                book_id = data[0]
                cursor.execute("UPDATE issued_books SET return_date=%s WHERE issue_id=%s", (date.today(), iid))
                cursor.execute("UPDATE books SET copies=copies+1 WHERE book_id=%s", (book_id,))
                db.commit()
                messagebox.showinfo("Returned", "Book Returned Successfully")
            else:
                messagebox.showerror("Error", "Invalid Issue ID or already returned")
            db.close()
            clear_issue_entries()
            show_issued_books()

    def clear_issue_entries():
        student_id_entry.delete(0, tk.END)
        issue_book_id_entry.delete(0, tk.END)
        issue_id_entry.delete(0, tk.END)

    def show_issued_books():
        for row in issue_table.get_children():
            issue_table.delete(row)
        db = connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT ib.issue_id, ib.student_id, s.name, ib.book_id, b.title, ib.issue_date, ib.return_date 
                FROM issued_books ib
                JOIN students s ON ib.student_id = s.student_id
                JOIN books b ON ib.book_id = b.book_id
                ORDER BY ib.issue_id
            """)
            for row in cursor.fetchall():
                issue_table.insert('', 'end', values=row)
            db.close()

    # Issue/Return Tab Layout
    issue_frame = tk.Frame(issue_tab)
    issue_frame.pack(padx=10, pady=10, fill=tk.X)

    # Issue Section
    issue_section = tk.LabelFrame(issue_frame, text="Issue Book", padx=10, pady=10)
    issue_section.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)

    tk.Label(issue_section, text="Student ID *").grid(row=0, column=0, sticky=tk.W, pady=5)
    student_id_entry = tk.Entry(issue_section, width=20)
    student_id_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(issue_section, text="Book ID *").grid(row=1, column=0, sticky=tk.W, pady=5)
    issue_book_id_entry = tk.Entry(issue_section, width=20)
    issue_book_id_entry.grid(row=1, column=1, pady=5, padx=5)

    tk.Button(issue_section, text="Issue Book", command=issue_book, bg="#4caf50", fg="white", width=15).grid(row=2, column=0, columnspan=2, pady=10)

    # Return Section
    return_section = tk.LabelFrame(issue_frame, text="Return Book", padx=10, pady=10)
    return_section.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)

    tk.Label(return_section, text="Issue ID *").grid(row=0, column=0, sticky=tk.W, pady=5)
    issue_id_entry = tk.Entry(return_section, width=20)
    issue_id_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Button(return_section, text="Return Book", command=return_book, bg="#f44336", fg="white", width=15).grid(row=1, column=0, columnspan=2, pady=10)

    # Buttons
    button_section = tk.Frame(issue_frame)
    button_section.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(button_section, text="Show Issued Books", command=show_issued_books, bg="#2196f3", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_section, text="Clear All", command=clear_issue_entries, bg="#ff9800", fg="white", width=15).pack(side=tk.LEFT, padx=5)

    # Issued Books Table
    issue_table_frame = tk.Frame(issue_tab)
    issue_table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    issue_table = ttk.Treeview(issue_table_frame, 
                              columns=("Issue ID", "Student ID", "Student Name", "Book ID", "Book Title", "Issue Date", "Return Date"), 
                              show='headings')
    
    for col in ("Issue ID", "Student ID", "Student Name", "Book ID", "Book Title", "Issue Date", "Return Date"):
        issue_table.heading(col, text=col)
    
    issue_table.column("Issue ID", width=70)
    issue_table.column("Student ID", width=80)
    issue_table.column("Student Name", width=120)
    issue_table.column("Book ID", width=70)
    issue_table.column("Book Title", width=150)
    issue_table.column("Issue Date", width=100)
    issue_table.column("Return Date", width=100)
    
    issue_scrollbar = ttk.Scrollbar(issue_table_frame, orient=tk.VERTICAL, command=issue_table.yview)
    issue_table.configure(yscrollcommand=issue_scrollbar.set)
    
    issue_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    issue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    show_issued_books()

    win.mainloop()

# ---------------- MAIN EXECUTION ----------------
if __name__ == "__main__":
    login_window()