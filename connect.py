import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import mysql.connector


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
             # Bind the onchange event to a function
            self.backup_options.bind("<<ComboboxSelected>>", self.on_backup_option_selected)

        self.label_folder = ttk.Label(self, text="Folder:")
        self.label_folder.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.choose_folder_button = ttk.Button(self, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.selected_folder_label = ttk.Label(self, text="")
        self.selected_folder_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        heading_label = ttk.Label(self, text=f"Select Compatability Options", font=("Helvetica", 10, "bold"))
        heading_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")

        self.ocimds_var = tk.BooleanVar()
        self.ocimds_checkbox = ttk.Checkbutton(self, text="ocimds", variable=self.ocimds_var, command=self.update_checkbox_state)
        self.ocimds_checkbox.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.skip_invalid_acc_var = tk.BooleanVar()
        self.skip_invalid_acc_checkbox = ttk.Checkbutton(self, text="skip Invalid accounts", variable=self.skip_invalid_acc_var, command=self.update_checkbox_state)
        self.skip_invalid_acc_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.strip_restricted_grants_var = tk.BooleanVar(value=False)
        self.strip_restricted_grants_checkbox = ttk.Checkbutton(self, text="strip_restricted_grants", variable=self.strip_restricted_grants_var, command=self.update_checkbox_state)
        self.strip_restricted_grants_checkbox.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.strip_definers_var = tk.BooleanVar(value=False)
        self.strip_definers_checkbox = ttk.Checkbutton(self, text="strip_restricted_grants", variable=self.strip_definers_var, command=self.update_checkbox_state)
        self.strip_definers_checkbox.grid(row=7, column=1, padx=10, pady=5, sticky="w")


        self.force_innodb_var = tk.BooleanVar(value=False)
        self.force_innodb_checkbox = ttk.Checkbutton(self, text="force_innodb", variable=self.force_innodb_var, command=self.update_checkbox_state)
        self.force_innodb_checkbox.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        

        self.strip_tablespaces_var = tk.BooleanVar(value=False)
        self.strip_tablespaces_checkbox = ttk.Checkbutton(self, text="strip_tablespaces", variable=self.strip_tablespaces_var, command=self.update_checkbox_state)
        self.strip_tablespaces_checkbox.grid(row=8, column=1, padx=10, pady=5, sticky="w")


        self.create_invisible_pk_var = tk.BooleanVar(value=False)
        self.create_invisible_pk_checkbox = ttk.Checkbutton(self, text="create_invisible_pk", variable=self.create_invisible_pk_var, command=self.update_checkbox_state)
        self.create_invisible_pk_checkbox.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        # Bind a function to handle visibility of ignore_missing_pks_checkbox
        self.create_invisible_pk_var.trace_add('write', self.toggle_ignore_missing_pks_checkbox)
        
        self.ignore_missing_pks_var = tk.BooleanVar(value=False)
        self.ignore_missing_pks_checkbox = ttk.Checkbutton(self, text="ignore_missing_pks", variable=self.ignore_missing_pks_var, command=self.update_checkbox_state)
        self.ignore_missing_pks_checkbox.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=10, column=0, columnspan=2, pady=10, sticky="w")

        # Move output_textbox to the next row
        self.output_textbox = tk.Text(self,  width=50,wrap="none")
        self.output_textbox.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
    def toggle_ignore_missing_pks_checkbox(self, *args):
         if self.create_invisible_pk_var.get():
           self.ignore_missing_pks_checkbox.grid_remove()
         else:
           self.ignore_missing_pks_checkbox.grid(row=9, column=1, padx=10, pady=5, sticky="w")    
       
    def on_backup_option_selected(self, event):
        selected_option = self.backup_options.get()
        if selected_option == "Schema Backup":
            # If Schema Backup is selected, display a message
            messagebox.showinfo("Schema Backup", "Please note that Schema Backup will not perform the backup operation but display the list of schemas.")
            self.get_mysql_schemas()
            schemas = self.get_mysql_schemas()
           # Create a dropdown menu for schemas
            self.label_schemas = ttk.Label(self, text="Schemas:")
            self.label_schemas.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.schema_var = tk.StringVar()
           # self.schema_dropdown = ttk.OptionMenu(self, self.schema_var, "Select Schema", *schemas)
            self.schema_dropdown = ttk.Combobox(self, values=[*schemas])
            self.schema_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

###############################################



