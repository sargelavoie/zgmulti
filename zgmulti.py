# Python script to perform a number of consecutive experiments 
# specified by the user, and starting from the actual 
# experimental number (expno).
# 
# Usage: 
#   - First create all the experiments and preacquisition
#     (lock, tune, shim, rga). All experiments must be in
#     consecutive expnos
#   - Go the the first experiment of the list and execute
#     multizg2
#   - At the first pop-up window, enter the number of
#     experiments to acquire
#   - At the second pop-up window, the total duration will
#     be indicated. The next user in the Faces interface,
#     if any, will be indicated, and the user will be 
#     invited to send him an email notifying when the instrument
#     will be available
#
# Written by Serge Lavoie
#            School of Biology
#            Georgia Institute of Technology
#
#            November 12, 2016
# Version 1.0
#
import os
import getpass as gp
import re
from datetime import timedelta as td
from datetime import datetime as dt
from topspin import *
from function import *

# Get User Informations
NMRuser=gp.getuser()

# Query the User for the Number of Experiment to acquire
cd=CURDATA()
startExpno = int(cd[1])
strExp=INPUT_DIALOG("Number of Experiments", "Enter the number of experiments to perform")
try:
  noExp=int(strExp[0])
except:
  sys.exit()

# Query the User if he wants to logout at the end of the sequence
doLogout=SELECT('Logout?','At the end of the sequece, would you like to logout?',['YES','NO'])

# Calculate expt
totExpt=td(0)
for iexp in range(startExpno,startExpno+noExp-1):
  totExpt += expt2td()
  RE_IEXPNO()
totExpt+= expt2td()

# Get Faces data
os.system('python ' + scriptDir + 'faces-get.py')
faces=parceFace(tmpDir + 'faces-get')

# Check with the user if he want to notify the next user
now=dt.now()
eEX=now+totExpt
eEXstr='%s %s %d, %dh%02d' % (eEX.strftime('%A'), eEX.strftime('%B'), eEX.day, eEX.hour, eEX.minute)
if faces['comment']=='NoApts':
  messageEmail="The sequence will end on " + eEXstr
  MSG(messageEmail,"Sequence Duration")
else:
  sNA=dt.strptime(faces['startDay'] + ' ' + faces['startTime'],'%Y-%m-%d %H:%M:%S')
  sNAStr='%s %s %d, %dh%02d' % (sNA.strftime('%A'), sNA.strftime('%B'), sNA.day, sNA.hour, sNA.minute)
  msgDur="The sequence will end on " + eEXstr + ".\n"
  if sNA < eEX:
    msgAbort=msgDur + "However, " + faces['owner'] + " have a hold on the instrument on " + sNAStr + ".\n\nYour sequence will be aborted."
    MSG(msgAbort,'WARNING')
    sys.exit()
  else:
    messageEmail=msgDur + "Also, " + faces['owner'] + " is planning to use the instrument on " + sNAStr + ".\n\nWould you like to notify him when your sequence is done ?"
    confirmEmail=SELECT("Email notification",messageEmail,["YES","NO"])
    if confirmEmail == 0:
      f=open(tmpDir+'faces-send','w')
      f.write('NMRuser : ' + NMRuser + '\n')
      f.write("endExpt : " + eEXstr + '\n')
      f.close()
      os.system('python '+ scriptDir + 'faces-send.py')
 
# Acquire the Data
for iexp in range(startExpno,startExpno+noExp-1):
  XCMD('zg',WAIT_TILL_DONE)
  RE_IEXPNO()

XCMD('zg',WAIT_TILL_DONE)

# Logout
if doLogout == 0:
  SLEEP(300)
  os.system("qdbus org.kde.ksmserver /KSMServer logout 0 0 0")


