# ------------------------------------------------------------------
# Author :     Mithun 
# Script:      DM.MRR.GLCONDITION  (Workflow Condition Script)
# Purpose:     Returns False if ANY DM_MRRLINE shown  as '?' in GLCREDIT or GLDEBIT). 
#               Returns True if every line is clean.
# ------------------------------------------------------------------

from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
logger = MXLoggerFactory.getLogger("maximo.custom.inventory")

evalresult = True 

try:
    linemboSet=mbo.getMboSet("DM_MRRLINE")
    lineMbo=linemboSet.moveFirst()
    while lineMbo :
        if lineMbo.isNull("GLCREDITACCT") or lineMbo.isNull("GLDEBITACCT"):
            evalresult = False
        elif "?" in lineMbo.getString("GLCREDITACCT") or "?" in lineMbo.getString("GLDEBITACCT"):
            evalresult = False
        lineMbo=linemboSet.moveNext()

except Exception, e:

    logger.error("****CHECKGLQMARK - error while checking GL lines: " + str(e))
    returnValue = False