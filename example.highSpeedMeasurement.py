#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# Author: Philipp Klaus, philipp.l.klaus AT web.de

# 480 / sec   on wolfdale, local network
#  17 / sec   on laptop: uni WLAN FLUGHAFEN

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



# example how to use the avrnetio class

## import the avrnetio class:
import avrnetio
## for debugging (set debug mark with pdb.set_trace() )
import pdb
## for sys.exit(1)
import sys
## for NTC calculations
import electronics

from time import time

AVRNETIO_HOST = "192.168.102.3"
SERIAL_DEVICE='/dev/ttyS0'
SERIAL_BAUD=115200
REFERENCE_VOLTAGE=4.36
NTC_ADC=4
NTC_R0=4700.0
NTC_T0=25.0
NTC_B=3500

def main():
    try:
        netio = avrnetio.avrnetio(AVRNETIO_HOST)
        netio.set_serial_mode(SERIAL_DEVICE,SERIAL_BAUD)
        netio.setRefEP(REFERENCE_VOLTAGE)
    except StandardError:
        print("could not connect")
        sys.exit(1)
    temperature = electronics.ntc(NTC_R0,NTC_T0+273.15,NTC_B)
    temperature.Uvcc = REFERENCE_VOLTAGE

    test_duration = 10 # seconds
    counter = 0
    start = time()
    duration=[]
    while test_duration>0:
        s = time()
        netio.getADCsAsVolts()[4]
        duration.append(time()-s)
        counter+=1
        if time()-start>=1.0:
            print "rate: ",counter,"per second"
            counter=0
            test_duration-=1
            start = time()
    netio = None

    totalDuration = 0
    for dur in duration:
        totalDuration += dur
    print "average duration: ", totalDuration/len(duration)
    

if __name__ == '__main__':
    main()


