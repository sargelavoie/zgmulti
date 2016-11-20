from function import *

# get faces info
faces=webFaces()
get=parceFace(tmpDir+'faces-get')
email=parceFace(tmpDir+'faces-send')

# prepare the email
start=get['startDay'] + ' ' + get['startTime']
end=get['endDay'] + ' ' + get['endTime']
owner=get['owner']
NMRuser=email['NMRuser']
message=NMRuser + ' will terminate using ' + faces.Inst + " on " + email['endExpt'] + "."
faces.send(3,{'start' : start, 'end' : end, 'owner' : owner, 'message' : message, 'rn' : "1234"})

