#-----------------------------------------------------------------------------------------
# Name:        SYNC.GRP_SUPPLIERCONTACT.USEREXIT.IN.BEFORE
# Description: Set default values for inbound GR data (XML-based)
#
# Enterprise Service: GRP_SUPPLIERCONTACT
# Event: Integration --> Enterprise Service --> Request --> User Exit --> Before External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 21-Mar-2025
# Version: 1.0 - -AA- 01-12-25
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
logger.debug("============= SYNC.GRP_SUPPLIERCONTACT.USEREXIT.IN.BEFORE: START =============")


def mandatoryChecks(erData):
    logger.debug("***mandatorychecks def***")
 
def setDefaultValues(erData):
    logger.debug("Setting default values if missing...")    
    erData.setCurrentData("ORGID", "DMORG")
        
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

isStructurePresent = True

userInfo = MXServer.getMXServer().getSystemUserInfo()

erData.breakData()
erData.moveToFirstObjectStruture()

while (isStructurePresent):
    ContactList = erData.getChildrenData("COMPCONTACT")
    ContactListCount = ContactList.size()
    if (ContactList is not None and ContactListCount > 0):
        #for poLine in poLineList:
        for i in range(ContactListCount):
            erData.setAsCurrent(ContactList, i)
            Contact = ""
            if ( erData.isInCurrentData("DM_FIRSTNAME") and not erData.isCurrentDataNull("DM_FIRSTNAME")):
                Contact = Contact +  erData.getCurrentDataAsString("DM_FIRSTNAME") 
            if ( erData.isInCurrentData("DM_LASTNAME") and not erData.isCurrentDataNull("DM_LASTNAME")):
                if ( not erData.isInCurrentData("DM_FIRSTNAME") or erData.isCurrentDataNull("DM_FIRSTNAME")):
                    Contact = erData.getCurrentDataAsString("DM_LASTNAME")
                else:
                    Contact = Contact + " " +  erData.getCurrentDataAsString("DM_LASTNAME")
            if Contact != "":
                erData.setCurrentData("CONTACT", Contact)
            else:
                service.error("DM","ERROR","One or more contract do not have a name")
    
    isStructurePresent = erData.moveToNextObjectStructure()


logErData(erData)


logger.debug("============= SYNC.GRP_SUPPLIERCONTACT.USEREXIT.IN.BEFORE: END =============")