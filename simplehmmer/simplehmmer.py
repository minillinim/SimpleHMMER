###############################################################################
#                                                                             #
#    simpleHMMER.py                                                           #
#                                                                             #
#    Run HMMER and provide an API for Parsing output                          #
#                                                                             #
#    Copyright (C) Michael Imelfort                                           #
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

__author__ = "Michael Imelfort"
__copyright__ = "Copyright 2012"
__credits__ = ["Michael Imelfort"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Michael Imelfort"
__email__ = "mike@mikeimelfort.com"
__status__ = "Development"

###############################################################################

from re import split as re_split
from os import system, makedirs
from os.path import join as osp_join
import errno
import sys

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class FormatError(BaseException): pass
class HMMERError(BaseException): pass

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class HMMERRunner():
    """Wrapper for running HMMER3"""
    def __init__(self, prefix=''):
        # make sure HMMER is installed! 
        self.checkForHMMER()
        # make the output file names
        if prefix == '':
            self.txtOut = 'hmmer_out.txt'
            self.hmmOut = 'hmmer_out.hmmer3'
        else:
            self.txtOut = '%s_out.txt' % prefix
            self.hmmOut = '%s_out.hmmer3' % prefix
    
    def checkForHMMER(self):
        """Check to see if HMMER is on the system before we try fancy things
        
        We assume that a successful hmmsearch -h returns 0 and anything
        else returns something non-zero
        """
        # redirect stdout so we don't get mess!
        try:
            exit_status = system('hmmsearch -h > /dev/null')
        except:
          print "Unexpected error!", sys.exc_info()[0]
          raise
      
        if exit_status != 0:
            raise HMMERError("Error attempting to run hmmsearch, is it in your path?")
    
    def search(self, db, query, outputDir):
        """Do the search"""
        # make the output dir and files
        self.makeSurePathExists(outputDir)
        txt_file = osp_join(outputDir, self.txtOut)
        hmm_file = osp_join(outputDir, self.hmmOut)
        
        # run hmmer!
        system('hmmsearch --tblout %s %s %s > %s' % (txt_file, db, query, hmm_file))
        
    def makeSurePathExists(self, path):
        try:
            makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    
###############################################################################
###############################################################################
###############################################################################
###############################################################################

class HMMERParser():
    """Parses tabular output"""
    def __init__(self, fileHandle):
        """Give this guy an open file!"""
        self.handle = fileHandle
    
    def next(self):
        """Get the next result in the file"""
        while 1:
            hit = self.readHits()
            if hit == {}:
                return None
            else:
                return hit

    def readHits(self):
        """Look for the next hit, package it up and return it"""
        while (1):
            line = self.handle.readline().rstrip()
            try:
                if line[0] != '#' and len(line) != 0:
                    """
We expect line to look like:
NODE_110054_length_1926_cov_24.692627_41_3 -          Ribosomal_S9         PF00380.14   5.9e-48  158.7   0.0   6.7e-48  158.5   0.0   1.0   1   0   0   1   1   1   1 # 1370 # 1756 # 1 # ID=41_3;partial=00;start_type=ATG;rbs_motif=None;rbs_spacer=None
                    """
                    dMatch = re_split( r'\s+', line.rstrip() )
                    if len(dMatch) < 19:
                        raise FormatError( "Something is wrong with this line:\n%s" % (line) )
                    refined_match = dMatch[0:18] + [" ".join([str(i) for i in dMatch[18:]])]
                    return HmmerHit(refined_match)
            except IndexError:
                return {}

class HmmerHit():
    """Encapsulate a hmmer hit"""
    def __init__(self, values):
        """Load em' in"""
        if len(values) == 19:
            self.target_name = values[0]
            self.target_accession = values[1]
            self.query_name = values[2]
            self.query_accession = values[3]
            self.full_e_value = float(values[4])
            self.full_score = float(values[5])
            self.full_bias = float(values[6])
            self.best_e_value = float(values[7])
            self.best_score = float(values[8])
            self.best_bias = float(values[9])
            self.exp = float(values[10])
            self.reg = int(values[11])
            self.clu = int(values[12])
            self.ov = int(values[13])
            self.env = int(values[14])
            self.dom = int(values[15])
            self.rep = int(values[16])
            self.inc = int(values[17])
            self.target_description = values[18]    
    
    def __str__(self):
        """when we need to print"""
        return "\t".join([self.target_name,
                          self.target_accession,
                          self.query_name,
                          self.query_accession,
                          str(self.full_e_value),
                          str(self.full_score),
                          str(self.full_bias),
                          str(self.best_e_value),
                          str(self.best_score),
                          str(self.best_bias),
                          str(self.exp),
                          str(self.reg),
                          str(self.clu),
                          str(self.ov),
                          str(self.env),
                          str(self.dom),
                          str(self.rep),
                          str(self.inc),
                          self.target_description
                          ]
                         )

###############################################################################
###############################################################################
###############################################################################
###############################################################################
        