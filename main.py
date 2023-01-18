import os
import threading
from time import sleep

MASK = '0b11111111111111111111111111111111'

class MyThread(threading.Thread):
  def __init__(self, ip):
    # calling parent class constructor
    threading.Thread.__init__(self)
    self.ip = ip
    self.response = 1
    
  # define your own run method
  def run(self):
    self.response = os.system("ping -n 1 " + self.ip + "> nul")
    

def toOct(ip):
  ipb = bin(ip)[2:]
  return str(int('0b' + ipb[:8], 2)) + '.' + str(int('0b' + ipb[8:16], 2)) + '.' + str(int('0b' + ipb[16:24], 2)) + '.' + str(int('0b' + ipb[24:], 2))


def getMyIp():
  os.system("ipconfig > ip")
  f = open("ip", 'r')
  data = f.read()
  f.close()
  data = data.split('Adaptador')
  for d in range(1, len(data)):
    if "Wi-Fi" in data[d]:
      data = data[d].split('\n')
      for i in data:
        if "IPv4" in i:
          ip = i.split(':')[1].strip()
        if "M\xa0scara" in i:
          mask = i.split(':')[1].strip()
  return ip, mask
  

def main():

  ip, mask = getMyIp()
  ip8 = [(int(oct)) for oct in ip.split('.')]
  mask8 = [(int(oct)) for oct in mask.split('.')]
  netId = [(ip8[i] & mask8[i]) for i in range(4)]
  print(ip8, mask8)
  print(netId)

  wildMask = int('0b' + bin((mask8[0]))[2:].zfill(8) +  bin(mask8[1])[2:].zfill(8) + bin(mask8[2])[2:].zfill(8) + bin(mask8[3])[2:].zfill(8), 2) ^ int(MASK, 2)
  wildMask = '0b' + bin(wildMask)[2:].zfill(32)
  limit = int(wildMask, 2)
  netIdBin = ('0b' + bin(ip8[0])[2:].zfill(8) +  bin(ip8[1])[2:].zfill(8) + bin(ip8[2])[2:].zfill(8) + bin(ip8[3])[2:].zfill(8))

  listOdThreads = []

  for i in range(1, limit+1):
    ip = int(netIdBin, 2) + i
    print(toOct(ip), end=" ")
    tr = MyThread(toOct(ip))
    tr.start()
    listOdThreads.append(tr)

  sleep(10)

  for t in listOdThreads:
    if t.response == 0:
      print(t.ip)



  




if __name__ == "__main__":
  main()