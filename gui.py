import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import serial
import time

class MyGUI:
    def __init__(self, master):
        bold_font = ('Trebuchet MS', 12, 'bold')
        normal_font = ('Trebuchet MS', 12)

        self.master = master
        master.title("Serial Communication GUI")
        self.test_running_displayed = False
        self.sample_frequency = 1
        self.check_sample_frequency = False
        # Create a thread for serial communication
        self.serial_thread = threading.Thread(target=self.read_serial)
        self.serial_thread.start()  # Start the serial thread

        # Input Section
        self.input_label = tk.Label(master, text="Sample Frequency (Hz):", font=bold_font)
        self.input_entry = tk.Entry(master, width=30)
        self.text_button = tk.Button(master, text="Enter", command=self.process_text)

        self.input_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        self.text_button.grid(row=0, column=2, padx=5, pady=5)

        # Label for the Text Box
        self.text_box_label = tk.Label(master, text="Test Sequence", font=bold_font)
        self.text_box_label.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.W)

        # Text Box Section
        self.text_box = scrolledtext.ScrolledText(master, width=60, height=5, font=normal_font, state=tk.DISABLED)
        self.text_box.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Clear Test Sequence Button
        self.clear_button = tk.Button(master, text="Clear Test Sequence", command=self.clear_test_sequence)
        self.clear_button.grid(row=2, column=9, padx=5, pady=5, sticky="nsew")

        # Status Box Section
        self.status_label = tk.Label(master, text="Status:")
        self.status_box = tk.Text(master, width=60, height=1, state=tk.DISABLED)
        self.status_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5, columnspan=4)
        self.status_box.grid(row=5, column=0, columnspan=4, padx=5, pady=10, sticky="nsew")
        
        # Button 1, Button 2, and Button 3 grouped together beside text box
        self.button1 = tk.Button(master, text="Test Auto", command=lambda: self.process_button("TestAuto"))
        self.button2 = tk.Button(master, text="Test Normal", command=lambda: self.process_button("TestNormal"))
        self.button3 = tk.Button(master, text="Test Serial", command=lambda: self.process_button("TestSerial"))
        self.new_button = tk.Button(master, text="Run Test", command=self.process_new_button)

        self.button1.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")
        self.button2.grid(row=2, column=5, padx=5, pady=5, sticky="nsew")
        self.button3.grid(row=2, column=6, padx=5, pady=5, sticky="nsew")
        self.new_button.grid(row=2, column=7, padx=5, pady=5, sticky="nsew")

        # Label for the Serial Read Box
        self.serial_read_label = tk.Label(master, text="Serial Read Display", font=bold_font)
        self.serial_read_label.grid(row=3, column=0, columnspan=4, pady=5, sticky=tk.W)

        # Serial Read Box Section
        self.serial_read_box = scrolledtext.ScrolledText(master, width=60, height=10, state=tk.DISABLED, font=normal_font, wrap=tk.WORD)
        self.serial_read_box.grid(row=4, column=0, padx=5, pady=5, columnspan=4, sticky="nsew")
        
        # Start Serial Button
        self.start_serial_button = tk.Button(master, text="Start Serial", command=self.start_serial)
        self.start_serial_button.grid(row=2, column=10, padx=5, pady=5, sticky="nsew")

        # Make rows and columns resizable
        for i in range(8):
            master.grid_rowconfigure(i, weight=1)
        for i in range(8):
            master.grid_columnconfigure(i, weight=1)

    # HANDLING SERIAL
    def read_serial(self):
        serial_port_read = 'COM2'
        baud_rate = 115200
        
        ser = serial.Serial(serial_port_read, baudrate=baud_rate, timeout=1)
        print(f"Serial port {serial_port_read} opened successfully for reading.")
        
        try:
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    read_data = data.decode('utf-8')
                    processed_data = self.process_data(read_data)
                    for item in processed_data:
                        self.master.after(0, self.update_serial_read_box, item)
                        print("Serial received data:")
                        print(item)
                else:
                    self.master.after(0, self.update_serial_read_box, "No data received")
                    print("No data received")

                time.sleep(1) 
                
        except Exception as e:
            print(f"Error: {e}")

        finally:
            ser.close()
            print(f"Serial port {serial_port_read} closed for reading.")

    def process_data(self, read_data):
        return read_data.split('^')

    def update_serial_read_box(self, new_data):
        current_data = self.serial_read_box.get(1.0, tk.END)
        updated_data = current_data + new_data + "\n"
        self.serial_read_box.config(state=tk.NORMAL)
        self.serial_read_box.delete(1.0, tk.END)
        self.serial_read_box.insert(tk.END, updated_data)
        self.serial_read_box.yview(tk.END)  # Scroll to the bottom
        self.serial_read_box.config(state=tk.DISABLED)
        
    def start_serial(self):
        if self.check_sample_frequency == True:
            process1 = subprocess.Popen(['start', 'cmd', '/k', 'python', 'write.py', str(self.sample_frequency), str(self.test_sequence_inputs)], shell=True)
              
            # Update Status Box
            self.status_box.config(state=tk.NORMAL)
            self.status_box.delete(1.0, tk.END)
            self.status_box.insert(tk.END, "Serial Communication Started")
            self.status_box.config(state=tk.DISABLED)
        else:
            self.show_error_message("Sample Freq not defined")

    def clear_test_sequence(self):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.config(state=tk.DISABLED)
        self.test_sequence_inputs = ""  # Clear the test sequence array
        print("Test sequence inputs and array cleared.")
    
    # errorbox message
    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def process_text(self):
        self.sample_frequency = self.input_entry.get()
        # error validation
        if self.sample_frequency.replace(".", "").isdigit():  # Check if digits (allowing a single decimal point)
            try:
                self.check_sample_frequency = True
            except ValueError:
                self.show_error_message("Input is not a float. Please try again.")
        else:
            self.show_error_message("Input contains non-digit characters. Please enter a valid float.")

    def process_button(self, message):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.test_sequence_inputs = message  # store test sequence inputs
    
    def process_new_button(self):
        self.status_box.config(state=tk.NORMAL)
        if not self.test_running_displayed:
            self.status_box.delete(1.0, tk.END)  # Clear the status box if it's not already cleared
            self.status_box.insert(tk.END, "Test Running")
            self.test_running_displayed = True
        self.status_box.config(state=tk.DISABLED)

        # Store the inputs in the test sequence array
        self.test_sequence_inputs = self.text_box.get(1.0, tk.END).strip()
        
        # Print every array input in the test_sequence_inputs array
        print("Test_sequence_inputs:")
        print(self.test_sequence_inputs)

    def update_status_box(self):
        self.status_box.update_idletasks()

    def show_serial_read_data(self, data):
        self.serial_read_box.config(state=tk.NORMAL)
        self.serial_read_box.insert(tk.END, data + "\n")
        self.serial_read_box.yview(tk.END)  # Scroll to the bottom
        self.serial_read_box.config(state=tk.DISABLED)
    
    def show_serial_write_data(self, data):
        self.serial_write_box.config(state=tk.NORMAL)
        self.serial_write_box.insert(tk.END, data + "\n")
        self.serial_write_box.yview(tk.END)  # Scroll to the bottom
        self.serial_write_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()