#!/usr/bin/python2.7

import socket   #for sockets
import sys  #for exit
import numpy
import os

if __name__ == '__main__':

  frequency=sys.argv[1]
  power=sys.argv[2]

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 5025;
  remote_ip = '192.168.1.76'

  #Connect to remote server
  try:
      s.connect((remote_ip , port))
  except socket.error:
      print ('Failed to create socket')
      sys.exit()

  print ('Socket Connected to ' + ' ip ' + remote_ip)


  #Send some data to remote server
  message = 'freq ' + str(frequency) + ' GHz\n'

  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()

  print ('Frequency setting sent successfully')

  message = 'pow:ampl ' + str(power) + ' dBm\n'

  try:
      os.remove('SGparams.txt')
  except OSError:
      pass

  outfile=open('SGparams.txt','w')
  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()

  print ('Power setting sent successfully')

  message = "freq:cw?\n"

  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()

  print ('Frequency Query')
  #Now receive data
  reply = s.recv(4096)

  print ("Frequency is:  " + reply.decode().rstrip('\n') + ' Hz')
  freq_query="Frequency is:  " + reply.decode().rstrip('\n') + ' Hz\n'
  outfile.write(freq_query)

  message = "pow:ampl?\n"

  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()
  print ('Power Query')

  #Now receive data
  reply = s.recv(4096)

  print ("Power is:  " + reply.decode().rstrip('\n') + ' dBm')
  power_query="Power is:  " + reply.decode().rstrip('\n') + ' dBm\n'
  outfile.write(power_query)

  message = "OUTP ON\n"

  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()

  message = "OUTP?\n"


  try :
      #Set the whole string
      s.sendall(message.encode())
  except socket.error:
      #Send failed
      print ('Send failed')
      sys.exit()

  print ('RF output On Query')

  #Now receive data
  reply = s.recv(4096)

  print ("RF Output is:  " + reply.decode().rstrip('\n'))
  stat_query="RF Output is:  " + reply.decode().rstrip('\n')
  outfile.write(stat_query)
  outfile.close()
