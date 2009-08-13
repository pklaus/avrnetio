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
#   along with avrnetio.  If not, see <http://www.gnu.org/licenses/>.



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

import time
### for date.today()
#from datetime import date
from datetime import datetime

class avrnetio(object):

    def __init__(self, host, username="", password="", secureLogin=False):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__secureLogin = secureLogin
        self.__port = 2701
        self.__bufsize = 1024
        # create a TCP/IP socket
        self.__s = socket(AF_INET, SOCK_STREAM)
        self.__s.settimeout(6)
 
    def __login(self):
        # connect to the server
        try:
            self.__s.connect((self.__host, self.__port))
        except error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                raise NameError("Timeout while connecting to " + self.__host)
                #print "There was a timeout"
            else:
                raise NameError("No connection to endpoint " + self.__host)
                #print "There was some other socket error"
            return False
        return True
    
    #def setSystemTime(self,dt):
    #    self.__sendRequest("time " + time.time()dt.strftime() )
    def getSystemTime(self):
        return self.__sendRequest("time")
    
    def getSystemUptime(self):
        return self.__sendRequest("whm")
    
    def __hexStringToInt(self, hexString):
        return int(hexString, 16)
    
    def getADCs(self):
        data = self.__sendRequest("adc get").strip().split(" ")
        data = map(self.__hexStringToInt,data)
        return data
    
    
    
    # generic method to send requests to the NET-IO 230A and checking the response
    def __sendRequest(self,request,complainIfAnswerNot250=True):
        self.__login()
        self.__s.send(request+"\n")
        data = self.__s.recv(self.__bufsize)
        #if re.search("^250 ", data) == None and complainIfAnswerNot250:
        #    raise NameError("Error while sending request: " + request + "\nresponse from NET-IO 230A is:  " + data)
        #    return None
        #else:
        return data.replace("\n","")
        self.disconnect()
    
    def disconnect(self):
	    # close the socket:
        self.__s.close()
    
    def __del__(self):
        self.disconnect()
    ###   end of class netio230a   ----------------

