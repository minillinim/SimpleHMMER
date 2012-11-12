.                                                                             
.            .d8888b.  d8b                        888                         
.           d88P  Y88b Y8P                        888                         
.           Y88b.                                 888                          
.            "Y888b.   888 88888b.d88b.  88888b.  888  .d88b.                 
.               "Y88b. 888 888 "888 "88b 888 "88b 888 d8P  Y8b                
.                 "888 888 888  888  888 888  888 888 88888888                
.           Y88b  d88P 888 888  888  888 888 d88P 888 Y8b.                        
.            "Y8888P"  888 888  888  888 88888P"  888  "Y8888                 
.                                        888                                  
.                                        888                                  
.                                        888                                  
.                                                                             
.        888    888 888b     d888 888b     d888 8888888888 8888888b.          
.        888    888 8888b   d8888 8888b   d8888 888        888   Y88b         
.        888    888 88888b.d88888 88888b.d88888 888        888    888          
.        8888888888 888Y88888P888 888Y88888P888 8888888    888   d88P         
.        888    888 888 Y888P 888 888 Y888P 888 888        8888888P"          
.        888    888 888  Y8P  888 888  Y8P  888 888        888 T88b           
.        888    888 888   "   888 888   "   888 888        888  T88b          
.        888    888 888       888 888       888 8888888888 888   T88b         
.

Overview
=========

SimpleHMMER is just that, a super simple way to run HMMER3 and parse the
output. No biopython, no frills, just parse

Installation
=========

Should be as simple as

    pip install SimpleHMMER

Using MetaChecka2000
=========

Running hmmer

    from simplehmmer.simplehmmer import HMMERRunner
    HR=HMMERRunner(prefix='frode')
    HR.search('/path/to/some.hmm', '/path/to/some.fasta', '/path/to/save/to/')
    
Parsing results

    from simplehmmer.simplehmmer import HMMERParser
    with open('/path/to/save/to/frode_out.txt', 'r') as fh:
         HP = HMMERParser(fh)
         while True:
             result = HP.next()
             if result:
                 print result
             else:
                 break

Super simple!

Licence and referencing
=========

Project home page, info on the source tree, documentation, issues and how to contribute, see http://github.com/minillinim/SimpleHMMER

This software is currently unpublished. Please contact me at m_dot_imelfort_at_uq_dot_edu_dot_au for more information about referencing this software.

Copyright © 2012 Michael Imelfort. See LICENSE.txt for further details.
