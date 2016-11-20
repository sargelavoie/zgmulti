import sys
#tmpDir='/tmp/'
tmpDir='c:\\users\\sarge\\appdata\\local\\Temp\\'

def CURDATA():
  a={}
  a[1]='1'
  return a

def INPUT_DIALOG(trash,question):
  a={}
  sys.stdout.write(question+': ')
  a[0]=raw_input()
  return a

def SELECT(trash,question,arrayAnwser):
  prompt=question+': '
  for val in arrayAnwser:
    prompt=prompt + val.lower() + ', '
  prompt=prompt.rstrip(', ')+'? '
  sys.stdout.write(prompt+': ')
  a=raw_input().lower()
  i=0
  for val in arrayAnwser:
    if a==val.lower():
      return i
    i += 1
  return i
            
def XCMD(trash,arg): 
  f=open(tmpDir+'expt','w')
  f.write('experiment time = 1h 3min\n')
  f.close()
    

class WAIT_TILL_DONE: pass

def RE_IEXPNO(): pass

def MSG(message,trash):
  print message

def SLEEP(i):pass