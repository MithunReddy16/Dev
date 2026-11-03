#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRP_PRACK.USEREXIT.IN.BEFORE
# Description: Set default values and normalize status for inbound PR data (XML-based)
#
# Enterprise Service: GRP_PRACK
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 22-May-2025
# Version: 2.0 - 14-Nov-2025
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

logger = MXLoggerFactory.getLogger("maximo.custom")
logger.debug("=============Mithun SYNC.GRP_PRACK.USEREXIT.IN.BEFORE: START =============")
#-----------------------------------------------------------------------------------------
# CHeck Mandatory Checks for fields in the incoming XML data
#-----------------------------------------------------------------------------------------

def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")

#-----------------------------------------------------------------------------------------
# Set default values for required fields if missing in the incoming XML data
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")

    if erData.isCurrentDataNull("SITEID"):
        erData.setCurrentData("SITEID", "DM")
        
#-----------------------------------------------------------------------------------------
# Converting the incoming status values to Maximo internal statuses
#-----------------------------------------------------------------------------------------
def convertStatus(erData):
    if erData.isInCurrentData("STATUS") and not erData.isCurrentDataNull("STATUS"):
        status = erData.getCurrentDataAsString("STATUS").strip()
        if status.upper() == "REJECTED":
            erData.setCurrentData("STATUS", "CAN")
            erData.setCurrentData("STATUSIFACE", "1")
        elif status.upper() == "RETURNED":
            #erData.setCurrentData("STATUS", "GRPRETURN")
            erData.setCurrentData("STATUS", "CAN")
            erData.setCurrentData("STATUSIFACE", "1")
        elif status.upper() == "APPROVED":
            erData.setCurrentData("STATUS", "GRPAPPR")
            erData.setCurrentData("STATUSIFACE", "0")
        else:
            service.error("DM","genericerror",["Un-Supported Status"])

            
        '''
        if status == "APPROVED":
            erData.setCurrentData("STATUS", "APPR")
        elif status == "INCOMPLETE":            
            erData.setCurrentData("STATUS", "WAPPR")
        elif status == "REJECTED":
            erData.setCurrentData("STATUS", "CAN")
        elif status == "RETURNED":
            erData.setCurrentData("STATUS", "GRPRETURN")
        elif status == "IN PROCESS":
            erData.setCurrentData("STATUS", "INPRG")
        '''
            
def skipRule(erData):
    try:
        # checking for APPR Status
        if erData.isCurrentDataNull("PRNUM"):
             service.raiseSkipTransaction()
        else:
            prnum = erData.getCurrentDataAsString("PRNUM")
            logger.debug("****prnum : " + str(prnum))
            prSet = MXServer.getMXServer().getMboSet("PR", MXServer.getMXServer().getSystemUserInfo())
            where = SqlFormat(prSet.getUserInfo(), "PRNUM = :1 AND SITEID = :2 AND ( STATUS=:3 OR STATUS=:4) ")
            where.setObject(1, "PR", "PRNUM", prnum)
            where.setObject(2, "PR", "SITEID", "DM")
            where.setObject(3, "PR", "STATUS", "APPR")
            where.setObject(4, "PR", "STATUS", "GRPAPPR")
            prSet.setWhere(where.format())
            prSet.reset()
            logger.debug("** pr getwhere is  " +prSet.getWhere()  )
            PRMbo = prSet.moveFirst()
            if not PRMbo:
                logger.debug("** SKIPING the TRANSCATION PR is not Present ***")
                service.raiseSkipTransaction()
            prSet.close()
    except Exception as e:
        logger.error("*** Error in checking the PR with APPR status : " + str(e))


def setBusinessValues(erData):
    logger.debug("**** in business def****")
    

def setChildrenValuesNull(erData) :
    
    erData.removeFromCurrentData("ITEMNUM")
    erData.removeFromCurrentData("COMMODITY")
    erData.removeFromCurrentData("DM_ITEMID")
    erData.removeFromCurrentData("DESCRIPTION")
    erData.removeFromCurrentData("ORDERQTY")
    erData.removeFromCurrentData("UNITCOST")
    erData.removeFromCurrentData("ORDERUNIT")
    erData.removeFromCurrentData("DM_CREATIONDATE")

    '''
    #Keeping these for now to match with receving
    erData.removeFromCurrentData("DM_QTYREC")
    erData.removeFromCurrentData("DM_QTYACCEP")
    erData.removeFromCurrentData("DM_QTYDEL")
    erData.removeFromCurrentData("DM_QTYCAN")
    erData.removeFromCurrentData("DM_QTYREJ")
    '''
    
    
    
        
        
        
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
logErData(erData)

skipRule(erData)

mandatoryChecks(erData)
setDefaultValues(erData)
convertStatus(erData)
setBusinessValues(erData)

# manipulating childern Data 
prnum=erData.getCurrentDataAsString("PRNUM")
prLineList=erData.getChildrenData("PRLINE")
noOfPRLines=prLineList.size()
if (noOfPRLines is not None and noOfPRLines > 0):
    for i in range(noOfPRLines):        
        erData.setAsCurrent(prLineList,i)
        setChildrenValuesNull(erData)
        
    erData.setParentAsCurrent()


logErData(erData)
#service.error('A',XMLOutputter().outputString(erData.getData()))

logger.debug("============= SYNC.GRP_PRACK.USEREXIT.IN.BEFORE: END =============")