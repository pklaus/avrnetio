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



# project-wide config file handling

## import the avrnetio class:
import avrnetio
## for debugging (set debug mark with pdb.set_trace() )
import pdb
## for config handling
from ConfigurationHandler import ConfigurationHandler

def main():
    ch = ConfigurationHandler() #use the default filename, specified in ConfigurationHandler.py
    print type(ch.host)
    netio = avrnetio.Avrnetio(ch.host)
    onewires = netio.get_1ws()
    onewires_status = dict()
    for onewire in onewires:
        onewires_status.update({onewire: netio.get_1w(onewire)})
    netio = None
    
    # print response
    print("\n--------- successfully queried the AVR-NET-IO with ethersex commands ---------")
    print("onewires: %s" % (", ".join(onewires)) )
    for which, data in onewires_status.items():
        print("onewire %s, data %s" % (which, data) )
    print("---------------------------------------------------------------- \n")
    

if __name__ == '__main__':
    main()


