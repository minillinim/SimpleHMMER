###############################################################################
#                                                                             #
#    HMMModelParser.py                                                        #
#                                                                             #
#    Parse a Hmmer model file to get all the different parameters             #
#                                                                             #
#    Copyright (C) Connor Skennerton                                          #
#                                                                             #
###############################################################################
#                                                                             #
#            .d8888b.  d8b                        888                         #
#           d88P  Y88b Y8P                        888                         #
#           Y88b.                                 888                         # 
#            "Y888b.   888 88888b.d88b.  88888b.  888  .d88b.                 #
#               "Y88b. 888 888 "888 "88b 888 "88b 888 d8P  Y8b                #
#                 "888 888 888  888  888 888  888 888 88888888                #
#           Y88b  d88P 888 888  888  888 888 d88P 888 Y8b.   .                #    
#            "Y8888P"  888 888  888  888 88888P"  888  "Y8888                 #
#                                        888                                  #
#                                        888                                  #
#                                        888                                  #
#                                                                             #
#        888    888 888b     d888 888b     d888 8888888888 8888888b.          #
#        888    888 8888b   d8888 8888b   d8888 888        888   Y88b         #
#        888    888 88888b.d88888 88888b.d88888 888        888    888         # 
#        8888888888 888Y88888P888 888Y88888P888 8888888    888   d88P         #
#        888    888 888 Y888P 888 888 Y888P 888 888        8888888P"          #
#        888    888 888  Y8P  888 888  Y8P  888 888        888 T88b           #
#        888    888 888   "   888 888   "   888 888        888  T88b          #
#        888    888 888       888 888       888 8888888888 888   T88b         #
#                                                                             #
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Connor Skennerton"
__copyright__ = "Copyright 2012"
__credits__ = ["Connor Skennerton"]
__license__ = "GPL3"
__version__ = "0.2.3"
__maintainer__ = "Connor Skennerton"
__email__ = "mike@mikeimelfort.com"
__status__ = "Development"

###############################################################################

import re
import errno
import sys

class HmmModelError(Exception):
	pass
		

class HmmModel(object):
	"""docstring for HmmModel"""
	def __init__(self, keys):
		super(HmmModel, self).__init__()
		for key, value in keys.items():
			setattr(self, key, value)

	def __len__(self):
		if self.leng is None:
			raise HmmModelError
		return self.leng

	def __str__(self):
		ret = str()

		print self.format
		ret += "NAME\t" + self.name + "\n"
		try:
			ret += "ACC\t" + self.acc + "\n"
		except AttributeError:
			pass
		try:
			ret += "DESC\t" + self.desc + "\n"
		except AttributeError:
			pass
		ret += "LENG\t"  + str(self.leng) + "\n"
		ret += "ALPH\t" + self.alph + "\n"
		try:
			if self.rf is True:
				ret += "RF\tyes\n"
			else:
				ret += "RF\tno\n"
		except AttributeError:
			pass
		try:
			if self.cs is True:
				ret += "CS\tyes\n"
			else:
				ret += "CS\tno\n"
		except AttributeError:
			pass
		try:
			if self.map is True:
				ret += "MAP\tyes\n"
			else:
				ret += "MAP\tno\n"
		except AttributeError:
			pass
		try:
			ret += "DATE\t" + self.date + "\n"
		except AttributeError:
			pass
		try:
			ret += "COM\t" + self.com + "\n"
		except AttributeError:
			pass
		try:
			ret += "NSEQ\t" + str(self.nseq) + "\n"
		except AttributeError:
			pass
		try:
			ret += "EFFN\t" + str(self.effn) + "\n"
		except AttributeError:
			pass
		try:
			ret += "CKSUM\t" + str(self.cksum) + "\n"
		except AttributeError:
			pass
		try:
			ret += "GA\t" + str(self.ga[0]) +" "+ str(self.ga[1]) + "\n"
		except AttributeError:
			pass
		try:
			ret += "TC\t" + str(self.tc[0]) +" "+ str(self.tc[1]) + "\n"
		except AttributeError:
			pass
		try:
			ret += "NC\t" + str(self.nc[0]) +" "+ str(self.nc[1]) + "\n"
		except AttributeError:
			pass
		try:
			ret += "STATS LOCAL MSV\t" + str(self.stats_local_msv[0]) +" "+ str(self.stats_local_msv[1]) + "\n"
		except AttributeError:
			pass
		try:
			ret += "STATS LOCAL VITERBI\t" + str(self.stats_local_viterbi[0]) +" "+ str(self.stats_local_viterbi[1]) + "\n"
		except AttributeError:
			pass
		try:
			ret += "STATS LOCAL FORWARD\t"+ str(self.stats_local_forward[0]) +" "+ str(self.stats_local_forward[1]) + "\n" 
		except AttributeError:
			pass
		ret += "//\n"
		return ret

		
class HmmModelParser(object):
	"""HmmModelParser holds a file object for a HMM model and a custom iterator
	   for getting the values out"""
	def __init__(self, hmmfile):
		super(HmmModelParser, self).__init__()
		self.hmmfile = open(hmmfile)

	def parse(self):
		fields = []
		header_keys = dict()
		for current_line in self.hmmfile:
			if 0 == len(current_line.rstrip()):
				continue
			# line should be: HMMER3/b [3.0b2 | June 2009]
			if current_line.startswith("HMMER"):
				header_keys['format'] = current_line.rstrip()
			
			elif current_line.startswith("HMM"):
				# begining of the model hmm
				# parsing not implemented at the moment - iterate through till
				# the end of this model
				for current_line in self.hmmfile:
					if current_line.startswith("//"):
						yield HmmModel(header_keys)
						break

			else:
				# header sections
				fields = current_line.rstrip(' ;\n').split(None, 1)
				if 2 != len(fields):
					raise HmmModelError
				else:
					# transform some data based on some of the header tags
					if fields[0] == "LENG" or fields[0] == "NSEQ" or fields[0] == "CKSUM":
						header_keys[fields[0].lower()] = int(fields[1])
					elif fields[0] == "RF" or fields[0] == "CS" or fields[0] == "MAP":
						if fields[1].lower() == "no":
							header_keys[fields[0].lower()] = False
						else:
							header_keys[fields[0].lower()] = True
					elif fields[0] == "EFFN":
						header_keys[fields[0].lower()] = float(fields[1])
					elif fields[0] == "GA" or fields[0] == "TC" or fields[0] == "NC":
						params = fields[1].split()
						if len(params) != 2:
							raise HmmModelError
						try:
							header_keys[fields[0].lower()] = (float(params[0]), float(params[1]))
						except ValueError:
							print params[0], params[1]
							raise
					elif fields[0] == "STATS":
						params = fields[1].split()
						if params[0] != "LOCAL":
							raise HmmModelError
						if params[1] == "MSV" or params[1] == "VITERBI" or params[1] == "FORWARD":
							header_keys[(fields[0]+"_"+params[0]+"_"+params[1]).lower()] = (float(params[2]), float(params[3]))
						else:
							print("'"+params[1]+"'")
							raise HmmModelError
					else:
						header_keys[fields[0].lower()] = fields[1]
