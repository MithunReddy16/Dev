from psdi.server import MXServer
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from java.util import Date

evalresult = True		
 # ChecK if aLL Reviewer rows are reviewed
revMboSet = mbo.getMboSet("$PLUSGPERWORKREV","PLUSGPERWORKREV","plusgpermitworkid = :plusgpermitworkid and REVIEWED = '0'")
if( not revMboSet.isEmpty() ):
    evalresult = False