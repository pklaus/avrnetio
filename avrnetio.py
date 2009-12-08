#
# -*- encoding: UTF8 -*-

# author: Philipp Klaus, philipp.l.klaus AT web.de


#   This file is part of avrnetio.
#
#   avrnetio is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   avrnetio is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with avrnetio.  If not, see <http:#www.gnu.org/licenses/>.



# This class represents the ECMDs (Ethersex Commands) available on the Pollin AVR-NET-IO.
# It uses raw TCP communication to send the commands.
# The class aimes at providing complete coverage of the functionality of the box
#  but not every action is supported yet.


## for the raw TCP socket connection:
from socket import *
## for md5 checksum:
#import hashlib
## for RegularExpressions:
#import re
## for debugging (set debug mark with pdb.set_trace() )
import pdb
## for math.ceil()
#import math
## for sys.exc_info()
import sys

import time
### for date.today()
#from datetime import date
from datetime import datetime

import serial

LINE_END="\n"

class avrnetio(object):

    def __init__(self, host, username="", password="", secureLogin=False):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__secureLogin = secureLogin
        self.__port = 2701
        self.__bufsize = 1024
        self.__refEP = None
        self.__serial_mode = False
    
    def __login(self):
        # connect to the server
        try:
            # create a TCP/IP socket
            self.__s = socket(AF_INET, SOCK_STREAM)
            self.__s.settimeout(6)
            self.__s.connect((self.__host, self.__port))
        except error:# some other socket error
            raise NameError("No connection to endpoint " + self.__host)
            return False
            self.disconnect()
        return True
    
    def set_serial_mode(self, device="/dev/ttyS0", baud=115200):
        self.__serial_device = device
        self.__serial_mode = True
        self.__serial_baud = baud
        
    #def setSystemTime(self,dt):
    #    self.__sendRequest("time " + time.time()dt.strftime() )
    def getSystemTime(self):
        return self.__sendRequest("time")
        
    def getSystemDate(self):
        return self.__sendRequest("date")
    
    def getSystemUptime(self):
        return self.__sendRequest("whm")
    
    def __hexStringToInt(self, hexString):
        return int(hexString, 16)
    
    def getADCs(self):
        data = self.__sendRequest("adc get").strip().split(" ")
        data = map(self.__hexStringToInt,data)
        return data
    
    # set reference electrical potential
    def setRefEP(self,referenceEP):
        self.__refEP = referenceEP
    
    def __10bitIntToVolt(self, Integer):
        return Integer/1023.0*self.__refEP
    
    def getADCsAsVolts(self):
        if self.__refEP == None:
            raise NameError("Please set reference electrical potential first.")
        return map(self.__10bitIntToVolt,self.getADCs())
    
    
    # generic method to send requests to the NET-IO 230A and checking the response
    def __sendRequest(self,request,complainIfAnswerNot250=True):
        # RS232 mode:
        if self.__serial_mode:
            try:
                self.__serial
            except:
                self.__serial = serial.Serial(self.__serial_device, self.__serial_baud, timeout=2)
                print "(re)connecting serial"
            self.__serial.write(request+LINE_END)                  # send the request
            self.__serial.readline()
            return self.__serial.readline().replace(LINE_END,"")   # read a '\n' terminated line
        # network mode
        try:
            self.__s
        except:
            self.__login()
            print "(re)connecting network"
        s = time.time()
        self.__s.send(request+LINE_END)
        s = time.time()
        data = self.__s.recv(self.__bufsize)
        #if re.search("^250 ", data) == None and complainIfAnswerNot250:
        #    raise NameError("Error while sending request: " + request + "\nresponse from NET-IO 230A is:  " + data)
        #    return None
        #else:
        return data.replace(LINE_END,"")
    
    def disconnect(self):
        try:
            if self.__serial_mode:
                self.__serial
            else:
                # close the network socket:
                self.__s.close()
        except:
            pass
            
    
    def __del__(self):
        self.disconnect()
    ###   end of class netio230a   ----------------

