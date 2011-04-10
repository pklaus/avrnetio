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
## for ConfigParser.RawConfigParser()
import ConfigParser

CONFIGURATION_FILE = "connection.cfg"

def main():
    config = ConfigParser.ConfigParser()
    try:
        if config.read(CONFIGURATION_FILE) == []: raise Exception()
    except:
        print "error: please make sure you adopted the configuration file:", CONFIGURATION_FILE
        sys.exit(2)
    try:
        host = config.get('avrnetio1', 'host')
    except:
        print "error: please make sure your configuration file", CONFIGURATION_FILE, "contains the section", '"avrnetio1"', 'with the entry', '"host"'
        sys.exit(2)
    try:
        netio = avrnetio.Avrnetio(host)
    except StandardError:
        print("could not connect")
        sys.exit(1)
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


