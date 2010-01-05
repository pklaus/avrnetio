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
import re
## for debugging (set debug mark with pdb.set_trace() )
import pdb
## for math.ceil()
#import math
## for sys.exc_info()
# import sys

import time
### for date.today()
#from datetime import date
from datetime import datetime

try:
    import serial
except ImportError:
    serial = None

LINE_END="\n"
BUFF_SIZE = 1024 # OK as long as ECMDs do not return anything longer than this...

class Avrnetio(object):
    """ Avrnetio is the representation of the hardware running the ethersex firmware. It can be used to send ECMDs via TCP/IP or via RS232. """
    
    def __init__(self, host='', username="", password="", secure_login=False, port = 2701, tcp_mode = True):
        """ custom constructor:
        
        host:                the network IP or hostname of the avrnetio to interface.
        username, password:  PAM data [not handled yet]
        secureLogin:         whether to use secure authentication [not handled yet]
        port:                TCP port to use when sending ECMDs to host.
        """
        self.__host = host
        self.__username = username
        self.__password = password
        self.__secureLogin = secure_login
        self.__port = port
        self.__tcp_mode = tcp_mode
        self.__bufsize = BUFF_SIZE
        self.__refEP = None         # has to be set during operation
        self.__serial_mode = False  # has to be set during operation
    
    def __login(self):
        """ log in using TCP/IP"""
        try:
            # create the socket
            if self.__tcp_mode:
                self.__s = socket(AF_INET, SOCK_STREAM)
                self.__s.settimeout(6)
                self.__s.connect((self.__host, self.__port))
            else:
                self.__s = socket(AF_INET, SOCK_DGRAM)
                self.__s.settimeout(6)
        except error: # some socket error
            raise NameError("No connection to endpoint " + self.__host)
            return False
            self.disconnect()
        return True
    
    def set_serial_mode(self, device="/dev/ttyS0", baud=115200):
        """ use this procedure after instantiation of the object to set the communication with the avrnetio to rs232 instead of network."""
        pdb.set_trace()
        if serial:
            self.__serial_mode = True
            self.__serial_device = device
            self.__serial_baud = baud
        else:
            raise NameError("Trying to set_serial_mode(), but python module pySerial is not installed.")
    def get_system_time(self):
        """ask for the system time of the avrnetio"""
        return self.__send_request("time")
        
    def get_system_date(self):
        """ask for the system date of the avrnetio"""
        return self.__send_request("date")
    
    def get_system_uptime(self):
        """ask for the system uptime of the avrnetio"""
        return self.__send_request("whm")
    
    def __hex_string_to_int(self, hex_string):
        return int(hex_string, 16)
    
    def get_adcs(self):
        data = self.__send_request("adc get").strip().split(" ")
        data = map(self.__hex_string_to_int,data)
        return data
    
    # set reference electrical potential
    def set_ref_ep(self,reference_ep):
        self.__ref_ep = reference_ep
    
    def __10bit_int_to_volt(self, integer):
        return integer/1023.0*self.__ref_ep
    
    def get_adcs_as_volts(self):
        if self.__ref_ep == None:
            raise NameError("Please set reference electrical potential first.")
        return map(self.__10bit_int_to_volt,self.get_adcs())
    
    
    # generic method to send requests to the NET-IO 230A and checking the response
    def __send_request(self,request):
        # RS232 mode:
        if self.__serial_mode:
            try:
                self.__serial
            except:
                self.__serial = serial.Serial(self.__serial_device, self.__serial_baud, timeout=2)
                print "(re)connecting serial"
            try:
                self.__serial.write(request+LINE_END)                  # send the request
            except serial.serialutil.SerialException:
                raise NameError("Connection to ethersex device failed. Wrong RS232 port given? Device not powered?")
            self.__serial.readline()
            return self.__serial.readline().replace(LINE_END,"")   # read a '\n' terminated line
        # network mode
        try:
            self.__s
        except:
            self.__login()
            print "(re)connecting network"
        if self.__tcp_mode:
            self.__s.send(request+LINE_END)
            data = self.__s.recv(self.__bufsize)
        else:
            self.__s.sendto(request+LINE_END, (self.__host, self.__port) )
            data = self.__s.recvfrom(self.__bufsize, (self.__host, self.__port) )
        if re.match("parse error", data) != None:
            raise NameError("Error while sending request: " + request + "\nresponse from avrnetio is:  " + data)
            return None
        else:
            return data.replace(LINE_END,"")
    
    def disconnect(self):
        """disconnect the class from the avrnetio. That means closing the serial port and/or closing the TCP connection."""
        try:
            if self.__serial_mode:
                self.__serial
            # close the network socket:
            self.__s.close()
        except:
            pass
            
    
    def __del__(self):
        self.disconnect()
    ###   end of class netio230a   ----------------

