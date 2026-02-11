import random
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class MyLibrary:
    number_members = 0
    member_information = {}

    def __init__(self):
        raise IndexError("Please use the Membership method to join!")
    
    @classmethod
    def Membership(cls, full_name, age):
        if age > 15:
            obj = object.__new__(cls)
            obj.id = random.randint(10_000, 99_999)
            obj.full_name = full_name
            obj.age = age
            obj.list_books = {}

            cls.number_members += 1
            cls.member_information[obj.id] = obj
            return obj
        elif age <= 15:
            raise ValueError("Please visit the children's library.")
        
    def get_book(self, book_name):
        if len(self.list_books) >= 3:
            return "You can't get more than 3 books."
        else:
            date = datetime.now().strftime("%Y/%A/%d")
            self.list_books[book_name] = date
            return f"Book: {book_name}, Time: {date}"
    
    def return_book(self, book_name):
        if book_name in self.list_books:
            del self.list_books[book_name]
            return f"Book: {book_name} returned."
        else:
            return f"You don't have --> {book_name}."
    
    def info(self):
        info_text = f"ID: {self.id}\nName: {self.full_name}\nAge: {self.age}\n"
        if len(self.list_books) == 0:
            info_text += "No book received"
        else:
            info_text += "Books:\n"
            for book, date in self.list_books.items():
                info_text += f"  - {book} ({date})\n"
        return info_text


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x500")
        self.current_member = None
        
        # Create main frame
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text=" Library Management", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        # Membership Section
        member_frame = tk.LabelFrame(main_frame, text="Create Membership", padx=10, pady=10)
        member_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(member_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(member_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(member_frame, text="Age:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.age_entry = tk.Entry(member_frame, width=30)
        self.age_entry.grid(row=1, column=1, pady=5)
        
        tk.Button(member_frame, text="Register", command=self.create_membership, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
        
        # Book Operations Section
        book_frame = tk.LabelFrame(main_frame, text="Book Operations", padx=10, pady=10)
        book_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(book_frame, text="Book Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.book_entry = tk.Entry(book_frame, width=30)
        self.book_entry.grid(row=0, column=1, pady=5)
        
        btn_frame = tk.Frame(book_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Get Book", command=self.get_book, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Return Book", command=self.return_book, bg="#FF9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Info Section
        info_frame = tk.LabelFrame(main_frame, text="Member Information", padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.info_text = tk.Text(info_frame, height=8, width=50)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(main_frame, text="Show Info", command=self.show_info, bg="#9C27B0", fg="white", width=20).pack(pady=5)
        
    def create_membership(self):
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()
        
        if not name or not age_str:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return
        
        try:
            age = int(age_str)
            self.current_member = MyLibrary.Membership(name, age)
            messagebox.showinfo("Success", f"Membership created!\nID: {self.current_member.id}")
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.show_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def get_book(self):
        if not self.current_member:
            messagebox.showwarning("Warning", "Please create a membership first!")
            return
        
        book_name = self.book_entry.get().strip()
        if not book_name:
            messagebox.showwarning("Warning", "Please enter book name!")
            return
        
        result = self.current_member.get_book(book_name)
        messagebox.showinfo("Info", result)
        self.book_entry.delete(0, tk.END)
        self.show_info()
    
    def return_book(self):
        if not self.current_member:
            messagebox.showwarning("Warning", "Please create a membership first!")
            return
        
        book_name = self.book_entry.get().strip()
        if not book_name:
            messagebox.showwarning("Warning", "Please enter book name!")
            return
        
        result = self.current_member.return_book(book_name)
        messagebox.showinfo("Info", result)
        self.book_entry.delete(0, tk.END)
        self.show_info()
    
    def show_info(self):
        self.info_text.delete(1.0, tk.END)
        if self.current_member:
            info = self.current_member.info()
            self.info_text.insert(1.0, info)
        else:
            self.info_text.insert(1.0, "No active membership")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()