# Simple demo of the VL53L1X distance sensor.
# Will print the sensed range/distance every second.
import socket
import encodings
import time
import board
import adafruit_vl53l1x
import datetime


HOST = '192.168.0.104' #Fill in with local host of PI
PORT = 10370

i2c = board.I2C()  # uses board.SCL and board.SDA

vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# OPTIONAL: can set non-default values
vl53.distance_mode = 1
vl53.timing_budget = 100

vl53.start_ranging()

def is_person(data):
    if data<863:
        print("I see someone!")
        return True
    else:
        print("No one here")
        return False

def my_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server waiting for client to connect")
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        if vl53.data_ready:
            distance = vl53.distance
            person = is_person(distance)
            print("Distance: {} cm".format(distance))
            vl53.clear_interrupt()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode('utf-8')


                if str(data) == "Data":
                    print("Sending Data")
                    if person:
                        my_data = "True"
                    else:
                        my_data = "False"

                    encoded_data = my_data.encode('utf-8')

                    conn.sendall(encoded_data)
                    print("Data Sent!")

                if str(data) == "Quit":
                    print("shutting down server")

                if not data:
                    break
                else:
                    pass
                

if __name__ == '__main__':
    while True:
        my_server()