##################################################
           
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
        self.skip_invalid_acc_var.set(self.skip_invalid_acc_checkbox.instate(['selected']))
        self.strip_definers_var.set(self.strip_definers_checkbox.instate(['selected']))
        #self.strip_tablespaces_var.set(self.strip_tablespaces_checkbox.instate(['selected']))
        #self.ignore_missing_pks_var.set(self.ignore_missing_pks_checkbox.instate(['selected']))
    def get_mysql_schemas(self):
      try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            port=self.port
        )
        if connection.is_connected():
            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the SQL query to retrieve the list of schemas
            cursor.execute("SHOW DATABASES")

            # Fetch all the rows from the cursor
            rows = cursor.fetchall()

            # Extract schema names from the rows
            schemas = [row[0] for row in rows]

            # Close the cursor and connection
            cursor.close()
            connection.close()
            return schemas
            # Display the list of schemas
            schema_list = "\n".join(schemas)
            messagebox.showinfo("List of Schemas", f"The following schemas are available:\n\n{schema_list}")

      except mysql.connector.Error as error:
        # Display error message if connection or query fails
        messagebox.showerror("Error", f"An error occurred while fetching schemas: {error}")
        return []

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
            
        if self.skip_invalid_acc_var.get():
            compatibility_options.append("skip_invalid_accounts")
            
        if self.strip_definers_var.get():
            compatibility_options.append("strip_definers")
            
        if self.strip_tablespaces_var.get():
            compatibility_options.append("strip_tablespaces")
            
        if self.strip_tablespaces_var.get():
            compatibility_options.append("ignore_missing_pks")
            
        compatibility_options_str = ', '.join([f"'{option}'" for option in compatibility_options])
        
        if self.backup_options.get() == "Schema Backup" and self.schema_dropdown.get():
          print("you are in if")  
        # Construct the command for util.dumpSchemas
          command_backup = f"mysqlsh --uri mysqlx://{self.username}:{self.password}@{self.hostname} -e \"util.dumpSchemas(['{self.schema_dropdown.get()}'],'{self.selected_folder}')\""
          #util.dumpSchemas(["sbtest"],"/home/backup/sbtest/",{threads :2})
        else:
        # Construct the command for util.dumpInstance
          print("u i in else")
          command_backup = f"mysqlsh --uri mysqlx://{self.username}:{self.password}@{self.hostname} -e \"util.dumpInstance('{self.selected_folder}', {{ocimds: {ocimds}, compatibility: [{compatibility_options_str}]}})\""
        # Construct the MySQL dump command with selected options
        
        print(command_backup)
        self.run_mysqlsh_backup(command_backup)
        # Run MySQL Shell backup command and capture output
       

    def run_mysqlsh_backup(self, command_backup):
        # Clear previous output
        self.output_textbox.delete(1.0, tk.END)

        try:
            # Run mysqlsh command and capture output
            result = subprocess.run(command_backup, capture_output=True, text=True, shell=True)

            # Update the output textbox with the result
            if result.returncode == 0:
                print(result.stdout)
                self.output_textbox.insert(tk.END, result.stdout)
                messagebox.showinfo("Success", "Backup completed successfully.")
            else:
                self.output_textbox.insert(tk.END, result.stderr)
                messagebox.showerror("Error", "Backup failed.")
        except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

class RestoreOptionsForm(tk.Frame):
    def __init__(self, parent, hostname, username, port, password, restore_type):
        super().__init__(parent)
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password
        self.restore_type = restore_type
        self.selected_folder = None  # Initialize selected_folder attribute

        # Create a heading label for the restore type
        heading_label = ttk.Label(self, text=f"{restore_type} Restore Options", font=("Helvetica", 14, "bold"))
        heading_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.label_folder = ttk.Label(self, text="Folder:")
        self.label_folder.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.choose_folder_button = ttk.Button(self, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.selected_folder_label = ttk.Label(self, text="")
        self.selected_folder_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.label_username = ttk.Label(self, text="Username:")
        self.label_username.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_username = ttk.Entry(self)
        self.entry_username.grid(row=3, column=1, padx=10, pady=5)

        self.label_password = ttk.Label(self, text="Password:")
        self.label_password.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.grid(row=4, column=1, padx=10, pady=5)

        self.label_hostname = ttk.Label(self, text="Hostname:")
        self.label_hostname.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.entry_hostname = ttk.Entry(self)
        self.entry_hostname.grid(row=5, column=1, padx=10, pady=5)

        self.label_port = ttk.Label(self, text="Port:")
        self.label_port.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.entry_port = ttk.Entry(self)
        self.entry_port.grid(row=6, column=1, padx=10, pady=5)

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="w")

        self.submit_button = ttk.Button(self, text="TestConnection", command=self.testconnection)
        self.submit_button.grid(row=7, column=1, columnspan=2, pady=10, sticky="w")
       
        # Move output_textbox to the next row
        self.output_textbox = tk.Text(self, width=50, wrap="none")
        self.output_textbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def choose_folder(self):
        self.selected_folder = filedialog.askdirectory()
        self.selected_folder_label.config(text=f"Selected Folder: {self.selected_folder}")
        #if self.selected_folder:
            #files_in_folder = os.listdir(self.selected_folder)
           # if files_in_folder:
               # messagebox.showwarning("Folder Contains Files", "The selected folder contains files. It is recommended to choose an empty folder for restore.")
    def testconnection(self):
        username_restore = self.entry_username.get()
        password_restore = self.entry_password.get()
        hostname_restore = self.entry_hostname.get()
        port_restore = self.entry_port.get()
       
       
        # Call connect_to_mysql to check connection
        result_message = connect_to_mysql(hostname_restore,username_restore,password_restore,port_restore)
       
        if result_message == True:
            messagebox.showinfo("Success","Successfully connected to " + hostname_restore)
           
        else:
            error_msg = f"Failed to connect to MySQL: {result_message}"
            messagebox.showerror("Error", error_msg)
       
    def submit_form(self):
        username_restore = self.entry_username.get()
        password_restore = self.entry_password.get()
        hostname_restore = self.entry_hostname.get()
        port_restore = self.entry_port.get()
        folder_restore = self.selected_folder
        print(username_restore)
        print(password_restore)
        print(hostname_restore)
        print(port_restore)
        print(folder_restore)
        password_restore_encoded = password_restore.replace("@", "%40")
