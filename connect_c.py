import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys,os
from typing import Self 
sys.path.append("C:/Users/tantr/source/repos")
from bkp import MyForm

class BackupOptionsForm(tk.Frame):
    def __init__(self, parent, hostname, username, port, password, backup_type):
        super().__init__(parent)
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password
        self.backup_type = backup_type
        self.selected_folder = None  # Initialize selected_folder attribute
        
        # Create a heading label for the backup type
        heading_label = ttk.Label(self, text=f"{backup_type} Backup Options", font=("Helvetica", 14, "bold"))
        heading_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        if backup_type == "Local":
            self.label_backup_option = ttk.Label(self, text="Backup Option:")
            self.label_backup_option.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.backup_options = ttk.Combobox(self, values=["Instance Backup", "Schema Backup", "Table Backup"])
            self.backup_options.grid(row=1, column=1, padx=10, pady=5, sticky="w")
            self.backup_options.current(0)  # Set default option to Instance Backup

        self.label_folder = ttk.Label(self, text="Folder:")
        self.label_folder.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.choose_folder_button = ttk.Button(self, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.selected_folder_label = ttk.Label(self, text="")
        self.selected_folder_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.ocimds_var = tk.BooleanVar()
        self.ocimds_checkbox = ttk.Checkbutton(self, text="ocimds", variable=self.ocimds_var, command=self.update_checkbox_state)
        self.ocimds_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.strip_restricted_grants_var = tk.BooleanVar(value=False)
        self.strip_restricted_grants_checkbox = ttk.Checkbutton(self, text="strip_restricted_grants", variable=self.strip_restricted_grants_var, command=self.update_checkbox_state)
        self.strip_restricted_grants_checkbox.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.force_innodb_var = tk.BooleanVar(value=False)
        self.force_innodb_checkbox = ttk.Checkbutton(self, text="force_innodb", variable=self.force_innodb_var, command=self.update_checkbox_state)
        self.force_innodb_checkbox.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.create_invisible_pk_var = tk.BooleanVar(value=False)
        self.create_invisible_pk_checkbox = ttk.Checkbutton(self, text="create_invisible_pk", variable=self.create_invisible_pk_var, command=self.update_checkbox_state)
        self.create_invisible_pk_checkbox.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=8, column=0, columnspan=2, pady=10, sticky="w")

    def choose_folder(self):
        self.selected_folder = filedialog.askdirectory()
        self.selected_folder_label.config(text=f"Selected Folder: {self.selected_folder}")
        if self.selected_folder:
            files_in_folder = os.listdir(self.selected_folder)
            if files_in_folder:
                messagebox.showwarning("Folder Contains Files", "The selected folder contains files. It is recommended to choose an empty folder for backup.")
                
    def update_checkbox_state(self):
        # Update the state of the checkbox variables based on the checkbox values
        self.ocimds_var.set(self.ocimds_checkbox.instate(['selected']))
        self.strip_restricted_grants_var.set(self.strip_restricted_grants_checkbox.instate(['selected']))
        self.force_innodb_var.set(self.force_innodb_checkbox.instate(['selected']))
        self.create_invisible_pk_var.set(self.create_invisible_pk_checkbox.instate(['selected']))

    def submit_form(self):
        compatibility_options = []
        ocimds="false"
        if self.ocimds_var.get():
            ocimds="true"

        # Initialize compatibility options with "force_innodb" by default
        if self.force_innodb_var.get():
            compatibility_options.append("force_innodb")

        # Check if other options are selected and add them to compatibility options
        if self.strip_restricted_grants_var.get():
            compatibility_options.append("strip_restricted_grants")

        if self.create_invisible_pk_var.get():
            compatibility_options.append("create_invisible_pks")

        # Construct the MySQL dump command with selected options
        compatibility_options_str = ', '.join([f"'{option}'" for option in compatibility_options])
        command_backup = f"mysqlsh --uri mysqlx://{self.username}:{self.password}@{self.hostname} -e \"util.dumpInstance('{self.selected_folder}', {{ocimds: {ocimds}, compatibility: [{compatibility_options_str}]}})\""
        
        # Print the command for debugging
        print(f"Backup Type: {self.backup_type}")
        if self.backup_type == "Local":
            print("Backup Option:", self.backup_options.get())
        print("Selected Folder:", self.selected_folder)
        print("ocimds:", self.ocimds_var.get())
        print("strip_restricted_grants:", self.strip_restricted_grants_var.get())
        print("force_innodb:", self.force_innodb_var.get())
        print("create_invisible_pk:", self.create_invisible_pk_var.get())
        print("Hostname:", self.hostname)
        print("Username:", self.username)
        print("Port:", self.port)
        print("Password:", self.password)
        print(command_backup)
        run_mysqlsh_backup(command_backup)
