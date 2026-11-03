#-----------------------------------------------------------------------------------------
# Script Name : SYNC.GRP_INVENTORY.USEREXIT.IN.BEFORE
# Description : External Exit In script for GRP_INVENTORY inbound interface.
#
# Enterprise Service : GRP_INVENTORY
# Object Structure   : GRP_INVENTORY
# Event              : Integration --> Enterprise Service --> Request --> User Exit --> External Exit
#
# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------

from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= SYNC.GRP_INVENTORY.USEREXIT.IN.BEFORE: START=============")

#-----------------------------------------------------------------------------------------
# Set default values and normalize category/status
#-----------------------------------------------------------------------------------------
def setDefaults(erData):
    storeroom = erData.getCurrentDataAsString("LOCATION")
    itemNum = erData.getCurrentDataAsString("ITEMNUM")
    category = erData.getCurrentDataAsString("CATEGORY")
    status = erData.getCurrentDataAsString("STATUS")
    uom = erData.getCurrentDataAsString("ORDERUNIT")
    logger.debug("***storeroom is "+str(storeroom))
    if storeroom != "M00":
        erData.setCurrentData("ITEMSETID", "ITEMSET")
        erData.setCurrentData("SITEID","DM")
        if uom is not None:
            erData.setCurrentData("ISSUEUNIT", uom)

        if  category == 'Y':
            erData.setCurrentData("CATEGORY", "STK")
        else:
            erData.setCurrentData("CATEGORY", "NS")

        if status is not None and status.upper() == "ACTIVE":
            erData.setCurrentData("STATUS", "ACTIVE")
        else:
            erData.setCurrentData("STATUS", "INACTIVE")
    else:
        print("****STOREROOM is-M00 So skipping transaction***")
        service.raiseSkipTransaction()

#-----------------------------------------------------------------------------------------
# Print full erData for debug
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
logger.debug("** Root Action: " + erData.getAction())

setDefaults(erData)
logErData(erData)

logger.debug("============= SYNC.GRP_INVENTORY.USEREXIT.IN.BEFORE: END =============")