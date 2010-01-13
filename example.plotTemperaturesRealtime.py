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

import time
import pylab # needs matplotlib:  sudo aptitude install python-matplotlib

## import the avrnetio class:
import avrnetio
## for debugging (set debug mark with pdb.set_trace() )
import pdb
## for sys.exit(1)
import sys
## for NTC calculations
import electronics
## for ConfigParser.RawConfigParser()
import ConfigParser

import array # for ema() ( uses array.array() )

CONFIGURATION_FILE = "connection.cfg"

ADC_NTC = 4

SECONDS_DISPLAYED = 5
RATE=40.0

SMOOTHING_FACTOR = int(RATE*4)


def main():    
    config = ConfigParser.RawConfigParser()
    config.read(CONFIGURATION_FILE)
    HOST = config.get('avrnetio1', 'host')
    REFERENCE_VOLTAGE = config.getfloat('avrnetio1', 'reference_voltage')
    
    try:
        netio = avrnetio.Avrnetio(HOST)
        netio.set_ref_ep(REFERENCE_VOLTAGE)
    except StandardError:
        print("could not connect")
        sys.exit(1)
    temperature = electronics.Ntc(4700.0,25.0+273,3548.0)
    temperature.Uvcc = REFERENCE_VOLTAGE
    
    pylab.ion() # interactive mode on
 
    timefig = pylab.figure(1)
    timesub = pylab.subplot(111)
    
    pylab.grid()
    
    seconds_displayed=SECONDS_DISPLAYED
    rate=RATE
    dt = 1/rate
    tim = []
    rawtemp = []
    start = time.time()
    for i in range(int(seconds_displayed*rate)+SMOOTHING_FACTOR-1):
        rawtemp.append(temperature.ntc_potential_to_temp(netio.get_adcs_as_volts()[ADC_NTC])-273)
        if i < int(seconds_displayed*rate):
            tim.append(time.time()-start)
        #time.sleep(0.001)
    smoothtemp = ema(rawtemp,SMOOTHING_FACTOR)
    lines = pylab.plot(tim,smoothtemp)
    lines2 = pylab.plot(tim,rawtemp[SMOOTHING_FACTOR-1:int(seconds_displayed*rate+SMOOTHING_FACTOR)])
    count = 0
    cycle_start = time.time()
    for i in range(1500):
        tim.append(time.time()-start)
        tim.pop(0)
        rawtemp.append(temperature.ntc_potential_to_temp(netio.get_adcs_as_volts()[ADC_NTC])-273)
        rawtemp.pop(0)
        smoothtemp = ema(rawtemp,SMOOTHING_FACTOR)
        lines[0].set_data(tim,smoothtemp)
        lines2[0].set_data(tim,rawtemp[SMOOTHING_FACTOR-1:int(seconds_displayed*rate+SMOOTHING_FACTOR)])
        timesub.set_xlim((float("%.3f" % tim[0]),float("%.3f" % tim[-1])))
        diff = max(smoothtemp)-min(smoothtemp)
        begin = min(smoothtemp)-0.05*diff-0.13
        end = max(smoothtemp)+0.05*diff+0.13
        timesub.set_ylim(begin,end)
        #if count==0: print "", time.time()-start
        pylab.draw()  # takes up to 0.10 seconds on wolfdale workstation
        #if count==0: print "pylab.draw", time.time()-start
        sleep=1/rate-0.04
        time.sleep(sleep if sleep>0 else 0)
        count+=1
        if time.time()-cycle_start>=1.0:
            print "rate set: ", rate, "rate achieved: ", count/1.0
            cycle_start=time.time()
            count=0
    
    netio = None


def ema(s, n):
    """         exponential moving average
    
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    
    http://osdir.com/ml/python.matplotlib.general/2005-04/msg00044.html
    """
    s = array.array('d',s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
       tmp = ( (i - ema[j]) * multiplier) + ema[j]
       j = j + 1
       ema.append(tmp)

    return ema



if __name__ == '__main__':
    main()


