#!/usr/bin/python2.7

import socket   #for sockets
import sys  #for exit
import numpy
import os

if __name__ == '__main__':

  #create an INET, STREAMing socket
  try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error:
      print 'Failed to create socket'
      sys.exit()

  print 'Socket Created'

  port = 5025;

  remote_ip = '192.168.1.76'

  #Connect to remote server
  s.connect((remote_ip , port))

  print 'Socket Connected to ' + ' ip ' + remote_ip

  try:
      os.remove('/var/www/cgi-bin/GLT/SGQueryparams.txt')
  except OSError:
      pass

  outfile=open('/var/www/cgi-bin/GLT/SGQueryparams.txt','w')

  message = "freq:cw?\n"

  try :
      #Set the whole string
      s.sendall(message)
  except socket.error:
      #Send failed
      print 'Send failed'
      sys.exit()

  print 'Frequency Query'
  #Now receive data
  reply = s.recv(4096)

  print "Frequency is:  " + reply.rstrip('\n') + ' Hz'
  freq_query= reply.rstrip('\n') + '\n'
  outfile.write(freq_query)

  message = "pow:ampl?\n"

  try :
      #Set the whole string
      s.sendall(message)
  except socket.error:
      #Send failed
      print 'Send failed'
      sys.exit()
  print 'Power Query'

  #Now receive data
  reply = s.recv(4096)

  print "Power is:  " + reply.rstrip('\n') + ' dBm'
  power_query= reply.rstrip('\n') + '\n'
  outfile.write(power_query)

  message = "OUTP?\n"


  try :
      #Set the whole string
      s.sendall(message)
  except socket.error:
      #Send failed
      print 'Send failed'
      sys.exit()

  print 'RF output On Query'

  #Now receive data
  reply = s.recv(4096)

  print "RF Output is:  " + reply.rstrip('\n')
  stat_query= reply.rstrip('\n')
  outfile.write(stat_query)
  outfile.close()
