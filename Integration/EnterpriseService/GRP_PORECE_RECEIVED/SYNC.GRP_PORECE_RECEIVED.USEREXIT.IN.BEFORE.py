#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRP_PORECE_RECEIVED.USEREXIT.IN.BEFORE
# Description: Set default values for inbound GR data (XML-based)
#
# Enterprise Service: GRP_PORECE_RECEIVED
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

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= SYNC.GRP_PORECE_RECEIVED.USEREXIT.IN.BEFORE: START =============")

def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")
    receiptQty = erData.getCurrentDataAsDouble("RECEIPTQUANTITY")
    if receiptQty < 0:
        raise MXApplicationException("userexit", "negativereceiptqty")
    
    



#-----------------------------------------------------------------------------------------
# Set default values for missing fields in inbound XML
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")

    if erData.isCurrentDataNull("SITEID"):
        erData.setCurrentData("SITEID", "DM")
        logger.debug("**SITEID defaulted to DM")
    
    if erData.isCurrentDataNull("POSITEID"):
        erData.setCurrentData("POSITEID", "DM")
        logger.debug("**SITEID defaulted to DM")
    
    if erData.isCurrentDataNull("SOURCESYSID"):
        erData.setCurrentData("SOURCESYSID", "GRP")
        logger.debug("**SOURCESYSID defaulted to GRP")
    
    erData.setCurrentData("ENTERBY", "MAXADMIN")
    logger.debug("**ENTERBY defaulted to MAXADMIN")

def setBusinessValues(erData):
    logger.debug("**** in business def****")
    ponum = erData.getCurrentDataAsString("PONUM")
    polinenum = erData.getCurrentDataAsString("POLINENUM")
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    polineSet = MXServer.getMXServer().getMboSet("POLINE", userInfo)
    sqlFormat = SqlFormat(userInfo, "ponum = :1 and polinenum = :2")
    sqlFormat.setObject(1, "POLINE", "PONUM", ponum)
    sqlFormat.setObject(2, "POLINE", "POLINENUM", polinenum)
    polineSet.setWhere(sqlFormat.format())
    polineSet.reset()
    
    if not polineSet.isEmpty():
        linetype = polineSet.moveFirst().getString("LINETYPE")
        if linetype== "ITEM" :
            erData.setCurrentData("LINETYPE", "ITEM")
        if linetype== "MATERIAL" :
            erData.setCurrentData("LINETYPE", "MATERIAL")    
        if linetype== "SERVICE" :
            erData.setCurrentData("LINETYPE", "SERVICE")
            receiptQty = erData.getCurrentDataAsDouble("RECEIPTQUANTITY")
            erData.setCurrentDataNull("RECEIPTQUANTITY")
            erData.setCurrentData("QTYTORECEIVE", receiptQty)
            
          
    # passing binnum 
    binnum = erData.getCurrentDataAsString("TOBIN")
    if binnum is not None :
        binnum=formatBin(binnum)
        erData.setCurrentData("TOBIN", str(binnum))
    
    
        
def formatBin(binnum) :
    
    parts = binnum.split('-')
    if len(parts) != 3:
        raise MXApplicationException("userexit", "invalidbinformat")

    first_part = parts[0]  
    second_part = parts[1]  
    third_part = parts[2]   
    
    first_segment = first_part[0]  
    second_segment = first_part[1:]
    third_segment = second_part  
    fourth_segment = third_part   ##[1:]  
    
    result = first_segment + '-' + second_segment + '-' + third_segment + '-' + fourth_segment
    
    return result


def checkSkiprules(erData) :
    ponum = erData.getCurrentDataAsString("PONUM") 
    polinenum = erData.getCurrentDataAsString("POLINENUM")
    externalid = erData.getCurrentDataAsString("EXTERNALREFID")  
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    poSet = MXServer.getMXServer().getMboSet("PO", userInfo)
    sqlFormat = SqlFormat(userInfo, "PONUM = :1 and SITEID = :2")
    sqlFormat.setObject(1, "PO", "PONUM", ponum)
    sqlFormat.setObject(2, "PO", "SITEID", "DM")
    poSet.setWhere(sqlFormat.format())
    poSet.reset()
    if not poSet.isEmpty() :
        logger.debug("** if poset not empty**")
        linetype=erData.getCurrentDataAsString("LINETYPE")
        """
        if linetype in[ "ITEM","MATERIAL" ]:
            matrectransSet = MXServer.getMXServer().getMboSet("MATRECTRANS", userInfo)
            sqlFormat = SqlFormat(userInfo, "PONUM = :1 and POLINENUM = :2 AND EXTERNALREFID=:3 ")
            sqlFormat.setObject(1, "MATRECTRANS", "PONUM", ponum)
            sqlFormat.setObject(2, "MATRECTRANS", "POLINENUM", "DM")
            sqlFormat.setObject(3, "MATRECTRANS", "EXTERNALREFID", externalid)
            matrectransSet.setWhere(sqlFormat.format())
            matrectransSet.reset()
            if not matrectransSet.isEmpty() :
                service.raiseSkipTransaction()   
        elif linetype in[ "SERVICE" ]:
            servrectransSet = MXServer.getMXServer().getMboSet("SERVRECTRANS", userInfo)
            sqlFormat = SqlFormat(userInfo, "PONUM = :1 and POLINENUM = :2 AND EXTERNALREFID=:3 ")
            sqlFormat.setObject(1, "SERVRECTRANS", "PONUM", ponum)
            sqlFormat.setObject(2, "SERVRECTRANS", "POLINENUM", "DM")
            sqlFormat.setObject(3, "SERVRECTRANS", "EXTERNALREFID", externalid)
            matrectransSet.setWhere(sqlFormat.format())
            matrectransSet.reset()
            if not matrectransSet.isEmpty() :
                service.raiseSkipTransaction()
                """
    else :
        print("*** skiping the transcation there is no PO***")
        service.raiseSkipTransaction()
        
    

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
erData.setAction("Add")
logger.debug("** Parent action **"+str(erData.getAction()))
mandatoryChecks(erData)
setDefaultValues(erData)
setBusinessValues(erData)
checkSkiprules(erData)
logErData(erData)

logger.debug("============= SYNC.GRP_PORECE_RECEIVED.USEREXIT.IN.BEFORE: END =============")