#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRPRECTRANSinterface.USEREXIT.IN.BEFORE
# Description: Set default values for inbound GR data (XML-based)
#
# Enterprise Service: GRPRECTRANSinterface
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Amir Anwar.
#-----------------------------------------------------------------------------------------

'''
* Manage trans type
* Manage Status ( COMP, winsp , WASSET)
* Manage External ref iD ( done)
* Manage Inspection on PO ( done)
* Change Relase num ( done)
* Changes to UI for adding External Ref - shipment etc..
'''

'''
skipped transaction might need to be created in Maximo for tracking purpise of parent - child
Trans TYpes
1.	RETURN TO VENDOR
2.	DELIVER
3.	TRANSFER ( NA within PO receipting)
4.	REJECT ( to maximo this is similar to return to vendor so it will be skipped)
5.	RETURN TO RECEIVING (  This could be void in case delievered)
6.	UNORDERED (Transaction of un existing PO is not permitted in Maximo hence skipped)
7.	ACCEPT ( to maximo this is similar to deliver so it will be skipped)
8.	CORRECT
9.	RECEIVE ( in maximo if item is not require inspection then Receive  delivery )

'''

from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from java.io import StringWriter
from javax.xml.transform import TransformerFactory
from javax.xml.transform.dom import DOMSource
from javax.xml.transform.stream import StreamResult
from org.jdom2.output import XMLOutputter
from psdi.server import MXServer
from psdi.mbo import SqlFormat
from psdi.util import MXApplicationException

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("============= SYNC.GRPRECTRANSinterface.USEREXIT.IN.BEFORE: START =============")

userInfo = MXServer.getMXServer().getSystemUserInfo()

#-----------------------------------------------------------------------------------------
# get the PO 
#
# @param Mbo (poNum) The PO Number
# @param Mbo (siteId) The Organization
#-----------------------------------------------------------------------------------------
def getPO(poNum,POHeaderID, siteId):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - PO: " + str(poNum))

    #whereclause = "ponum = :1 and siteid = :2" 
    #whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where ponum = :1 and siteid = :2 "
    
    whereclause = "(PONUM=:1 OR DM_GRPHEADERID = :2) and siteid = :3" 
    whereclause = whereclause + " and revisionnum = (select max(revisionnum) from po where (PONUM=:1 OR DM_GRPHEADERID = :2) and siteid = :3 "
    
    whereclause = whereclause + " and status not in (select value from synonymdomain where domainid = 'POSTATUS' and maxvalue in ('CAN', 'REVISE', 'CLOSE')))"
    
    sqlFormat = SqlFormat(userInfo, whereclause)    
    sqlFormat.setObject(1, "PO", "ponum", poNum)
    sqlFormat.setObject(2, "PO", "DM_GRPHEADERID", str(POHeaderID))
    sqlFormat.setObject(3, "PO", "siteid", siteId)

    
    pos = MXServer.getMXServer().getMboSet("PO", userInfo)
    pos.setWhere(sqlFormat.format())
    pos.reset()
    
    #logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-getPO\n" + " - whereclause: " + pos.getCompleteWhere())
    
    return pos.getMbo(0)

def isDMPO(poNum, POHeaderID,siteid):

    if getPO(poNum, POHeaderID,siteid):
        return True
        
    prLineSet = MXServer.getMXServer().getMboSet("prLine", userInfo)
    prLineSet.setWhere(sqlFormat.format())
    prLineSet.reset()

    sqlFormat = SqlFormat(userInfo, "(DM_GRPPONUM = :1 or DM_GRPPOHEADERID=:2) AND SITEID = :3")
    sqlFormat.setObject(1, "prLine", "DM_GRPPONUM",  poNum)
    sqlFormat.setObject(2, "prLine", "DM_GRPPOHEADERID",  str(POHeaderID))
    sqlFormat.setObject(3, "prLine", "siteid",  siteid)
    
    prLineSet.setWhere(sqlFormat.format())
    prLineSet.reset()
    if prLineSet.moveFirst() :
        logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO eNDED - po fOUND\n")
        return True
    
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-isDMPO eNDED - PO NOT FOUND\n")
    
    return  False




    





def checkSkiprules(erData):
    logger.debug("\n\r!!! SYNC.POINTERFACE.USEREXIT.IN.BEFORE-SKIP RULES START\n")
    ponum = erData.getCurrentDataAsString("PONUM")
    

    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
        ponum =ponum + "-" + str(ReleaseNum)    

    POHeaderID = erData.getCurrentDataAsInt("DM_POHEADERID")

    if not isDMPO(ponum,POHeaderID,"DM"):
        logger.debug("\n\r!!! PO is not DM Inventory PO , skipping ....\n")
        service.raiseSkipTransaction()

    


def setBusinessValues(erData):
    if erData.isInCurrentData("DM_GRPRELEASENUM") and not erData.isCurrentDataNull("DM_GRPRELEASENUM"):
        ReleaseNum =  erData.getCurrentDataAsInt("DM_GRPRELEASENUM")
        ponum =erData.getCurrentDataAsString("PONUM") + "-" + str(ReleaseNum)
        erData.setCurrentData("PONUM",  ponum)
    
        
    

def logErData(erData):
    try:
        logger.debug("===== Pretty Printed erData XML1 =====")
        logger.debug(XMLOutputter().outputString(erData.getData()))
        logger.debug("===== Pretty Printed erData XML2 =====")
    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))

#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
erData.setAction("AddChange")
logger.debug("** Parent action **"+str(erData.getAction()))
checkSkiprules(erData)
setBusinessValues(erData)

#logErData(erData)
logger.debug("============= SYNC.GRPRECTRANSinterface.USEREXIT.IN.BEFORE: END =============")