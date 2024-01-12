import serial
import sys
import time

sample_frequency = 1 #user defined freq in Hz
baud_rate = 115200 
data_to_publish = ""

serial_port_publish = 'COM1'
serial_port_read = 'COM2'

def send_auto_mode():
    normal_mode_values = normal_mode_datagram()

    for i in range(len(normal_mode_values)):
        print(normal_mode_values[i])
        publish_to_serial(serial_port_publish, normal_mode_values[i])

def send_serial_num():
    serial_num_values = serial_num_datagram()

    for i in range(len(serial_num_values)):
        print(serial_num_values[i])
        publish_to_serial(serial_port_publish, serial_num_values[i])

def normal_mode_datagram():
    # Normal mode datagram value for 0x91 - rate and inclination. gyro and acc values are randomised
    datagram_id = "0x91" #rate and inclination
    gyro_data_x = "2.00"
    gyro_data_y = "-1.23"
    gyro_data_z = "3.15"
    gyro_status = "0" #8 bit 0000 0000 for ok
    acc_data_x = "0.00"
    acc_data_y = "0.00"
    acc_data_z = "9.81"
    acc_status = "0" #8 bit 0000 0000 for ok
    counter = "127"  # 8-bit integer
    latency = "40000"  # 16-bit for 40000 microseconds
    crc = "0xC3562699" #32 bit crc. no dummy bytes needed for 0x91

    # Concatenate into big string with delimiter
    normal_mode_values = "datagram_id:" + "^" + datagram_id + "^" + "gyro_data_x:" + "^" + gyro_data_x + "^" + "gyro_data_y" + "^" + gyro_data_y + "^" + "gyro_data_z" + "^" + gyro_data_z  + "^" + "gyro_status" + "^" + gyro_status +  "^" + "acc_data_x" + "^" +  acc_data_x +  "^" + "acc_data_y" + "^" + acc_data_y + "^" + "acc_data_z" + "^" +  acc_data_z + "^" + "acc_status" + "^" +  acc_status + "^" +  "counter" + "^" + counter + "^" + "latency" + "^" +  latency + "^" + "crc" + "^" +  crc

    return normal_mode_values

def serial_num_datagram():
    #12 bytes: 8 byte serial num, 4 byte CRC
    serial_num = "ABCD1234"
    crc = "0xC3562699"  # 32 bit crc. no dummy bytes needed for 0x91
    
    serial_num_datagram = "serial_num:" + "^" + serial_num + "^" + "crc" + "^" + crc + "^"
    
    return serial_num_datagram
            
def publish_to_serial(serial_port, values):
    try:
        ser.write(values.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

def transmit_part_number():
    print("Transmitting Part Number datagram")
    send_auto_mode()

def transmit_serial_number():
    print("Transmitting Serial Number datagram")

def transmit_configuration():
    print("Transmitting Configuration datagram") #blank for now

def transmit_bias_trim_offset():
    print("Transmitting Bias Trim Offset datagram") #blank for now

def transmit_extended_error_info():
    print("Transmitting Extended Error Information datagram") #blank for now

def reset_unit():
    print("Resetting the unit") #blank for now

def enter_service_mode():
    print("Entering Service Mode") #blank for now

def enter_utility_mode():
    print("Entering Utility Mode") #blank for now

def switch_mode(mode, auto_switch, counter):
    print(sample_frequency)
    if auto_switch:
        while True:
            mode()
            time.sleep((1/sample_frequency))  # Sleep for 0.5 seconds before the next iteration
            counter = counter + 1
            if counter == ((1/sample_frequency)*sample_frequency)*1: #send 5 packets according to frequency
                auto_switch = False
                print("Test ended")
                counter = 0
                break
def menu():
    while True:
        auto_switch = True
        counter = 0
        test_sequence = sys.argv[2]
        test_commands = test_sequence.split()

        for command in test_commands:
            stripped_command = ''.join(filter(str.isalpha, command)) #strips commands to alpha char
            
            print(stripped_command)
            
            if stripped_command == "TestAuto":
                switch_mode(send_auto_mode, auto_switch, counter)
            elif stripped_command == "TestNormal":
                switch_mode(send_auto_mode, auto_switch, counter)
            elif stripped_command == "TestSerial":
                switch_mode(send_serial_num, auto_switch, counter)
            else:
                pass
            
            time.sleep(1)
            
if __name__ == "__main__":   
    ser = serial.Serial(serial_port_publish, baudrate=baud_rate, timeout=1)
    print(f"Serial port {serial_port_publish} opened successfully.")
    sample_frequency = float(sys.argv[1])
    print(sample_frequency)
    menu()
    
    