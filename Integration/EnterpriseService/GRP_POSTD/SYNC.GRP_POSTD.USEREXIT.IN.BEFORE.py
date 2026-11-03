#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRP_POSTD.USEREXIT.IN.BEFORE
# Description: Set default values and normalize status for inbound PO data (XML-based)
#
# Enterprise Service: GRP_POSTD
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 21-Mar-2025
#-----------------------------------------------------------------------------------------
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
from java.text import SimpleDateFormat

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("=============Mithun SYNC.GRP_POSTD.USEREXIT.IN.BEFORE: START =============")


def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")
    #if erData.isCurrentDataNull("ITEMNUM"):
        #raise MXApplicationException("integration", "missingitemnum")



#-----------------------------------------------------------------------------------------
# Set default values for required fields if missing in the incoming XML data
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")

    if erData.isCurrentDataNull("SITEID"):
        erData.setCurrentData("SITEID", "DM")
        logger.debug("SITEID defaulted to DM")


    # setting potype as STD in all cases 
    erData.setCurrentData("POTYPE", "STD")
    

#-----------------------------------------------------------------------------------------
# Converting the incoming status values to Maximo internal statuses
#-----------------------------------------------------------------------------------------
def convertStatus(erData):
    if erData.isInCurrentData("STATUS") and not erData.isCurrentDataNull("STATUS"):
        status = erData.getCurrentDataAsString("STATUS").strip()
        
        if status == "REQUIRES REAPPROVAL":
            erData.setCurrentData("STATUS", "RETURNED")
            logger.debug("STATUS changed to WAPPR")
        elif status == "APPROVED":
            erData.setCurrentData("STATUS", "APPR")
            logger.debug("STATUS changed to APPR")
        elif status == "IN PROCESS":
            erData.setCurrentData("STATUS", "INPRG")
            logger.debug("STATUS changed to INPRG")
        elif status == "REJECTED":
            erData.setCurrentData("STATUS", "CAN")
            logger.debug("STATUS changed to CAN")
        elif status == "INCOMPLETE":
            erData.setCurrentData("STATUS", "WAPPR")
            logger.debug("STATUS changed to CAN")
        
    if erData.isInCurrentData("CLOSEDCODE") and not erData.isCurrentDataNull("CLOSEDCODE"):
        closecode = erData.getCurrentDataAsString("CLOSEDCODE").strip()
        if closecode =="FINALLY CLOSED" :
            erData.setCurrentData("STATUS", "CLOSE")

def checkingRevision(erData):
    try:
        incomingRev = erData.getCurrentDataAsInt("REVISIONNUM")
        ponum = erData.getCurrentDataAsString("PONUM")
        siteid = erData.getCurrentDataAsString("SITEID")

        logger.debug("****Incoming REVISIONNUM: " + str(incomingRev))
        logger.debug("****ponum : " + str(ponum))
        logger.debug("****siteid : " + str(siteid))
        poSet = MXServer.getMXServer().getMboSet("PO", MXServer.getMXServer().getSystemUserInfo())
        where = SqlFormat(poSet.getUserInfo(), "PONUM = :1 AND SITEID = :2")
        where.setObject(1, "PO", "PONUM", ponum)
        where.setObject(2, "PO", "SITEID", siteid)
        poSet.setWhere(where.format())
        logger.debug("** po getwhere is  " +poSet.getWhere()  )
        poSet.setOrderBy("REVISIONNUM desc")
        logger.debug("Incoming REVISIONNUM: " + str(incomingRev))
        if not poSet.isEmpty():
            po = poSet.moveFirst()
            maxRev = po.getInt("REVISIONNUM")
            logger.debug("Existing Max REVISIONNUM: " + str(maxRev))

            if incomingRev > maxRev:
                erData.setCurrentData("REVCOMMENTS", "PO revision "+str(incomingRev)+" revised from GRP.")
                #erData.setCurrentData("STATUS","PNDREV")
                logger.debug("REVCOMMENTS set for new revision")

        poSet.close()
    except Exception as e:
        logger.error("Error in checkAndSetRevisionComments: " + str(e))

def setBusinessValues(erData):
    logger.debug("**** in business def****")
    
 
        
        
        
# setting default error at the end            
def logErData(erData):
    try: 
        logger.debug("===== Pretty Printed erData before =====")
        logger.debug(XMLOutputter().outputString(erData.getData()))
        logger.debug("===== Pretty Printed erData After =====")
    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))



#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
logger.debug("** Parent Data **"+erData.getCurrentAction())

