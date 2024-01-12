import serial
import time

def read_serial(serial_port, baud_rate):
    ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)
    print(f"Serial port {serial_port} opened successfully for reading.")
    
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                read_data = data.decode('utf-8')
                processed_data = process_data(read_data)
                print("Serial received data:")
                print(processed_data)
            else:
                print("No data received")

            time.sleep(1) 
            
    except Exception as e:
        print(f"Error: {e}")

    finally:
        ser.close()
        print(f"Serial port {serial_port} closed for reading.")

def process_data(read_data):
    return read_data.split('^')
    
if __name__ == "__main__":
    serial_port_read = 'COM2'
    baud_rate = 115200
    read_serial(serial_port_read, baud_rate)