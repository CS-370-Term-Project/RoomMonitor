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

def is_person():
    if vl53.data_ready:
        distance = vl53.distance
        vl53.clear_interrupt()

    if distance == None:
        distance = 100

    if distance<50:
        print("Distance: {} cm".format(distance))
        return True
    else:
        return False

def my_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server waiting for client to connect")
        s.bind((HOST, PORT))
        s.listen(5)
        connection, addr = s.accept()

        with connection:
            print('Connection From', addr)
            while True:
                data = connection.recv(1024).decode('ascii')

                if str(data) == "Data":
                    print("Sending Data")
                    if is_person():
                        my_data = "True"
                        print("Sent True")
                    else:
                        my_data = "False"
                        print("Sent False")

                    encoded_data = my_data.encode('ascii')

                    connection.sendall(encoded_data)
                    print("Data Sent!")

                if str(data) == "Quit":
                    print("shutting down server")
                    connection.close()
                    exit()

                if not data:
                    break
                else:
                    pass
                

if __name__ == '__main__':
    while True:
        my_server()
