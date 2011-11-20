#!/usr/bin/env python2
# -*- encoding: UTF-8 -*-

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

# superclass in order to provide global config

# project-wide config file handling
## for sys.exit(1)
import sys
## for ConfigParser.RawConfigParser()
import ConfigParser
## main module
import avrnetio

class ConfigurationHandler(object):
	"""
	config handler class (simple superclass)
	without any weird patterns
	"""

	def __init__(self, name='connection.cfg'):
		self._name = name
		self._config = ConfigParser.ConfigParser()
		try:
			if self._config.read(self._name) == []: raise Exception()
		except:
			print "error: please make sure that your configfile has the name:", self._name
			sys.exit(2)
		try:
			self._host = self._config.get('avrnetio1', 'host')
		except:
			print "error: please make sure your configuration file", self._name, "contains the section", '"avrnetio1"', 'with the entry', '"host"'
			sys.exit(2)
		try:
			self._v_ref = self._config.get('avrnetio1', 'reference_voltage')
		except:
			print "error: please make sure your configuration file", self._name, "contains the section", '"avrnetio1"', 'with the entry', '"reference_voltage"'
			sys.exit(2)
		try:
			self._netio = avrnetio.Avrnetio(self._host)
		except:
			print "could not connect to", self._host
			sys.exit(1)

	def getHost(self):
		return self._host
	def getVRef(self):
		return self._v_ref
	def getConn(self):
		return self._netio

# vim:ts=2:sw=2