# Validate form fields
        if not username_restore or not password_restore or not hostname_restore or not port_restore or not folder_restore:
             messagebox.showerror("Error", "Please fill in all the fields.")
             return
        command_restore = f"mysqlsh --uri mysqlx://{username_restore}:{password_restore_encoded}@{hostname_restore}:{port_restore} -e \"util.loadDump('{folder_restore}', {{progressFile: 'C:/Users/tantr/AppData/Local/Temp/log_restore.json', threads: 12, ignoreVersion: true}})\""
        print(command_restore)
        # Proceed with restore process
        run_mysqlsh_restore(self,command_restore)
       
def run_mysqlsh_restore(self,command_restore):
        # Clear previous output
        self.output_textbox.delete(1.0, tk.END)
        try:
            # Run mysqlsh command and capture output
            result = subprocess.run(command_restore, capture_output=True, text=True, shell=True)

            # Update the output textbox with the result
            if result.returncode == 0:
                print(result.stdout)
                self.output_textbox.insert(tk.END, result.stdout)
                messagebox.showinfo("Success", "Restore process completed successfully.")
            else:
                self.output_textbox.insert(tk.END, result.stderr)
                messagebox.showerror("Error", "Restore failed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

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
        self.backup_menu = tk.Menu(self.menu, tearoff=0)
        self.restore_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Backup Options", menu=self.backup_menu)
        self.menu.add_cascade(label="Restore Options", menu=self.restore_menu)

        # Add Local Backup option under Backup Options
        self.backup_menu.add_command(label="Local Backup", command=lambda: self.show_backup_options("Local"))
       
        # Add Cloud Backup option under Backup Options
        self.backup_menu.add_command(label="Cloud Backup", command=lambda: self.show_backup_options("Cloud"))

        # Add Local Restore option under Restore Options
        self.restore_menu.add_command(label="Local Restore", command=lambda: self.show_restore_options("Local"))

        # Add Cloud Restore option under Restore Options
        self.restore_menu.add_command(label="Cloud Restore", command=lambda: self.show_restore_options("Cloud"))

        # Initialize backup options frame
        self.backup_options_frame = None

    def show_backup_options(self, backup_type):
        # Clear existing frame if exists
        if self.backup_options_frame:
            self.backup_options_frame.destroy()

        # Create and pack new backup options frame
        self.backup_options_frame = BackupOptionsForm(self, self.hostname, self.username, self.port, self.password, backup_type)
        self.backup_options_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def show_restore_options(self, restore_type):
        # Clear existing frame if exists
        if self.backup_options_frame:
            self.backup_options_frame.destroy()

        # Create and pack new restore options frame
        self.backup_options_frame = RestoreOptionsForm(self, self.hostname, self.username, self.port, self.password, restore_type)
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

       # default_hostname = "10.187.127.133"
       # default_port = "3306"
       # default_username = "dbe_admin"
       # default_password = "Dbe$admin$525"

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

        self.submit_button = ttk.Button(self, text="Login", command=self.submit_form)
        self.submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_form(self):
        hostname = self.entry_hostname.get()
        port = self.entry_port.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Call connect_to_mysql to check connection
        result_message = connect_to_mysql(hostname, username, password, port)
        if result_message == True:
            messagebox.showinfo("Success","Successfully connected to " + hostname)
            welcome_form = WelcomeForm(hostname, username, port, password)
            self.withdraw()
        else:
            error_msg = f"Failed to connect to MySQL: {result_message}"
            messagebox.showerror("Error", error_msg)

def connect_to_mysql(host, user, password, port):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        if connection.is_connected():
            # Close the connection
            connection.close()
            # Return success message
            return True
    except mysql.connector.Error as error:
        # Return error message
        return f"Error while connecting to MySQL: {error}"

if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()
