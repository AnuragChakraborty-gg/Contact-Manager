import tkinter as tk
from tkinter import messagebox
import cx_Oracle

# Oracle Database connection setup
try:
    connection = cx_Oracle.connect('ANURAG995/anurag@localhost:1521/xe')
    cursor = connection.cursor()
except cx_Oracle.DatabaseError as e:
    messagebox.showerror("Connection Error", f"There is a problem with the connection: {e}")
    exit(1)

# Function to create the contacts table if it doesn't exist
def create_table():
    try:
        cursor.execute("""
            CREATE TABLE contacts(
                id NUMBER(4) PRIMARY KEY,
                name VARCHAR2(100),
                email VARCHAR2(100)
            )
        """)
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        if 'ORA-00955' in str(e):  # Table already exists
            pass
        else:
            messagebox.showerror("Database Error", f"There is a problem with the SQL statement: {e}")

# Create the table
create_table()

# Functions to interact with the database
def add_contact(contact_id, name, email):
    try:
        cursor.execute("INSERT INTO contacts (id, name, email) VALUES (:1, :2, :3)", (contact_id, name, email))
        connection.commit()
        messagebox.showinfo("Success", "Contact added successfully")
    except cx_Oracle.DatabaseError as e:
        connection.rollback()
        messagebox.showerror("Database Error", str(e))

def get_contacts():
    cursor.execute("SELECT id, name, email FROM contacts")
    return cursor.fetchall()

def delete_contact(contact_id):
    try:
        cursor.execute("DELETE FROM contacts WHERE id = :1", (contact_id,))
        connection.commit()
        messagebox.showinfo("Success", "Contact deleted successfully")
    except cx_Oracle.DatabaseError as e:
        connection.rollback()
        messagebox.showerror("Database Error", str(e))

# GUI Setup
class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.id_label = tk.Label(root, text="ID")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)

        self.name_label = tk.Label(root, text="Name")
        self.name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1)

        self.email_label = tk.Label(root, text="Email")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=4, column=0, columnspan=2)

        self.contacts_listbox = tk.Listbox(root)
        self.contacts_listbox.grid(row=5, column=0, columnspan=2)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=6, column=0, columnspan=2)

    def add_contact(self):
        contact_id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        if contact_id and name and email:
            try:
                contact_id = int(contact_id)
                add_contact(contact_id, name, email)
                self.id_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.view_contacts()
            except ValueError:
                messagebox.showwarning("Input Error", "ID must be a number")
        else:
            messagebox.showwarning("Input Error", "Please enter ID, name, and email")

    def view_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in get_contacts():
            self.contacts_listbox.insert(tk.END, f"{contact[0]}: {contact[1]} - {contact[2]}")

    def delete_contact(self):
        selected = self.contacts_listbox.curselection()
        if selected:
            contact_id = self.contacts_listbox.get(selected).split(":")[0]
            delete_contact(contact_id)
            self.view_contacts()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()

# Close database connection on exit
cursor.close()
connection.close()
