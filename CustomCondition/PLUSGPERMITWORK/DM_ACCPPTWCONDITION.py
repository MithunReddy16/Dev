from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from java.util import Date

evalresult = True		
 # ChecK if aLL Acceptors rows are accepted
revMboSet = mbo.getMboSet("$PLUSGPERWORKACCP","PLUSGPERWORKACC","plusgpermitworkid = :plusgpermitworkid and accepted = '0'")
if( not revMboSet.isEmpty() ):
    evalresult = False