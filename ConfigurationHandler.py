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

# modified version of this post:
# http://stackoverflow.com/questions/747793/python-borg-pattern-problem/4857198#4857198



# project-wide config file handling
## for sys.exit(1)
import sys
## for ConfigParser.RawConfigParser()
import ConfigParser
## main module
import avrnetio
"""
config handler class
using the borg pattern
@see http://stackoverflow.com/questions/747793/python-borg-pattern-problem/4857198#4857198
"""
class ConfigurationHandler(object):

	def __init__(self, name=None):
		if name is None:
			self.name = "connection.cfg"
		else:
			self.name = name
		self.config = ConfigParser.ConfigParser()
		try:
			if self.config.read(self.name) == []: raise Exception()
		except:
			print "error: please make sure that your configfile has the name:", self.name
			sys.exit(2)
		try:
			self.host = self.config.get('avrnetio1', 'host')
		except:
			print "error: please make sure your configuration file", self.name, "contains the section", '"avrnetio1"', 'with the entry', '"host"'
			sys.exit(2)
		try:
			self.v_ref = self.config.get('avrnetio1', 'reference_voltage')
		except:
			print "error: please make sure your configuration file", self.name, "contains the section", '"avrnetio1"', 'with the entry', '"reference_voltage"'
			sys.exit(2)
		try:
			self.netio = avrnetio.Avrnetio(self.host)
		except:
			print "could not connect to", self.host
			sys.exit(1)

	@classmethod
	def borg_knowledge(cls, who_is_it):
		if hasattr(cls, "b_knowledge"):
			return "%s: I already know that the borg pattern is awesome!" % who_is_it
		else:
			cls.b_knowledge = True
			return "%s: Learning about the borg pattern..." % who_is_it

	def personal_experience(self):
		if hasattr(self, "p_knowledge"):
			return "%s: I already know that!" % self.name
		else:
			self.p_knowledge = True
			return "%s: Learning something..." % self.name

if __name__ == '__main__':
	b0 = ConfigurationHandler()
	b1 = ConfigurationHandler("myConfName.conf")

	print b1.personal_experience()
	print b2.personal_experience()

	print b1.borg_knowledge(b1.name)
	print b2.borg_knowledge(b1.host)
	print b2.borg_knowledge(b1.config)

	print b2.borg_knowledge(b2.name)
	print b2.borg_knowledge(b2.host)
	print b2.borg_knowledge(b2.config)
# vim:ts=2:sw=2
