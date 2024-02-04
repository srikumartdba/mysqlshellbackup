import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys 
sys.path.append("C:/Users/tantr/source/repos")
from bkp import MyForm
hostname=""
port=""
username=""
password=""
# Define the function to submit the form
def submit_form():
    # Get the values from the entry fields
    hostname = entry_hostname.get()
    port = entry_port.get()
    username = entry_username.get()
    password = entry_password.get()

    # Construct MySQL Shell command
    command = f"mysqlsh --uri {hostname} --user {username} -p{password} -f c:/dump/query.sql"

    print(command)  # Debugging

    try:
        # Execute the MySQL Shell command
        run_mysqlsh(command)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Define the function to run MySQL Shell command
def run_mysqlsh(command):
    # Run mysqlsh command and capture output
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Check if the command was successful
    if result.returncode == 0:
        success = "Successfully connected to the database"
        hostname = entry_hostname.get()
        username = entry_username.get()
        port =entry_port.get()
        password =entry_password.get()
        print("MySQL Shell Output:")
        print(result.stdout)
        messagebox.showinfo("Success", success)

        # Open another window or form after successful login
        #open_another_form()

        root.destroy()
        my_instance = MyForm()
    else:
        error_msg = f"Failed to run query: {result.stderr}"
        print("Error running MySQL Shell command:")
        print(result.stderr)
        messagebox.showerror("Error", error_msg)

# Define the function to open another form after successful login
def open_another_form():
    # Close the login window
    global hostname,username,password,port
    root.destroy()
    
    # Open another window or form
    another_root = tk.Tk()
    another_root.title("Welcome")
    print(hostname)
    print(username)
    # Add labels to the new window
    label = tk.Label(another_root, text="You are conneced to {hostname} as {username}")
    label.pack()
    
    # Add buttons for local backup and cloud backup
    
     #my_form = MyForm()
     #my_form.mainloop()
    # Run the event loop for the new window
    my_instance = MyForm()
    another_root.mainloop()

# Function to perform local backup
def perform_local_backup():
     my_instance = MyForm()

# Function to perform cloud backup
def perform_cloud_backup():
    print("Cloud backup initiated.")

# Define the function to toggle password visibility
def toggle_password_visibility():
    if entry_password.cget("show") == "":
        entry_password.config(show="*")
        show_password_button.config(text="Show Password")
    else:
        entry_password.config(show="")
        show_password_button.config(text="Hide Password")

# Create the main login window
root = tk.Tk()
root.title("Login")

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)

# Create a "File" menu item
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Create labels and entry fields
label_hostname = tk.Label(root, text="Hostname:")
label_hostname.grid(row=0, column=0, sticky="e")
entry_hostname = tk.Entry(root)
entry_hostname.grid(row=0, column=1)

label_port = tk.Label(root, text="Port:")
label_port.grid(row=1, column=0, sticky="e")
entry_port = tk.Entry(root)
entry_port.grid(row=1, column=1)

label_username = tk.Label(root, text="Username:")
label_username.grid(row=2, column=0, sticky="e")
entry_username = tk.Entry(root)
entry_username.grid(row=2, column=1)

label_password = tk.Label(root, text="Password:")
label_password.grid(row=3, column=0, sticky="e")
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=3, column=1)

# Create a show password button
show_password_button = ttk.Button(root, text="Show Password", command=toggle_password_visibility)
show_password_button.grid(row=3, column=2)

# Create a submit button
submit_button = tk.Button(root, text="Login", command=submit_form)
submit_button.grid(row=4, columnspan=2)

# Start the Tkinter event loop for the login window

root.mainloop()



