import urllib
import urllib2
import json
from datetime import datetime as dt
from function import *

# get faces info
faces=webFaces()

# parse the next user to the file faces-get
now=dt.now()
if not faces.noFaces:
  faces.send(0,{})
  data=json.loads(faces.Resp)
  for apts in data['apts']:
    startDT=dt.strptime(apts['startDay'] + ' ' + apts['startTime'], '%Y-%m-%d %H:%M:%S')
    if now < startDT:
      nextApts=apts
      break
f=open(tmpDir+'faces-get','w')
try:
  nextApts
except:
  f.write('comment : NoApts\n')
else:
  for c, v in nextApts.iteritems():
    f.write(c + ' : ' + v + '\n')
f.close()