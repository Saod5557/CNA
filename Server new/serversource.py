import socket

import threading

import binascii

port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('192.168.0.250', port))


def decodethis(data):
    codec = int(data[16:18], 16)

    if (codec == 8):
        lenght = int(data[8:16], 16)

        record = int(data[18:20], 16)

        timestamp = int(data[20:36], 16)

        priority = int(data[36:38], 16)

        lon = int(data[38:46], 16)

        lat = int(data[46:54], 16)

        alt = int(data[54:58], 16)

        angle = int(data[58:62], 16)

        sats = int(data[62:64], 16)  # maybe

        speed = int(data[64:68], 16)

        print("Record: " + str(record) + "\nTimestamp: " + str(timestamp) + "\nLat,Lon: " + str(lat) + ", " + str(lon) + "\nAltitude: " + str(alt) + "\nSats: " + str(sats) + "\nSpeed: " + str(speed) + "\n")

        return "0000" + str(record).zfill(4)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:

        imei = conn.recv(1024)

        try:

            message = '\x01'

            message = message.encode('utf-8')

            conn.send(message)

        except:

            print("Error sending reply. Maybe it's not our device")

        try:

            data = conn.recv(1024)

            recieved = binascii.hexlify(data)

            record = decodethis(recieved).encode('utf-8')

            conn.send(record)

        except socket.error:

            print("Error Occured.")

            break

    conn.close()


def start():
    s.listen()

    print(" Server is listening ...")

    while True:
        conn, addr = s.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")

start()