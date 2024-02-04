
from asyncio.windows_events import NULL
import tkinter as tk
import subprocess
import os
success=""
class ConnectForm(tk.Frame):

   def submit_form():
    # Get the values from the entry fields

    label_message = tk.Label(root, text=NULL)
    label_message.grid(row=5, column=0)
    hostname = entry_hostname.get()
    port = entry_port.get()
    username = entry_username.get()
    password = entry_password.get()
    message=""

    # Print the values (you can replace print with saving to a file or database)
    print("Hostname:", hostname)
    print("Port:", port)
    print("Username:", username)
    print("Password:", password)
    

    # Construct MySQL Shell command
    #mysql_shell_command = f"mysqlsh -u" +username + " -password" +password +" -h" +hostname + "--sql -e \"select @@hostname\""
    
    command = "mysqlsh --uri " +hostname + " --user " +username + " -p"+password +" -f c:/dump/query.sql"

    #command = "mysqlsh --uri localhost --user srini -pSai1prasad -f c:/dump/query.sql"
   #command = "mysqldump -u srini -pSai1prasad  --all-databases > c:/dump/dump2.sql" 
    print(command)
    run_mysqlsh(command)

   # mysqlsh user@ds1.example.com:33060/world_x

    # Execute the MySQL Shell command


# Create the main window
root = tk.Tk()
root.title("Connect to Database")



def align_center():
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position for the window to be in the center
    x_position = (screen_width - root.winfo_reqwidth()) / 2
    y_position = (screen_height - root.winfo_reqheight()) / 2

    global success
# Create labels and entry fields
label_hostname = tk.Label(root, text="Hostname:")
label_hostname.grid(row=0, column=0, sticky="e")
entry_hostname = tk.Entry(root)
entry_hostname.grid(row=0, column=1)

label_port = tk.Label(root, text="Port:")
label_port.grid(row=1, column=0, sticky="e")
entry_port = tk.Entry(root)
entry_port.grid(row=1, column=1)

label_username = tk.Label(root, text="username:")
label_username.grid(row=2, column=0, sticky="e")
entry_username = tk.Entry(root)
entry_username.grid(row=2, column=1)

label_password = tk.Label(root, text="password:")
label_password.grid(row=3, column=0, sticky="e")
entry_password = tk.Entry(root)
entry_password.grid(row=3, column=1)

# Create a submit button
submit_button = tk.Button(root, text="Connect to Database", command=submit_form)
submit_button.grid(row=4, columnspan=4)


label_message = tk.Label(root, text=success)
#label_message.grid(row=5, column=0, sticky="e")
label_message.grid(row=5, column=0, sticky="e")

align_center()

# Bind the window resize event to the align_center function
root.bind("<Configure>", lambda e: align_center())

def run_mysqlsh(command):
    global success
    try:
        # Run mysqlsh command and capture output
        print("u r in try")
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(result)
        # Check if the command was successful
        if result.returncode == 0:
            print("MySQL Shell Output:")
            print(result.stdout)
            success="succesfully connected to database "
            
            label_message = tk.Label(root, text=success)
            label_message.grid(row=5, column=0, sticky="e")
            label_message = tk.Label(root, text="what do you want to do?")
            label_message.grid(row=5, column=0, sticky="e")
        else:
            print("Error running MySQL Shell command:")
            print(result.stderr)
            success="failed to run query"
            label_message = tk.Label(root, text=result.stderr)
            label_message.grid(row=5, column=0, sticky="e")
    except Exception as e:
        print("Exception:", e)
        label_message = tk.Label(root, text=e)
        label_message.grid(row=5, column=0, sticky="e")
# Start the Tkinter event loop
root.mainloop()
}