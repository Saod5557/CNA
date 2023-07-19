import json
import binascii
import datetime

BitStream = b'0153cafe011b000f3335303534343530343934333931340807000001895e7d7e700117d129700cb5df0400000000000000000603ef010100715a03422a5e430faa0900570000000001895e7da5800117d129700cb5df0400000000000000000603ef000100715a03420c4d430faa0900570000000001895e7dcc900117d129700cb5df0400000000000000000603ef000100715503420689430f790900570000000001895e7df3a00117d129700cb5df0400000000000000000603ef0001007157034203fd430f8d0900570000000001895e7e1ab00117d129700cb5df0400000000000000000603ef000100715703420000430f8e0900570000000001895e7e41c00117d129700cb5df0400000000000000000603ef000100715703420000430f8a0900570000000001895e7e68d00117d129700cb5df0400000000000000000603ef000100715603420000430f86090057000007'
# BitStream = b'000000000000013e0807000001894b3e474a0117b5d47f0cd95a0500ea00fd040000000603ef010100715d03424afc430fcd0900570000000001894b3e6e500117b5d47f0cd95a0500ea00fd040000000603ef000100715503420cbd430f7a0900570000000001894b3e95600117b5d47f0cd95a0500ea00fd040000000603ef00010071550342064f430f780900570000000001894b3ebc700117b5d47f0cd95a0500eb00fd040000000603ef0001007155034203f2430f710900570000000001894b3ee3800117b5d47f0cd95a0500eb00fd040000000603ef000100715503420000430f700900570000000001894b3f0e780117b5d47f0cd95a0500eb00fd040000000603ef000100715403420000430f670900570000000001894b3f35880117b5d47f0cd95a0500ed00fd040000000603ef000100715403420000430f6809005700000700004a2c'
# BitStream = b'000000000000004308020000016B40D57B480100000000000000000000000000000001010101000000000000016B40D5C198010000000000000000000000000000000101010101000000020000252C'
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
    date_time = datetime.datetime.fromtimestamp(timestamp / 1000)

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
    print("pID: " + str(data[4:8]) + "AVL: " + str(data[10:12]) + "rec: " + str(data[48:50]))#test
    return "0005" + str(format(PacketID, 'x').zfill(4)) + "01" + str(format(AVLID, 'x').zfill(2)) + str(format(record1, 'x').zfill(2))

ack = decodethis(BitStream).encode('utf-8')
print(ack)#test

