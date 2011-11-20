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

# usage: example.i2cList.py

## for config handling
from ConfigurationHandler import ConfigurationHandler

class ExampleI2CList(ConfigurationHandler):
	def main(self):
		i2cs = self.getConn().get_i2cSlaves()
		
		# print response
		print("\n--------- successfully queried the AVR-NET-IO with ethersex commands ---------")
		print i2cs
		print("-"*79+"\n")


if __name__ == '__main__':

	ex = ExampleI2CList()
	ex.main()

# vim:ts=2:sw=2:number:ai
