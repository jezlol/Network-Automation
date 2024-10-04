from tkinter import Toplevel, Label, Entry, Button, StringVar, OptionMenu, Frame

def open_redistribution_window(shell, router_name, device_ip, result_text):
    redistribution_window = Toplevel()
    redistribution_window.title(f"Redistribute Routes - {router_name} ({device_ip})")

    # Select source protocol
    Label(redistribution_window, text="Select Source Protocol:").pack(pady=5)
    source_protocol = StringVar(redistribution_window)
    source_protocol.set("OSPF")  # Default option
    protocol_options = ["OSPF", "STATIC", "RIP", "EIGRP"]
    protocol_menu = OptionMenu(redistribution_window, source_protocol, *protocol_options)
    protocol_menu.pack(pady=5)

    # Frame to dynamically add/remove input fields
    input_frame = Frame(redistribution_window)
    input_frame.pack(pady=5)

    # Dynamic Input Fields (will be cleared and recreated depending on protocol)
    process_id_entry = None
    metric_entry = None
    as_number_entry = None

    # Function to update input fields based on protocol selection
    def update_input_fields(*args):
        nonlocal process_id_entry, metric_entry, as_number_entry  # Declare nonlocal variables at the beginning
        # Clear the current input frame
        for widget in input_frame.winfo_children():
            widget.destroy()

        # OSPF protocol-specific input
        if source_protocol.get() == "OSPF":
            Label(input_frame, text="Enter OSPF Process ID:").pack(pady=5)
            process_id_entry = Entry(input_frame, width=30)
            process_id_entry.pack(pady=5)

            Label(input_frame, text="Enter Metric (optional):").pack(pady=5)
            metric_entry = Entry(input_frame, width=30)
            metric_entry.pack(pady=5)

        # STATIC protocol-specific input
        elif source_protocol.get() == "STATIC":
            Label(input_frame, text="Enter Metric (optional):").pack(pady=5)
            metric_entry = Entry(input_frame, width=30)
            metric_entry.pack(pady=5)

        # RIP protocol-specific input
        elif source_protocol.get() == "RIP":
            Label(input_frame, text="Enter Metric (optional):").pack(pady=5)
            metric_entry = Entry(input_frame, width=30)
            metric_entry.pack(pady=5)

        # EIGRP protocol-specific input
        elif source_protocol.get() == "EIGRP":
            Label(input_frame, text="Enter EIGRP AS Number:").pack(pady=5)
            as_number_entry = Entry(input_frame, width=30)
            as_number_entry.pack(pady=5)

            Label(input_frame, text="Enter Metric (optional):").pack(pady=5)
            metric_entry = Entry(input_frame, width=30)
            metric_entry.pack(pady=5)

    # Attach update_input_fields to the protocol dropdown selection
    source_protocol.trace('w', update_input_fields)

    # Initialize with OSPF fields by default
    update_input_fields()

    # Function to configure redistribution based on selected source protocol
    def configure_redistribution():
        protocol = source_protocol.get()
        process_id = process_id_entry.get() if process_id_entry else ""
        metric = metric_entry.get() if metric_entry else ""
        as_number = as_number_entry.get() if as_number_entry else ""

        if protocol == "OSPF" and process_id:
            command = f"router ospf {process_id}\nredistribute {protocol.lower()} subnets metric {metric}\n" if metric else f"router ospf {process_id}\nredistribute {protocol.lower()} subnets\n"
        elif protocol == "STATIC":
            command = f"redistribute static metric {metric}\n" if metric else "redistribute static\n"
        elif protocol == "RIP":
            command = f"redistribute rip metric {metric}\n" if metric else "redistribute rip\n"
        elif protocol == "EIGRP" and as_number:
            command = f"router eigrp {as_number}\nredistribute {protocol.lower()} 10 metric {metric}\n" if metric else f"router eigrp {as_number}\nredistribute {protocol.lower()} 10\n"
        else:
            result_text.insert("end", "Error: Please provide necessary inputs\n")
            return

        # Send command to shell and get the output
        try:
            shell.send(command)
            time.sleep(2)
            output = shell.recv(10000).decode('utf-8')
            result_text.insert("end", f"{router_name} - Configured redistribution:\n{output}\n")
        except Exception as e:
            result_text.insert("end", f"Error configuring redistribution: {str(e)}\n")

    # Button to execute redistribution configuration
    configure_button = Button(redistribution_window, text="Configure Redistribution", command=configure_redistribution)
    configure_button.pack(pady=5)

    # Back Button to return to the previous window
    def go_back():
        redistribution_window.destroy()

    back_button = Button(redistribution_window, text="Back", command=go_back)
    back_button.pack(pady=10)
