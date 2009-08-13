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
##for OptionParser() (see <http://optik.sourceforge.net/>)
from optparse import OptionParser
## for time.sleep()
import time

host = "192.168.100.3"
defaultFilename = "./logged_data.txt"

def main():
    
    
    parser = OptionParser()
    parser.add_option("-f", "--file",
                    action="store", type="string", dest="filename",
                    help="write data to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=1,
                    help="don't print status messages to stdout")
    
    (options, args) = parser.parse_args()
    
    if options.filename == None:
        options.filename = defaultFilename
        print "Logging to " + defaultFilename + "as no filenmame was supplied on the command line."
    
    print "Writing to file: %s" % options.filename
    file = open(options.filename, 'w')
    file.write("Starting new logfile"+"\n")
    
    try:
        while 1:
            try:
                netio = avrnetio.avrnetio(host)
            except StandardError:
                print("could not connect")
                raise KeyboardInterrupt()
            ADCs = netio.getADCs()
            netio = None
            
            
            for ADC in ADCs :
                file.write("%s " % (ADC))            
            file.write("\n")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print "[Ctrl]-[C] pressed: closing logfile."
        file.close()


if __name__ == '__main__':
    main()


