from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 3.0
NUM_PACKETS = 3

def checksum(str_):
    # In this function we make the checksum of our packet 
    str_ = bytearray(str_)
    csum = 0
    countTo = (len(str_) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = str_[count+1] * 256 + str_[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(str_):
        csum = csum + str_[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def sendOnePing(mySocket, destAddr):
    
    myChecksum = 0
    myID = os.getpid() & 0xFFFF
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data) 

    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 0))
   
def ping(destName):
    
    destAddr = gethostbyname(destName)
    icmp = getprotobyname("icmp")
    print("Pinging " + destAddr + "(" + destName + ")" + " using Python:")
    
    for ttl in range(1,MAX_HOPS):
        timeLeft = TIMEOUT
        end = False
        hopAddr = ""
        print(" %d   "%ttl, end="")
        for i in range(NUM_PACKETS):
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                sendOnePing(mySocket, destAddr)
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    print("   *    ", end = "")

                recvPacket, addr = mySocket.recvfrom(1024)
                hopAddr = addr[0]
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                     print("   *    ", end = "")

            except timeout:
                continue

            else:
                icmpHeader = recvPacket[20:28]
                icmpType, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                byte = struct.calcsize("d")
                timeSent = struct.unpack("d", recvPacket[28:28 + byte])[0]
                if icmpType == 11:
                    print ("%.0f ms    " % ((timeReceived -t)*1000), end = "")
                    # print("TTL expired!")
                    # return
                elif icmpType == 0:
                    print ("%.0f ms    " % ((timeReceived -timeSent)*1000), end = "")
                    end = True
                else:
                    print ("error")
                    break
            finally:
                mySocket.close()
        if hopAddr != "":
            print(hopAddr)
        else:
            print("")
        if end:
            return

if __name__ == '__main__':	
	
	# ping("google.com")
    website = str(sys.argv[1])
    ping(website)