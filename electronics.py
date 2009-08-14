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



## for debugging (set debug mark with pdb.set_trace() )
#import pdb
## for math.log()
import math




# NTCs are temperature dependent resistors.
class ntc(object):
    #
    #     U_VCC
    #     ---+
    #        #
    #        #  serial constant resistor R   (10k)
    #        #
    #        |---------> U_NTC 
    #        #
    #        #   NTC R_NTC  (4.7k)
    #        #
    #     ---+
    #     GND
    #
    def __init__(self, RN0=4700.0, TN0 = 25.0+273.0, B0 = 3977.0):
        self.RN0 = RN0
        self.TN0 = TN0
        self.B0 = B0
        # R = 10000 Ohm
        self.serialResistance=10000.0
        # U_VCC = 5V
        self.Uvcc = 5.0

    # we want to calculate the temperature T at a measured resistance R of the NTC
    # http://tuxgraphics.org/common/images2/article07051/Ntcformula.gif
    # takes the value of an electrical resistance [Ohm] and gives back a temperature [K]
    def NTCresitanceToTemp(self, resistance):
        temperature = 1/(math.log(resistance/self.RN0)/self.B0+1/self.TN0)
        return temperature
    
    
    # NTC voltage -> NTC resistance   for connected voltage dividers
    def calculateResistanceOfNTC(self, Untc):
        # R_NTC   =   R / ( U_VCC / U_NTC - 1)
        if (Untc <= 0):
            # never divide by zero:
            Untc=0.001;
        ohm= self.serialResistance / (( self.Uvcc / Untc ) - 1 );
        return ohm
    
    
    def NTCpotentialToTemp(self, potential):
        return self.NTCresitanceToTemp(self.calculateResistanceOfNTC(potential))


