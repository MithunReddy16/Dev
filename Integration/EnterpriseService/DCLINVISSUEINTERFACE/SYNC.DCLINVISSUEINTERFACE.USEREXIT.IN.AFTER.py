#-----------------------------------------------------------------------------------------
# Script Name:SYNC.DCLINVISSUEINTERFACE.USEREXIT.IN.AFTER
# Description: Set default values for inbound Labware data
#
# Enterprise Service: DCLINVISSUEInterface
#
# Author: Mithun
# Date: 13-July-2026
#*****************************************************************************************


from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider import OslcJSONStructureData
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat
from java.text import SimpleDateFormat
from psdi.app.inventory import InventoryServiceRemote

logger = MXLoggerFactory.getLogger("maximo.custom.inventory")
logger.debug("============= SYNC.DCLINVISSUEINTERFACE.USEREXIT.IN.AFTER =============")
userInfo= MXServer.getMXServer().getSystemUserInfo()

def setDefaultValues(irData):
    logger.debug("****setDefaultValues def start***")
    irData.setCurrentData("ORGID", "DMORG")
    irData.setCurrentData("SITEID", "DM")
    irData.setCurrentData("SENDERSYSID", "DCL")
    irData.setCurrentData("ISSUETYPE", "ISSUE")
    irData.setCurrentData("GLDEBITACCT", "07-000-0000-00000-00-00000-00000-00000") # Defaulting GL Values
    irData.setCurrentData("GLCREDITACCT", "07-000-0000-00000-00-00000-00000-00000")# Defaulting GL Values
    if irData.isCurrentDataNull("ACTUALDATE"):
        irData.setCurrentData("ACTUALDATE", MXServer.getMXServer().getDate())
    #if irData.isCurrentDataNull("STORELOC"):
        #irData.setCurrentData("STORELOC", "M04")  # setting value store as M04
        
    logger.debug("****setDefaultValues def end***")

def issueUnitCheck(irData):
    logger.debug("****issueUnitCheck def start***")
    itemnum = irData.getCurrentDataAsString("ITEMNUM")
    qty = irData.getCurrentDataAsDouble("QUANTITY")
    location=irData.getCurrentDataAsString("STORELOC")
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    invSet = MXServer.getMXServer().getMboSet("INVENTORY", userInfo)
    sqlFormat = SqlFormat(userInfo, "ITEMNUM = :1 and LOCATION = :2")
    sqlFormat.setObject(1, "INVBALANCES", "ITEMNUM", itemnum)
    sqlFormat.setObject(2, "INVBALANCES", "LOCATION", location)
    invSet.setWhere(sqlFormat.format())
    invSet.reset()
    if not invSet.isEmpty() :
        invMbo=invSet.moveFirst()
        labIssue = irData.getCurrentDataAsString("ISSUEUNIT")
        invIssue = invMbo.getString("ISSUEUNIT")
        labIssueNorm = (labIssue or "").strip().upper()
        invIssueNorm = (invIssue or "").strip().upper()
        logger.debug("****labIssueNorm: "+labIssueNorm+" ***invIssueNorm: "+invIssueNorm)
        if invIssueNorm != labIssueNorm :
            invService = MXServer.getMXServer().lookup("INVENTORY")
            conversion = None
            try:
                conversion = invService.getConversionFactor(userInfo, labIssueNorm, invIssueNorm, "ITEMSET", itemnum)
            except:
                try:
                    conversion = invService.getConversionFactor(userInfo, labIssueNorm, invIssueNorm, "ITEMSET")
                except:
                    conversion = invService.getConversionFactor(userInfo, invIssueNorm, labIssueNorm, "ITEMSET")
            
            if conversion :
                newqty=qty*conversion
                irData.setCurrentData("QUANTITY", newqty )
            
    invSet.close() 
    logger.debug("****issueUnitCheck def end***")

def setBinnum(irData):
    logger.debug("****setBinnum def start***")
    if irData.isCurrentDataNull("BINNUM"):
        itemnum = irData.getCurrentDataAsString("ITEMNUM")
        location=irData.getCurrentDataAsString("STORELOC")
        userInfo = MXServer.getMXServer().getSystemUserInfo()
        invbalSet = MXServer.getMXServer().getMboSet("INVBALANCES", userInfo)
        sqlFormat = SqlFormat(userInfo, "ITEMNUM = :1 and LOCATION = :2")
        sqlFormat.setObject(1, "INVBALANCES", "ITEMNUM", itemnum)
        sqlFormat.setObject(2, "INVBALANCES", "LOCATION", location)
        invbalSet.setWhere(sqlFormat.format())
        invbalSet.reset()
        if not invbalSet.isEmpty() :
            qty=irData.getCurrentDataAsDouble("QUANTITY")
            invbalMbo=invbalSet.moveFirst()
            while invbalMbo is not None :
                curbal=invbalMbo.getDouble("CURBAL")
                if curbal>=qty :
                    bin = invbalMbo.getString("BINNUM")
                    irData.setCurrentData("BINNUM", bin )
                    break 
                invbalMbo=invbalSet.moveNext()
        invbalSet.close() 
        logger.debug("****setBinnum def stop***")


def setUnitLineCost(irData):
    logger.debug("****setUnitLineCost def start***")
    itemnum = irData.getCurrentDataAsString("ITEMNUM")
    qty = irData.getCurrentDataAsDouble("QUANTITY")
    location=irData.getCurrentDataAsString("STORELOC")
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    invcostSet = MXServer.getMXServer().getMboSet("INVCOST", userInfo)
    sqlFormat = SqlFormat(userInfo, "ITEMNUM = :1 and LOCATION = :2")
    sqlFormat.setObject(1, "INVBALANCES", "ITEMNUM", itemnum)
    sqlFormat.setObject(2, "INVBALANCES", "LOCATION", location)
    invcostSet.setWhere(sqlFormat.format())
    invcostSet.reset()
    if not invcostSet.isEmpty() :
        invcostMbo=invcostSet.moveFirst()
        invAvgCost=invcostMbo.getDouble("AVGCOST")
        irData.setCurrentData("UNITCOST", invAvgCost )
        lineCost=invAvgCost * qty 
        irData.setCurrentData("LINECOST", lineCost )
    logger.debug("****setUnitLineCost def stop***")


def logErData(process,irData):
    try: 
        logger.debug("===== Pretty Printed "+process +" =====")
        logger.debug(XMLOutputter().outputString(irData.getData()))
    except Exception, e:
        logger.error("Error while printing irData XML: " + str(e))
        
#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------

isStructurePresent = True
irData.breakData()
if irData.isMultiObjectStructure() :
    logger.debug("=====it is isMultiObjectStructure =====")

logErData("Before Process",irData)
irData.moveToFirstObjectStruture()
while (isStructurePresent):
    #skipRule(irData)
    #mandatoryChecks(irData)
    setDefaultValues(irData)
    issueUnitCheck(irData)
    setBinnum(irData)
    setUnitLineCost(irData)
    isStructurePresent = irData.moveToNextObjectStructure()
    
logErData("After Process",irData)
logger.debug("============= SYNC.DCLINVISSUEINTERFACE.USEREXIT.IN.AFTER: END =============")