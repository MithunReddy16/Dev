#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRP_MEASUREUNIT.USEREXIT.IN.BEFORE
# Description: Set default values for inbound GR data (XML-based)
#
# Enterprise Service: GRP_MEASUREUNIT
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
logger.debug("============= SYNC.GRP_MEASUREUNIT.USEREXIT.IN.BEFORE: START =============")


def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")
 
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")    
    erData.setCurrentData("ORGID", "DMORG")
    erData.setCurrentData("SITEID", "DM")
    erData.setCurrentData("ABBREVIATION", erData.getCurrentDataAsString("MEASUREUNITID"))
        
def setBusinessValues(erData):
    logger.debug("***setBusinessValues def***")                   

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
mandatoryChecks(erData)
setDefaultValues(erData)
setBusinessValues(erData)
logErData(erData)
logger.debug("============= SYNC.GRP_MEASUREUNIT.USEREXIT.IN.BEFORE: END =============")