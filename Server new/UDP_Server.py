import socket
import binascii
import json
import datetime

port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('192.168.8.130', port))

def decodethis(data):
    length = int(data[0:4], 16)
    PacketID = int(data[4:8], 16)
    notusedB = int(data[8:10], 16)

    AVLID = int(data[10:12], 16)
    IMEILength = int(data[12:16], 16)
    IMEI = binascii.unhexlify(data[16:46])

    codecID = int(data[46:48], 16)
    record1 = int(data[48:50], 16)

    timestamp = int(data[50:66], 16)
    date_time = datetime.datetime.fromtimestamp(timestamp/1000)

    priority = int(data[66:68], 16)
    longitude = int(data[68:76], 16)
    latitude = int(data[76:84], 16)
    altitude = int(data[84:88], 16)
    angle = int(data[88:92], 16)
    satellites = int(data[92:94], 16)
    speed = int(data[94:98], 16)

    # i/o element here later

    record2 = int(data[-2:], 16)

    if (record1 == record2 and len(data[10:10 + (length)]) == length and IMEILength == 15 and notusedB == 1):
        print('everything look good')
    else:
        print('something wrong in checking')

    Dict = {
        "DataLength": str(length),
        "PacketID": str(PacketID),
        "AVLID": str(AVLID),
        "IMEILength": str(int(IMEILength)),
        "IMEI": str(IMEI),
        "codecID": str(codecID),
        "record": str(record1),
        "timestamp": str(timestamp),
        "Date_time": str(date_time),
        "priority": str(priority),
        "longitude": str(longitude),
        "latitude": str(latitude),
        "altitude": str(altitude),
        "angle": str(angle),
        "satellites": str(satellites),
        "speed": str(speed)
    }

    with open('UDP.json', 'w', encoding='utf-8') as f:
        json.dump(Dict, f, ensure_ascii=False, indent=4)

    # ack
    print("pID: " + str(data[4:8]) + "AVL: " + str(data[10:12]))#test
    return "0005" + str(format(PacketID, 'x').zfill(4)) + "01" + str(format(AVLID, 'x').zfill(2)) + str(format(record1, 'x').zfill(2))#need to work on

def start():
    print("Server is listening ...")

    while True:
        data, addr = s.recvfrom(2048)

        try:
            received = binascii.hexlify(data)

            # print stream data
            print(received)

            ack = decodethis(received).encode('utf-8')
            s.sendto(ack, addr)#not ready
            print(ack)#test

        except socket.error:
            print("Error occurred.")

start()