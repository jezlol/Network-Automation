import paramiko
import time
from tkinter import Toplevel, Button, Label
from quick_commands import open_quick_command_script_window
from cli_window import open_cli_window
from routing_window import open_routing_window
from redistribution import open_redistribution_window
from eras import erase_router_config  # Import the erase function

# Function to open the option selection window
def open_option_window(shell, router_name, device_ip, result_text):
    option_window = Toplevel()
    option_window.title(f"Connected to {router_name} ({device_ip})")
    
    Label(option_window, text=f"Connected to {router_name} ({device_ip})").pack(pady=10)

    # Buttons for each option
    Button(option_window, text="CLI", command=lambda: open_cli_window(shell, router_name, device_ip, result_text)).pack(pady=5)
    Button(option_window, text="Quick Command Scripts", command=lambda: open_quick_command_script_window(shell, router_name, device_ip, result_text)).pack(pady=5)
    Button(option_window, text="Routing", command=lambda: open_routing_window(shell, router_name, device_ip, result_text)).pack(pady=5)
    Button(option_window, text="Redistribute Routes", command=lambda: open_redistribution_window(shell, router_name, device_ip, result_text)).pack(pady=5)
    Button(option_window, text="Erase Config", command=lambda: erase_router_config(shell, router_name, result_text)).pack(pady=5)

# SSH login function remains the same
def login_via_ssh(router_name, device_ip, result_text):
    username = "jez"
    password = "123"
    enable_password = "123"

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=device_ip, username=username, password=password)
        
        shell = client.invoke_shell()

        # Wait for the prompt and clear the buffer
        time.sleep(1)
        shell.recv(1000)

        # Send 'enable' command
        shell.send('enable\n')
        time.sleep(1)
        shell.recv(1000)  # Clear the buffer

        # Send the enable password
        shell.send(f'{enable_password}\n')
        time.sleep(1)
        shell.recv(1000)  # Clear the buffer again

        # Open the option window for further actions
        open_option_window(shell, router_name, device_ip, result_text)

    except Exception as e:
        result_text.delete("1.0", "end")
        result_text.insert("end", f"SSH login failed for {router_name} ({device_ip}): {str(e)}\n")
