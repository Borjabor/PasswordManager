from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

"""
This program is a simple password manager that allows the user to generate and save passwords for various websites. It provides functionality to generate a random password with a mix of letters, numbers, and symbols, and to save the generated password along with the associated website and email address. The program also allows the user to find and display the saved password for a specific website.

The program uses the Tkinter library for creating the graphical user interface (GUI). It includes functions for generating a password, saving the password, finding the password for a specific website, and toggling the visibility of the password in the GUI.

The program requires the following libraries: tkinter, messagebox, random, pyperclip, and json.

To run the program, execute the main.py file. The program will display a GUI with input fields for the website, email, and password. The user can generate a password by clicking the "Generate Password" button, save the generated password by clicking the "Save Password" button, and find the saved password for a specific website by clicking the "Find Password" button.

The program stores the saved passwords in a JSON file named "data.json". The passwords are organized in a dictionary format, with the website as the key and the email and password as the values.

Note: This program was for practice purposes only and should not be used to store sensitive information.
"""

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    n_letters = random.randint(8, 10)
    n_number = random.randint(2, 4)
    n_symbols = random.randint(2, 4)
    
    character_types = {
        "letters": [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)],
        "numbers": [str(i) for i in range(10)],
        "symbols": ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
                    '[', ']', '{', '}', '\\', '|', ';', ':', '\'', '"', ',', '<', '.', '>', '/', '?']
    }
    
    password_letters = [random.choice(character_types["letters"]) for _ in range(n_letters)]
    password_numbers = [random.choice(character_types["numbers"]) for _ in range(n_number)]
    password_symbols = [random.choice(character_types["symbols"]) for _ in range(n_symbols)]
    
    password_list = password_letters + password_numbers + password_symbols
        
    random.shuffle(password_list)
    
    password_entry.delete(0, END)
    password_entry.insert(0, "".join(password_list))
    pyperclip.copy("".join(password_list))


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email, 
            "password": password
            }
        }
    
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
                messagebox.showinfo(title="Success", message="New file created. Your credentials have been saved!")
        else:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
                messagebox.showinfo(title="Success", message="Your credentials have been saved!")
        finally:   
            for entry in entries:
                entry.delete(0, END)
    
    
# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}\n\n Password copied to clipboard.")
            pyperclip.copy(password)
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")
      
            
# ---------------------------- PASSWORD VISIBILITY TOGGLE ------------------------------- #

def toggle_password_visibility():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=32)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=1, sticky="w")

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

start_char = "|"
end_char = "|"
standard_email = "" 

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=32)
password_entry.config(show="*")
password_entry.grid(row=3, column=1, sticky="w")

show_password = IntVar()
show_password_check = Checkbutton(text="Show", variable=show_password, command=toggle_password_visibility)
show_password_check.grid(row=3, column=1, sticky="e")


entries = [website_entry, email_entry, password_entry]

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()