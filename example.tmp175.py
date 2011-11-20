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

# usage: example.tmp175.py [-h] [--offset OFFSET]

# import argument parser
import argparse
## for config handling
from ConfigurationHandler import ConfigurationHandler

class ExampleTMP175(ConfigurationHandler):
	def main(self, offset=0):
		tmp175_temp = self.getConn().get_tmp175(offset)
		
		# print response
		print("\n--------- successfully queried the AVR-NET-IO with ethersex commands ---------")
		print tmp175_temp
		print("-"*79+"\n")


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Get the temperature from a tmp175 sensor')
	parser.add_argument('--offset', default=0, type=int, help='int offset from base address 0x48', nargs=1, dest='offset')
	args = parser.parse_args()

	ex = ExampleTMP175()
	ex.main(args.offset)

# vim:ts=2:sw=2:number:ai
