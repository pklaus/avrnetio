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
TIMEOUT = 6

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
        self.__udp_connect = True # If you just communicate with one remote host, you can call "connect" and the socket will behave like TCP
        self.__bufsize = BUFF_SIZE
        self.__refEP = None         # has to be set during operation
        self.__serial_mode = False  # has to be set during operation
        try:
            # find out about the host:
            socktype = SOCK_STREAM if tcp_mode else SOCK_DGRAM
            #            getaddrinfo(host, port, family=0, socktype=0, proto=0)
            connection = getaddrinfo(host, port, AF_UNSPEC, socktype)
            if len(connection) < 1: raise NameError("Could not resolve hostname " + host)
            # Take the preferred connection:
            self.__connection = connection[0]
        except:
            raise NameError("There was a problem with the hostname & port you supplied: ",host,port)

    def __login(self):
        """ log in using TCP/IP"""
        try:
            # create the socket
            self.__s = socket(self.__connection[0], self.__connection[1], self.__connection[2])
            self.__s.settimeout(TIMEOUT)
            if self.__tcp_mode or self.__udp_connect: self.__s.connect(self.__connection[4])
            # self.__s.bind(('',0)) # (I think I don't need this as client!)
        except NameError: # some socket error
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

    def get_1w(self, which):
        self.__send_request("1w convert " + which)
        return self.__send_request("1w get " + which)

    def get_1ws(self):
        onewires = self.__send_request("1w list", True)
        if 'OK' in onewires: onewires.remove('OK')
        return onewires

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
    def __send_request(self,request, responses_till_OK=False):
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
            if responses_till_OK: answer = []
            while True:
                line = self.__serial.readline().replace(LINE_END,"")   # read a '\n' terminated line
                if line == 'OK': break
                if responses_till_OK:
                    answer.append(line)
                else:
                    answer = line
                    break
            return answer
        # network mode
        try:
            self.__s
        except:
            self.__login()
            print "(re)connecting network"
        if self.__tcp_mode or self.__udp_connect:
            self.__s.send(request+LINE_END)
            if responses_till_OK: answer = []
            while True:
                line = self.__s.recv(self.__bufsize).replace(LINE_END,'')
                if responses_till_OK:
                    answer.append(line)
                else:
                    answer = line
                    break
                if line == 'OK': break
        else:
            self.__s.sendto(request+LINE_END, (self.__host, self.__port) )
            addr = ('',0)
            start = time.time()
            while addr[0] != self.__host:
                if time.time()-start > TIMEOUT*2:
                    raise NameError('Did not receive a response from ethersex in time.')
                answer, addr = self.__s.recvfrom(self.__bufsize)
        if (type(answer).__name__=='string' and re.match("parse error", answer) != None) or (type(answer).__name__=='list' and "parse error" in answer):
            raise NameError("Error while sending request: " + request + "\nresponse from avrnetio is:  " + answer)
            return None
        return answer
    
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