mandatoryChecks(erData)
setDefaultValues(erData)
convertStatus(erData)
checkingRevision(erData)
setBusinessValues(erData)

# manipulating childern Data 
ponum=erData.getCurrentDataAsString("PONUM")
revnum=erData.getCurrentDataAsInt("REVISIONNUM")
logger.debug("*****revnumafter **"+str(revnum))
lastUpdateDate=erData.getCurrentDataAsDate("DM_LASTUPDATEDATE")
formatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
formattedDate = formatter.format(lastUpdateDate)
logger.debug("*****revnumafter1 **"+str(formattedDate))
poLineList=erData.getChildrenData("POLINE")
noOfPOLines=poLineList.size()
if (poLineList is not None and noOfPOLines > 0):
    for i in range(noOfPOLines):        
        erData.setAsCurrent(poLineList,i)        
        cancelflag=erData.getCurrentDataAsInt("CANCELFLAG")
        if cancelflag ==1:
            erData.setCurrentAction("Delete")
         # linetype  logic    
        linetype=erData.getCurrentDataAsString("LINETYPE")
        itemnum=erData.getCurrentDataAsString("ITEMNUM") 
        polinenum=erData.getCurrentDataAsInt("POLINENUM")
        logger.debug("***linetype="+str(linetype))
        logger.debug("***itemnum="+str(itemnum))
        if linetype == "Quantity" and (itemnum is not None and itemnum != "" ) :
            erData.setCurrentData("LINETYPE", "ITEM")
        elif linetype == "Quantity" and (itemnum is None or itemnum==""):
            erData.setCurrentData("LINETYPE", "MATERIAL")
            erData.setCurrentDataNull("STORELOC")
        else:
            erData.setCurrentData("LINETYPE", "SERVICE")
            erData.setCurrentDataNull("STORELOC")
        
        ## linking PO to PR
        logger.debug("**PO1 **")
        prLineSet = MXServer.getMXServer().getMboSet("PRLINE", MXServer.getMXServer().getSystemUserInfo())
        logger.debug("**PO2 **")
        where = SqlFormat(prLineSet.getUserInfo(), "DM_GRPPONUM = :1 AND SITEID = :2")
        logger.debug("**PO3 **")
        where.setObject(1, "PO", "PONUM", ponum)
        where.setObject(2, "PO", "SITEID", "DM")
        logger.debug("**PO4 **")
        prLineSet.setWhere(where.format())
        logger.debug("**PO5 **"+prLineSet.getWhere())
        if not prLineSet.isEmpty():
            prLine = prLineSet.moveFirst()
            prnum = prLine.getString("PRNUM")
            prlinenum = prLine.getString("PRLINENUM")
            erData.setCurrentData("PRNUM",prnum )
            erData.setCurrentData("PRLINENUM", prlinenum)
            logger.debug("**PO6 **")
        else :
            print("**Skiping the transcation there is no GRPPONUM in POLines **")
            logger.debug("**Skiping the transcation there is no GRPPONUM in POLines **")
            service.raiseSkipTransaction()
        
        """
        ## skiping the ponum and poline if lastUpdateDate is already present which means pastDate 
        logger.debug("**PO7 **")
        poSet = MXServer.getMXServer().getMboSet("PO", MXServer.getMXServer().getSystemUserInfo())
        logger.debug("**PO8 **")
        where = SqlFormat(prLineSet.getUserInfo(), "PONUM = :1 AND REVISIONNUM =:2 AND DM_LASTUPDATEDATE>:3 AND EXISTS (SELECT 1 FROM POLINE WHERE POLINE.PONUM=PO.PONUM AND POLINE.REVISIONNUM=PO.REVISIONNUM AND POLINE.POLINENUM=:4)")
        logger.debug("**PO9 **")
        where.setObject(1, "PO", "PONUM", ponum)
        where.setObject(2, "PO", "REVISIONNUM", str(revnum))
        where.setObject(3, "PO", "DM_LASTUPDATEDATE", str(formattedDate))
        where.setObject(4, "POLINE", "POLINENUM", str(polinenum))
        logger.debug("**P1O **")
        poSet.setWhere(where.format())
        logger.debug("**P11 **"+poSet.getWhere())
        if not poSet.isEmpty():
            logger.debug("**Skiping the transcation ponum and poline if lastUpdateDate is already present **")
            service.raiseSkipTransaction()
        """
        logger.debug("**line2 child Data **"+erData.getCurrentAction())
    erData.setParentAsCurrent()



logErData(erData)
logger.debug("============= SYNC.GRP_POSTD.USEREXIT.IN.BEFORE: END =============")
#