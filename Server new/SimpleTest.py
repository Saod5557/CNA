import json
import datetime
# import binascii
BitStream = b'000000000000013e0807000001894b3e474a0117b5d47f0cd95a0500ea00fd040000000603ef010100715d03424afc430fcd0900570000000001894b3e6e500117b5d47f0cd95a0500ea00fd040000000603ef000100715503420cbd430f7a0900570000000001894b3e95600117b5d47f0cd95a0500ea00fd040000000603ef00010071550342064f430f780900570000000001894b3ebc700117b5d47f0cd95a0500eb00fd040000000603ef0001007155034203f2430f710900570000000001894b3ee3800117b5d47f0cd95a0500eb00fd040000000603ef000100715503420000430f700900570000000001894b3f0e780117b5d47f0cd95a0500eb00fd040000000603ef000100715403420000430f670900570000000001894b3f35880117b5d47f0cd95a0500ed00fd040000000603ef000100715403420000430f6809005700000700004a2c'
def decodethis(data):
    tcpHeader = int(data[0:8], 16)

    if (tcpHeader == 0):
        codec = int(data[16:18], 16)

        if (codec == 8):
            DataLength = int(data[8:16], 16)
            record1 = int(data[18:20], 16)

            timestamp = int(data[20:36], 16)
            date_time = datetime.datetime.fromtimestamp(timestamp / 1000)

            priority = int(data[36:38], 16)
            # longitude =data[38:46]
            longitude = int(data[38:46], 16)
            print(longitude)
            latitude = int(data[46:54], 16)
            print(latitude)
            altitude = int(data[54:58], 16)
            angle = int(data[58:62], 16)
            satellites = int(data[62:64], 16)
            speed = int(data[64:68], 16)

#i/o element here later

            record2 = int(data[-10:-8:1], 16)
            crc_16 = int(data[-8::1], 16)

            if(record1 == record2 and len(data[16:16+(DataLength)]) == DataLength):
                print('everything look good')
            else:
                print('something wrong in checking')

print(BitStream)
decodethis(BitStream)
x=int("f",16)
print(x)
print(bin(x))