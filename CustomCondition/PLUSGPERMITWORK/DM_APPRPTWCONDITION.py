from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from java.util import Date

evalresult = True		
 # ChecK if aLL Approve rows are Approved
revMboSet = mbo.getMboSet("$PLUSGPERWORKAPPR","PLUSGPERWORKAPPR","plusgpermitworkid = :plusgpermitworkid and APPROVED = '0'")
if( not revMboSet.isEmpty() ):
    evalresult = False