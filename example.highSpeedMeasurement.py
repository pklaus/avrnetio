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

from datetime import datetime

host = "192.168.102.3"
refVoltage = 4.36

def main():
    try:
        netio = avrnetio.avrnetio(host)
        netio.setRefEP(refVoltage)
    except StandardError:
        print("could not connect")
        sys.exit(1)
    temperature = electronics.ntc(4700.0,25.0+273,9000.0)
    temperature.Uvcc = refVoltage
    
    test_duration = 10 # seconds
    counter = 0
    start = datetime.now()
    while test_duration>0:
        netio.getADCsAsVolts()[4]
        counter+=1
        if (datetime.now()-start).seconds>=1.0:
            print "rate: ",counter,"per second"
            counter=0
            start = datetime.now()
            test_duration-=1
    netio = None
    

if __name__ == '__main__':
    main()


