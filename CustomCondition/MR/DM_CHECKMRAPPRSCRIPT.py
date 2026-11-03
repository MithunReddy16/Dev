from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
myLogger = MXLoggerFactory.getLogger("maximo.custom")
mrnum = mbo.getString('MRNUM')  

evalresult = False

MRLineSet = mbo.getMboSet("MRLINE")
#MRLineSet.setWhere("mrnum = '{}' AND dm_appr = 0".format(mrnum))
line = MRLineSet.moveFirst()

while line:
    myLogger.info(' line # found in MR {}.'.format(line.getString('mrlinenum')))
    if not line.getBoolean('dm_appr'):
        evalresult = True
        break    
    line = MRLineSet.moveNext()