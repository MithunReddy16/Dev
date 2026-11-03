from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
myLogger = MXLoggerFactory.getLogger("maximo.custom")
prnum = mbo.getString('PRNUM')  

evalresult = False

PRLineSet = mbo.getMboSet("PRLINE")
#PRLineSet.setWhere("prnum = '{}' AND dm_appr = 0".format(prnum))
line = PRLineSet.moveFirst()

while line:
    myLogger.info(' line # found in pr {}.'.format(line.getString('prlinenum')))
    if not line.getBoolean('dm_appr'):
        evalresult = True
        break    
    line = PRLineSet.moveNext()