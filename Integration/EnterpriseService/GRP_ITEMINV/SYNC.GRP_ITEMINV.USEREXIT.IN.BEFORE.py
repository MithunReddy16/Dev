#-----------------------------------------------------------------------------------------
# Script Name : SYNC.GRP_ITEMINV.USEREXIT.IN.BEFORE
# Description : Inbound User Exit Before External Exit for GRP_ITEMINV interface
#
# Enterprise Service : GRP_ITEMINV
# Object Structure   : GRP_ITEMINV
# Event              : Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------

from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from java.io import StringWriter
from javax.xml.transform import TransformerFactory
from javax.xml.transform.dom import DOMSource
from javax.xml.transform.stream import StreamResult
from org.jdom2.output import XMLOutputter

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("========== START: SYNC.GRP_ITEMINV.USEREXIT.IN.BEFORE ==========")

#-----------------------------------------------------------------------------------------
# Set default values if missing
#-----------------------------------------------------------------------------------------
def setDefaultValues(erData):
    if erData.isCurrentDataNull("ITEMSETID"):
        erData.setCurrentData("ITEMSETID", "ITEMSET")

#-----------------------------------------------------------------------------------------
# Normalize UOM and status fields
#-----------------------------------------------------------------------------------------
def normalizeFields(erData):
    uom = erData.getCurrentDataAsString("ORDERUNIT")
    status = erData.getCurrentDataAsString("STATUS")

    if status is not None and status.upper() == "ACTIVE":
        erData.setCurrentData("STATUS", "ACTIVE")
    else:
        erData.setCurrentData("STATUS", "INACTIVE")
    
    if (erData.isInCurrentData("COMMODITY") and not erData.isCurrentDataNull("COMMODITY")):
        commodityCode = erData.getCurrentDataAsString("COMMODITY")
        if commodityCode[0:2] == "99" and not commodityCode == "99999-000":
            erData.setCurrentData("ROTATING", "Y")
    

#-----------------------------------------------------------------------------------------
# Process commodity group logic
#-----------------------------------------------------------------------------------------
def setcommodityGroup(erData):
    orgCode = erData.getCurrentDataAsString("DM_GRPORG")
    logger.debug("===== currentdata ====="+str(orgCode))
    if orgCode is not None and orgCode == "M00":
        commodityCode = erData.getCurrentDataAsString("COMMODITY")
        if commodityCode is not None:
            parts = commodityCode.split("-")
            if len(parts) >= 2 :
                parent = parts[0]
                erData.setCurrentData("COMMODITYGROUP", parent)
    else:
        
        logErData(erData)
        print("Skipping transaction due to ORGCODE mismatch.")
        service.raiseSkipTransaction()

#-----------------------------------------------------------------------------------------
# Pretty print the erData XML for debugging
#-----------------------------------------------------------------------------------------
def logErData(erData):
    try:
        logger.debug(XMLOutputter().outputString(erData.getData()))

    except Exception, e:
        logger.error("Error while printing erData XML: " + str(e))

#-----------------------------------------------------------------------------------------
# Main Execution
#-----------------------------------------------------------------------------------------
erData.breakData()
logger.debug("** currentbefore Action: "+str(erData.getAction()))

setDefaultValues(erData)
normalizeFields(erData)
setcommodityGroup(erData)

logErData(erData)
logger.debug("========== END: SYNC.GRP_ITEMINV.USEREXIT.IN.BEFORE ==========")