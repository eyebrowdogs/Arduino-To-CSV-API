import serial,csv, serial.tools.list_ports
from datetime import datetime
import time
import os
import re
import sys
from arduinouploader import *
import logging
import json
import platform

verbose = False
ldebug = True
verbp = print if verbose else lambda x: None
debugp = print if ldebug else lambda *x,**y: None



class SerialLogger:
    def __init__(self,baud=9600,parity="N",stopbits=1):
        self.baud = baud
        self.parity = parity
        self.stopbits = stopbits
        pass
        #defaul values
        
    def nojson(self):
        self.filesPathj = None
        self.prefixj = None
        self.sufixj = None
        self.timestampFj = "%d-%m-%Y-%H:%M:%S"
        self.baudratej = None
        self.portj = None
        self.CAj = False
        self.livePlotsj = False
        self.timerj = False

    def connector(self,port,tries=4):
        try:
            connection = serial.Serial(port,baudrate=self.baud,parity=self.parity,stopbits=self.stopbits)
            connection.reset_input_buffer()
            verbp("✅ Succesful connection at port "+port)
            debugp("🐛Is port " + port + " open?: " + str(connection.is_open),"🐛")
            debugp("🐛Waiting for device handshake🐛")
            connection.reset_input_buffer()
            connection.reset_output_buffer()
            for _ in range(tries):
                connection.write('a'.encode('utf-8'))
                time.sleep(1)
                response = connection.readline()
                dresponse = response.decode('utf-8')
                if dresponse == 'a\r\n':
                    verbp("✅ ArduinoDE found")
                    connection.reset_input_buffer()
                    connection.reset_output_buffer()
                    return connection
                connection.reset_output_buffer()
                connection.reset_input_buffer() 
            verbp("❌ Device not running ArduinoDE, upload .ino file to board an try again")
            return False
        except Exception as ex:
            debugp(str(ex))
            verbp("❌ Failed connection at at port " + port)
        return False
        
    def reader(self,start=None):
        pass


    def autoConnect(self,port_list=serial.tools.list_ports.comports(),word=None,rest=True):
        debugp("🐛PortList:",*port_list,"🐛")
        wordlist = []
        restlist = []
        if word is not None:
            wordlist = [name[0] for name in port_list if re.search(word, str(name))]
            debugp("🐛Wordlist:",wordlist,"🐛")
        if rest:
            restlist = [name[0] for name in port_list if (re.search(word, str(name))) is None]
            debugp("🐛Restlist:",restlist,"🐛")
        filteredlist = wordlist+restlist
        if len(filteredlist) == 0:
            verbose("❌No ports/devices found")
        debugp("🐛",filteredlist,"🐛")

        for port in filteredlist:
            conn = self.connector(port)
            if conn:
                debugp("🐛"+conn+"🐛")
                return conn
            

    def MultipleReader(self,connection, timeout=None):
        conn = connection
        verbp("Waiting...")
        try:
            buff = conn.readline()
            #print(buff)
            dbuff = buff.decode('utf-8')
            if dbuff == "begin\r\n":
                start = time.monotonic()
                print("✅ Calling reader from waiter...")
                if CAj is not False:
                    CAreader(start)
                    return
                else:
                    reader(start)
                    return

            conn.reset_input_buffer()
        except Exception as e:
            print(str(e))
            print("❌ Device disconnected")
            sys.exit()


            


logger = SerialLogger()

logger.autoConnect()
