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

import array


HOST = "192.168.102.3"
REFERENCE_VOLTAGE = 4.36

SECONDS_DISPLAYED = 10
RATE=28.0

SMOOTHING_FACTOR = int(RATE)


class Fifo:
    'Fastest implementation of FIFO queues http://code.activestate.com/recipes/68436/#c3'
    def __init__(self):
        self.nextin = 0
        self.nextout = 0
        self.data = {}
    def append(self, value):
        self.data[self.nextin] = value
        self.nextin += 1
    def pop(self, n=-1):
        value = self.data[self.nextout]
        del self.data[self.nextout]
        self.nextout += 1
        return value
    def get_all(self):
        lst = []
        for i in range(self.nextin-self.nextout):
            lst.append(self.data[i+self.nextout])
        return lst


def main():
    try:
        netio = avrnetio.avrnetio(HOST)
        netio.setRefEP(REFERENCE_VOLTAGE)
    except StandardError:
        print("could not connect")
        sys.exit(1)
    temperature = electronics.ntc(4700.0,25.0+273,3977.0)
    temperature.Uvcc = REFERENCE_VOLTAGE
    
    pylab.ion() # interactive mode on
 
    timefig = pylab.figure(1)
    timesub = pylab.subplot(111)
    
    seconds_displayed=SECONDS_DISPLAYED
    rate=RATE
    dt = 1/rate
    tim = Fifo()
    rawtemp = Fifo()
    for i in range(int(seconds_displayed*rate)):
        tim.append(dt*i)
    for i in range(int(seconds_displayed*rate)+SMOOTHING_FACTOR-1):
        rawtemp.append(temperature.NTCpotentialToTemp(netio.getADCsAsVolts()[4])-273)
    t = tim.get_all()
    h = ema(rawtemp.get_all(),SMOOTHING_FACTOR)
    lines = pylab.plot(t,h)
    lines2 = pylab.plot(t,rawtemp.get_all()[SMOOTHING_FACTOR-1:int(seconds_displayed*rate+SMOOTHING_FACTOR)])
    count = 0
    for i in range(1500):
        tim.append(tim.pop() + dt*rate*seconds_displayed)
        t = tim.get_all()
        rawtemp.append(temperature.NTCpotentialToTemp(netio.getADCsAsVolts()[4])-273)
        rawtemp.pop()
        h = ema(rawtemp.get_all(),SMOOTHING_FACTOR)
        lines[0].set_data(t,h)
        lines2[0].set_data(t,rawtemp.get_all()[SMOOTHING_FACTOR-1:int(seconds_displayed*rate+SMOOTHING_FACTOR)])
        timesub.set_xlim((t[0],t[-1]))
        diff = max(h)-min(h)
        begin = min(h)-0.05*diff-0.5
        end = max(h)+0.05*diff+0.5
        timesub.set_ylim(begin,end)
        pylab.draw()
        time.sleep(1/rate-0.03)
        count+=1
        if count %int(rate) == 0: print "1 second passed:", time.time()
    
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


