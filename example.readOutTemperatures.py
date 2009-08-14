#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# Author: Philipp Klaus, philipp.l.klaus AT web.de


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


host = "192.168.100.3"
refVoltage = 4.36

def main():
    try:
        netio = avrnetio.avrnetio(host)
        netio.setRefEP(refVoltage)
    except StandardError:
        print("could not connect")
        sys.exit(1)
    NTCvoltage = netio.getADCsAsVolts()[4]
    
    netio = None
    
    
    temperature = electronics.ntc()
    temperature.Uvcc = refVoltage
    
    # print response
    print "\n--------- successfully queried the AVR-NET-IO with ethersex commands ---------"
    print "NTC voltage: %.3f V" % (NTCvoltage)
    print "temperature: %.1f °C" % (temperature.NTCpotentialToTemp(NTCvoltage)-273)
    print "---------------------------------------------------------------- \n"
    

if __name__ == '__main__':
    main()


