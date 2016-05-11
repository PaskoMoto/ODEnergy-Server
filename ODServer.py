# (c) PaskoMoto -- 11/05/2016 --
#!/usr/bin/python

import binascii
import socket
import time 
import datetime
import base64
import sys
import string

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 1730))
s.listen(5)

##################### Gestion de las tramas recibidas de odenergy #####################################################

LOG = open('/media/ODEnergy/log.txt','a')

while True:
  sc, addr = s.accept()
  data = sc.recv(2048)

  if data[0:4] == "TIME":
    sc.send(str(int(time.time()))+"\n")
    packet_type = "TIME"
  else: 
    packet_type = data[19:21]
    packet_size = len(data)
    try:
      message_size = int(data[22:27])
    except ValueError:
      packet_type = packet_type+"ERROR_"
      packet_size = 0
      LOG.write("*************************************"+"\n")
      LOG.write("***** Error detectando longitud *****"+"\n")
      message_size = 0
    message_size = message_size - packet_size
    LOG.write("---------------------------------------------"+"\n")

    while (message_size > 0) and (packet_size !=0):
          data1 = sc.recv(2048)
          packet_size = len(data1)
          message_size = message_size - packet_size
          data = data + data1
    if packet_size == 0:
       sc.send("ODERR\n")
       packet_type = packet_type+"ERROR"
       LOG.write("enviando ODERR..... Tipo de Trama: "+packet_type+"\n")
       LOG.write(data+"\n")
       LOG.write(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d,%H:%M:%S') + "\n")
    else:
       sc.send("ODEOK\n")
       LOG.write("enviando ODEOK..... Tipo de Trama: "+packet_type+"\n")
       LOG.write(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d,%H:%M:%S') + "\n")

#################### Cerrar conexiones y eliminar cabaceras estaticas y espacios al final.###################

  LOG.flush()
  sc.shutdown(2)
  sc.close()
  data = data[28:len(data)-3]
  lista = data.split(" ")

#################### Gestion de la trama recibida ###########################################################

############ Convertir cada elemento de la trama a formato comun, separado por comas. #######################

  if packet_type == "PW":    ########################### tramas de consumo promediado #######################
     PW = open('/media/ODEnergy/PW.csv','a')
     for elemento in lista:
        timing = elemento[1:11]
        valores = elemento[12:].split(",")
        elemento = datetime.datetime.fromtimestamp(int(timing)).strftime('%Y-%m-%d,%H:%M:%S') + "," + elemento[12:]
        PW.write(elemento+"\n")
     PW.close()
 
  elif packet_type == "SG":   #########################  tramas de variacion instantanea ####################
     EV = open('/media/ODEnergy/EV.csv','a')
     for elemento in lista:
	timing = elemento[3:13]
        valores = elemento[14:].split(",")
        elemento = datetime.datetime.fromtimestamp(int(elemento[3:13])).strftime('%Y-%m-%d,%H:%M:%S') + elemento[13:len(elemento)]
        EV.write(elemento+"\n")
     EV.close()

  elif packet_type == "ST":  #########################   tramas de estado y contadores acumulados de consumo ###
     ST = open('/media/ODEnergy/ST.csv','a')
     for elemento in lista[1:3]:
        if elemento[0] == "T":
	   timing = elemento[3:13]
           elemento = elemento[0:2] + "-->" + datetime.datetime.fromtimestamp(int(elemento[3:13])).strftime('%Y-%m-%d,%H:%M:%S')
        else:
           elemento = elemento
           valores = elemento[3:].split(",")
        ST.write(elemento+"\n")
     ST.close()
  conn.close()
s.end()
