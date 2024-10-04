from tkinter import Toplevel, Button, Label
from arp_commands import show_arp_table, clear_arp_table
from traceroute import traceroute_script
import time
from assign_ip import open_assign_ip_window

# Function to open the Quick Command Scripts window
def open_quick_command_script_window(shell, router_name, device_ip, result_text):
    quick_window = Toplevel()
    quick_window.title(f"Quick Command Scripts for {router_name} ({device_ip})")

    Label(quick_window, text=f"Quick Command Scripts for {router_name}").pack(pady=10)

    # Quick command: Assign IP
    def assign_ip_script():
        quick_window.destroy()
        open_assign_ip_window(shell, router_name, device_ip, result_text)

    # Quick command: Configure Static Route
    def route_script():
        quick_window.destroy()
        open_route_config_window(shell, router_name, device_ip, result_text)

    # Quick command: Show IP Interface Brief
    def show_ip_interface_brief():
        try:
            shell.send('show ip interface brief\n')
            time.sleep(2)
            output = shell.recv(10000).decode('utf-8')
            result_text.insert("end", f"{router_name} - show ip interface brief:\n{output}\n")
        except Exception as e:
            result_text.insert("end", f"Error running 'show ip interface brief': {str(e)}\n")

    # Buttons for each quick command
    assign_ip_button = Button(quick_window, text="Assign IP to Interface", command=assign_ip_script)
    assign_ip_button.pack(pady=5)

    route_button = Button(quick_window, text="Configure Static Route", command=route_script)
    route_button.pack(pady=5)

    show_ip_button = Button(quick_window, text="Show IP Interface Brief", command=show_ip_interface_brief)
    show_ip_button.pack(pady=5)

    # Traceroute Button
    traceroute_button = Button(quick_window, text="Traceroute", command=lambda: traceroute_script(shell, router_name, device_ip, result_text))
    traceroute_button.pack(pady=5)

    # Move ARP commands into Quick Command Scripts
    show_arp_button = Button(quick_window, text="Show ARP Table", command=lambda: show_arp_table(shell, router_name, result_text))
    show_arp_button.pack(pady=5)

    clear_arp_button = Button(quick_window, text="Clear ARP Table", command=lambda: clear_arp_table(shell, router_name, result_text))
    clear_arp_button.pack(pady=5)

    # Back Button to return to the main option window
    back_button = Button(quick_window, text="Back", command=lambda: go_back(quick_window, shell, router_name, device_ip, result_text))
    back_button.pack(pady=10)

def go_back(quick_window, shell, router_name, device_ip, result_text):
    quick_window.destroy()
    open_option_window(shell, router_name, device_ip, result_text)
