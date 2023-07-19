import socket
# import threading
import binascii
import json
import datetime

port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('192.168.8.116', port))


def decodethis(data,imei):
    IMEILength = int(imei[0:4], 16)
    IMEI = binascii.unhexlify(imei[4:34])

    tcpHeader = int(data[0:8], 16)

    if (tcpHeader == 0):
        codec = int(data[16:18], 16)

        if (codec == 8):

            DataLength = int(data[8:16], 16)
            record1 = int(data[18:20], 16)

            timestamp = int(data[20:36], 16)
            date_time = datetime.datetime.fromtimestamp(timestamp / 1000)

            priority = int(data[36:38], 16)
            longitude = int(data[38:46], 16)
            latitude = int(data[46:54], 16)
            altitude = int(data[54:58], 16)
            angle = int(data[58:62], 16)
            satellites = int(data[62:64], 16)
            speed = int(data[64:68], 16)

#i/o element here later

            record2 = int(data[-10:-8:1], 16)
            crc_16 = int(data[-8::1], 16)

            if(record1 == record2):
                record = int(data[18:20], 16)
                record_check_is_good = True
            else:
                print('something wrong in checking record')
                record = int(data[18:20], 16)
                record_check_is_good = False

            print("\nDataLength: "+str(DataLength) + "\ncodec: "+str(codec) + "\nrecord: "+str(record) + '\ntimestamp: '+str(timestamp) + '\npriority: '+str(priority) + "\nlongitude: "+str(longitude) + "\nlatitude: "+str(latitude) + "\naltitude: "+str(altitude) + "\nangle: "+str(angle) + "\nsatellites: "+str(satellites) + "\nspeed: "+str(speed) + "\ncrc-16: "+str(crc_16) )
            Dict = {
                "IMEILength": str(int(IMEILength)),
                "IMEI": str(IMEI),
                "DataLength": str(DataLength),
                "codec": str(codec),
                "record": str(record),
                "record_check_is_good": record_check_is_good,
                "timestamp": str(timestamp),
                "Date_time": str(date_time),
                "priority": str(priority),
                "longitude": str(longitude),
                "latitude": str(latitude),
                "altitude": str(altitude),
                "angle": str(angle),
                "satellites": str(satellites),
                "speed": str(speed),
                "crc-16": str(crc_16)
            }
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(Dict, f, ensure_ascii=False, indent=4)

            return "0000" + str(record).zfill(4)
        else:
            print("not codec 8")
            return "0000"
    else:
        print("not tcp")
        return "0000"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:

        imei = binascii.hexlify(conn.recv(1024))

        try:

            message = '\x01'

            message = message.encode('utf-8')

            conn.send(message)

        except:

            print("Error sending reply. Maybe it's not our device")

        try:

            data = conn.recv(1024)

            recieved = binascii.hexlify(data)

            #print stream data
            print(str(recieved))

            record = decodethis(recieved,imei)

            conn.send(record.encode('utf-8'))

        except socket.error:

            print("Error Occured.")

            break

    conn.close()


def start():
    s.listen()

    print(" Server is listening ...")

    while True:
        conn, addr = s.accept()

        handle_client(conn,addr)
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()

        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")

start()