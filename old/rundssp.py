#!/usr/bin/env python

import os, sys

pdbfile="/project/home/student1/tmp/1kf5sd.pdb"
dsspfile="/project/home/student1/tmp/1kf5.dssp"
logfile="/project/home/student1/tmp/1kf5.log"

shell_cmd = ("dssp {} {} > {} ".format(pdbfile, dsspfile, logfile))

os.system(shell_cmd)
shell_check = os.system("echo $?")
print ("shell_check ", shell_check)
