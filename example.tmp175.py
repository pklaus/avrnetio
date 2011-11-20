#!/usr/bin/env python2
# -*- encoding: UTF8 -*-

# Author: 4096R/26F7CE8A Patrick Hieber <patrick.hieber AT gmx.net>


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



## import the avrnetio class:
import avrnetio
# import argument parser
import argparse
## for config handling
from ConfigurationHandler import ConfigurationHandler


def main():
	parser = argparse.ArgumentParser(description='Get the temperature from a tmp175 sensor')
	parser.add_argument('--offset', dest='offset', type=int, nargs=1,\
		metavar='N', help='int offset from base address')
	args = parser.parse_args()
	ch = ConfigurationHandler() #use the default filename, specified in ConfigurationHandler.py
	netio = avrnetio.Avrnetio(ch.host)
	tmp175_temp = netio.get_tmp175(args.offset.pop())
	netio = None
	
	# print response
	print("\n--------- successfully queried the AVR-NET-IO with ethersex commands ---------")
	print tmp175_temp
	print("------------------------------------------------------------------------------- \n")

if __name__ == '__main__':
	main()

# vim:ts=2:sw=2:number:ai
