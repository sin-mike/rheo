import threading
from collections import deque
import numpy as np
import time
import serial
import HumanIO

class remgSerialInterface(HumanIO.HumanStateReader):
    """
    A class to interface with a serial port, read incoming data, and store it in a deque for further processing.

    Attributes:
    port (str): The serial port to connect to.
    baudrate (int): The baud rate for the serial communication.
    data_len (int): The length of the data frame to read from the serial port.
    ser (serial.Serial): The serial port object.
    thread (threading.Thread): The thread object for reading data.
    running (bool): A flag to indicate if the reading thread is running.
    """

    def __init__(self, port):
        """
        Initializes the remgSerialInterface with the specified serial port.

        Args:
        port (str): The serial port to connect to.
        """

        if HumanIO.__version__ != "0.0.1":
            print(f"HumanIO version {HumanIO.__version__} has not been tested with this device. \r\nPlease install HumanIO version 0.0.1.")

        super(remgSerialInterface, self).__init__()

        self.device_name = "REMG"
        self.port = port
        self.baudrate = 921600
        self.data_len = 152
        self.ser = None
        self.thread = None
        self.running = False
        self.CYCLE_MS = 20
        self.SFREQ = 1000/self.CYCLE_MS
        self.EMG_IDX = list(range(0, 12))
        self.RMG_IDX = list(range(12, 24))

        try:
            if self.ser:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.002)
            print(f"Opened serial port {self.port} at {self.baudrate} baud")
        except Exception as e:
            print(f"Error opening serial port: {e}")


    def read_serial(self):
        """
        Reads data from the serial port and stores it in the deque.
        """
        print("Started Serial While Loop")
        while self.ser.in_waiting > 0:
            self.ser.read(self.ser.in_waiting)
            time.sleep(0.001)

        while self.running:
            if self.ser.in_waiting > 0:
                data_raw = self.ser.read(self.data_len)
                if len(data_raw) == self.data_len:
                    data = np.frombuffer(data_raw, dtype=np.uint8)
                    start_byte = data[0]
                    frame = np.frombuffer(data_raw[1:(4*24+1)], dtype=np.int32)
                    crc = data[-1] # not used
                    self.update_state(frame, state_id=start_byte)
                    
            time.sleep(0.005)

    def start_reading(self):
        """
        Starts the reading thread to read data from the device.
        """
        self.running = True
        self.ts_launch = time.time()
        self.thread = threading.Thread(target=self.read_serial)
        self.thread.start()
        print("Started reading thread")

    def stop_reading(self):
        """
        Stops the reading thread and closes the serial port.
        """
        self.running = False
        if self.thread:
            self.thread.join()
            print("Joined reading thread")

        if self.ser:
            self.ser.close()
            print("Closed serial port")


if __name__ == "__main__":
    """
    Main function to run the remgSerialInterface module as a standalone script.
    """
    import sys

    if len(sys.argv) != 2:
        print("Usage: python remgSerialInterface.py <serial_port>")
        sys.exit(1)

    port = sys.argv[1]
    remg = remgSerialInterface(port)
    remg.start_reading()
    time.sleep(1)
    for i in range(100):
        if remg.have_state():
            state_id, state_ts, state = remg.get_state()
            print(state_id, state_ts, list(state[remg.EMG_IDX]), list(state[remg.RMG_IDX]), end=" "*50+'\r')
        else:
            time.sleep(0.005)       
    remg.stop_reading()
