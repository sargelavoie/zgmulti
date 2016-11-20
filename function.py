from topspin import *
import re
from datetime import timedelta as td
import urllib as ul
import urllib2 as ul2

#tmpDir='/tmp/'
#scriptDir='/opt/topspin3.5pl5/exp/stan/nmr/py/user/'
tmpDir='c:\\users\\sarge\\appdata\\local\\Temp\\'
scriptDir='d:\\docuserge\\code\\multizg2\\multizg2\\'

# a class to transform a string experiment time to a mapping object
class clsExpt:
  def __init__(self,raw):
    self.raw=raw
  def regex(self):
    a=re.compile(r'((?P<days>\d+?)d)? ?((?P<hours>[0-9]+?)h)? ?((?P<minutes>\d+?)min)? ?((?P<seconds>\d+?)sec)?')
    self.m=a.match(self.raw)
    return self.m.groupdict().iteritems()
  def dt(self):
    a={}
    for (n,p) in self.regex():
      if p:
        a[n]=int(p)
    return a
 # a function to get the experiment time in a timedelta object 
def expt2td():
  XCMD('expt '+tmpDir+'expt',WAIT_TILL_DONE)
  expt=clsExpt('0sec')
  try:
    f=open(tmpDir+'expt','r')
  except IOError as e:
    pass
  else:
    expt.raw=f.readline().split(' = ')[1].rstrip('\n')
    f.close()
  return td(**expt.dt())

# a function to parse file into a mapping object
def parceFace(s):
  a={}
  try:
    f=open(s,'r')
  except IOError as e:
    pass
  else:
    for l in f:
      s=l.split(' : ')
      a[s[0]]=s[1].rstrip()
    f.close()
  return a

# a function to get the credential from the file
def getCred():
  return parceFace(scriptDir+'credential.faces')

#class to interact with the Faces website
class webFaces():
  l_url='https://faces.ccrc.uga.edu/ccrcfaces/login.php'
  d_url='https://faces.ccrc.uga.edu/ccrcfaces/data3.php'
  def __init__(self):
    a=getCred()
    self.Inst=a['faceInstrument']
    self.Acc=a['faceAccount']
    self.Usr=a['faceUser']
    self.Pwd=a['facePwd']
    self.Resp=''
    instPat='value="([0-9]+)".*' + self.Inst
    pkPat="'pk' VALUE='(.+)'>"
    l_val={'account' : self.Acc, 'user' : self.Usr, 'passwd' : self.Pwd}
    l_enc=ul.urlencode(l_val)
    l_req=ul2.Request(self.l_url,l_enc)
    try: 
      l_resp=ul2.urlopen(l_req)
    except ul2.URLError, e:
      self.noFaces=True
    else:
      self.noFaces=False
      login=l_resp.read()
      m=re.search(instPat,login,re.M)
      if m is not None:
        self.InstNumber=m.group(1)
      else:
        self.InstNumber=0
      m=re.search(pkPat,login,re.M)
      if m is not None:
        self.PK=m.group(1)
      else:
        self.noFaces=True
  def send(self,mode,suffix={}):
    d_val={'user' : self.Usr, 'account' : self.Acc, 'rindex' : self.InstNumber, 'pk' : self.PK}
    d_val.update(suffix)
    d_val.update({'mode' : mode})
    d_data=ul.urlencode(d_val)
    try:
      url_resp=ul2.urlopen(self.d_url+'?'+d_data)
      self.Resp=url_resp.read()
    except ul2.URLError:
      self.noFaces=False


