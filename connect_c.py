import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class WelcomeForm(tk.Tk):
    def __init__(self, hostname, username, port, password):
        super().__init__()
        self.title("Welcome")
        self.geometry("300x200")
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password

        # Add labels to the new window
        label = tk.Label(self, text=f"You are connected to {self.hostname} as {self.username}")
        label.pack()

        # Create a menu
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # Create an "Action" menu
        self.action_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Action", menu=self.action_menu)
        self.action_menu.add_command(label="Local Backup", command=lambda: self.perform_local_backup(hostname, username, port, password))
        self.action_menu.add_command(label="Cloud Backup", command=self.perform_cloud_backup)

    def perform_local_backup(self, hostname, username, port, password):
        print("Local backup initiated.")
        print("Hostname:", hostname)
        print("Username:", username)
        print("Port:", port)
        print("Password:", password)
       

    def perform_cloud_backup(self):
        print("Cloud backup initiated.")
        # Implement cloud backup logic here

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        # Set default values
        default_hostname = "localhost"
        default_port = "3306"
        default_username = "srini"
        default_password = "Sai1prasad"

        # Create labels and entry fields
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

        # Create a show password button
        self.show_password_button = ttk.Button(self, text="Show Password", command=self.toggle_password_visibility)
        self.show_password_button.grid(row=3, column=2)

        # Create a submit button
        self.submit_button = ttk.Button(self, text="Login", command=self.submit_form)
        self.submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_form(self):
        # Get the values from the entry fields
        hostname = self.entry_hostname.get()
        port = self.entry_port.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Construct MySQL Shell command
        command = f"mysqlsh --uri {hostname} --user {username} -p{password} -f c:/dump/query.sql"

        try:
            # Execute the MySQL Shell command
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            # Check if the command was successful
            if result.returncode == 0:
                success = "Successfully connected to the database"
                print("MySQL Shell Output:")
                print(result.stdout)
                messagebox.showinfo("Success", success)

                # Open the welcome form after successful login
                welcome_form = WelcomeForm(hostname, username, port, password)
                self.destroy()  # Close the login window
                welcome_form.mainloop()
            else:
                error_msg = f"Failed to run query: {result.stderr}"
                print("Error running MySQL Shell command:")
                print(result.stderr)
                messagebox.showerror("Error", error_msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
