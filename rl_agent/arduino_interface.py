import serial
import time

# Request codes
MOTOR_CONTROL = 1000
RESET_CODE = 6666

# Response codes
NOMINAL = 1111
ERROR = 9999

# Constants for communication
END_CHAR = '>'
MESSAGE_TERMINATOR = '\n'
DELIMITER = ','


def read_serial_line(serial_device: serial.Serial):
    """
       Reads data from Serial (from Arduino) with a safe check for end char

       Args:
           serial_device (serial.Serial): The Serial device
       Returns:
           (str): The output of the line, or None if invalid message
    """
    data_line = serial_device.readline().decode().strip()
    if END_CHAR in data_line:
        data_list = data_line.replace(END_CHAR, '').split(DELIMITER)
    else:
        data_list = None
    return data_list


def write_serial_line(serial_device: serial.Serial, code_array, write_timeout=3):
    """
    Args:
        serial_device (serial.Serial): The Serial device
        code_array (list): The sequence of codes/values to send to Arduino

    Returns:
        (bool): True for successful write, False for timeout

    """
    message = ','.join([str(x) for x in code_array]) + END_CHAR + MESSAGE_TERMINATOR

    # Track write time or timeout
    write_success = True
    write_start = time.time()
    serial_device.write(str(message).encode())

    # Attempt to write message
    print('Writing serial message...')
    while (serial_device.out_waiting > 0) and (time.time() - write_start < write_timeout):
        time.sleep(0.05)
    if (time.time() - write_start > write_timeout) and (serial_device.out_waiting > 0):
        write_success = False

    # Reset buffer
    serial_device.reset_output_buffer()

    return write_success


def initialize_serial(serial_port='/dev/cu.usbmodem14101', baud_rate=9600, timeout=2):
    serial_device = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=timeout)
    serial_device.flush()
    time.sleep(2)
    return serial_device

def loop():
    # Testing
    read_start = time.time()
    while arduino.in_waiting <= 0 and time.time() - read_start < read_timeout:
        time.sleep(0.05)

if __name__ == '__main__':
    # Initialize serial port
    serial_port = '/dev/cu.usbmodem14101'
    baud_rate = 9600
    timeout = 3
    arduino = initialize_serial(serial_port=serial_port, baud_rate=baud_rate, timeout=timeout)

    #