class WelcomeForm(tk.Tk):
    def __init__(self, hostname, username, port, password):
        super().__init__()
        self.title("Welcome")
        self.geometry("400x400")
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.action_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Action", menu=self.action_menu)
        self.action_menu.add_command(label="Local Backup", command=lambda: self.show_backup_options("Local"))
        self.action_menu.add_command(label="Cloud Backup", command=lambda: self.show_backup_options("Cloud"))

    def show_backup_options(self, backup_type):
        self.backup_options_frame = BackupOptionsForm(self, self.hostname, self.username, self.port, self.password, backup_type)
        self.backup_options_frame.pack(pady=10, padx=10, fill="both", expand=True)

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        default_hostname = "localhost"
        default_port = "3306"
        default_username = "srini"
        default_password = "Sai1prasad"

        self.label_hostname = ttk.Label(self, text="Hostname:")
        self.label_hostname.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_hostname = ttk.Entry(self)
        self.entry_hostname.grid(row=0, column=1, padx=10, pady=5)
        self.entry_hostname.insert(0, default_hostname)

        self.label_port = ttk.Label(self, text="Port:")
        self.label_port.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_port = ttk.Entry(self)
        self.entry_port.grid(row=1, column=1, padx=10, pady=5)
        self.entry_port.insert(0, default_port)

        self.label_username = ttk.Label(self, text="Username:")
        self.label_username.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=2, column=1, padx=10, pady=5)
        self.entry_username.insert(0, default_username)

        self.label_password = ttk.Label(self, text="Password:")
        self.label_password.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.grid(row=3, column=1, padx=10, pady=5)
        self.entry_password.insert(0, default_password)

        #self.show_password_button = ttk.Button(self, text="Show Password", command=self.toggle_password_visibility)
        self.show_password_button = ttk.Button(self, text="Show Password")
        self.show_password_button.grid(row=3, column=2)

        self.submit_button = ttk.Button(self, text="Login", command=self.submit_form)
        self.submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_form(self):
        hostname = self.entry_hostname.get()
        port = self.entry_port.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        command = f"mysqlsh --uri {hostname} --user {username} -p{password} -f c:/dump/query.sql"
        print(command)  # Debugging
        try:
         # Execute the MySQL Shell command
            run_mysqlsh(self,command, hostname,username,password,port)
        except Exception as e:
         messagebox.showerror("Error", str(e))    
         
def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "":
            self.entry_password.config(show="*")
            self.show_password_button.config(text="Show Password")
        else:
            self.entry_password.config(show="")
            self.show_password_button.config(text="Hide Password")



                

def run_mysqlsh(self,command, hostname,username,password,port):
    # Run mysqlsh command and capture output
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Check if the command was successful
    if result.returncode == 0:
        success = "Successfully connected to the database"
        #global hostname,username,password,port
        print("MySQL Shell Output:")
        print(result.stdout)
        messagebox.showinfo("Success", success)

        # Open another window or form after successful login
        #open_another_form()

        #self.destroy()
        welcome_form = WelcomeForm(hostname, username, port, password)
        self.withdraw()

        #my_instance = MyForm()
    else:
        error_msg = f"Failed to run query: {result.stderr}"
        print("Error running MySQL Shell command:")
        print(result.stderr)
        messagebox.showerror("Error", error_msg)
        
def run_mysqlsh_backup(command_backup):
    # Run mysqlsh command and capture output
    result = subprocess.run(command_backup, capture_output=True, text=True, shell=True)

    # Check if the command was successful
    if result.returncode == 0:
        success = "starting backup"
        #global hostname,username,password,port
        print("MySQL Shell Output:")
        print(result.stdout)
        messagebox.showinfo("Success", result.stdout)

        # Open another window or form after successful login
        #open_another_form()

        #self.destroy()
        
        #my_instance = MyForm()
    else:
        error_msg = f"Failed to run query: {result.stderr}"
        print("Error running MySQL Shell command:")
        print(result.stderr)
        messagebox.showerror("Error", error_msg)


    def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "":
            self.entry_password.config(show="*")
            self.show_password_button.config(text="Show Password")
        else:
            self.entry_password.config(show="")
            self.show_password_button.config(text="Hide Password")

if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()
