/*
Created By: Ashok
Date: 19-MAr-2024
Req: To check if the contarct still have available amount for the current work order 
to request the services service
This script is only top calcultae the Services for PS - Provision Service


*/
load("nashorn:mozilla_compat.js");
importPackage(java.util)
importPackage(Packages.psdi.server)
importPackage(Packages.psdi.mbo)
importPackage(Packages.psdi.util.logging)
//from psdi.util.logging import MXLoggerFactory

logger = MXLoggerFactory.getLogger("maximo.dm")


logger.error("***ASH***Sript DM_CHKCONTRCOST**START***")

contractCost=mbo.getMboSet("DM_STSERVPSCOST").sum("LINECOST")
logger.error("***ASH***Sript DM_CHKCONTRCOST**contractCost="+contractCost)
allwoUsedCost=mbo.getMboSet("DM_ALLSTDSERVPSCOST").sum("LINECOST")
logger.error("***ASH***Sript DM_CHKCONTRCOST**allwoUsedCost="+allwoUsedCost)
currwoCost=mbo.getMboSet("DM_STDSERVPSCOST").sum("LINECOST")
logger.error("***ASH***Sript DM_CHKCONTRCOST**currwoCost="+currwoCost)
if(currwoCost>(contractCost-allwoUsedCost))
{
    logger.error("***ASH***Sript DM_CHKCONTRCOST**evalresult= false")
    evalresult = false
}
else
{
    logger.error("***ASH***Sript DM_CHKCONTRCOST**evalresult= true")
    evalresult = true
}