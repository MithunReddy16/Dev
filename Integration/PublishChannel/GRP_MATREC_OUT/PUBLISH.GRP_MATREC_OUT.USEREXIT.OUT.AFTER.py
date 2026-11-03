#-----------------------------------------------------------------------------------------
# Name:        SYNC.MATRECTRANS.USEREXIT.OUT.AFTER
# Description: Sets formatted values during outbound publish from MATRECTRANS
#
# Publish Channel: SYNCMATRECTRANS
# Event: Integration --> Publish Channel --> User Exit --> After External Exit
#
# Author: Mithun Reddy
# Version: 1.0 - 26-Mar-2025
# Version: 2.0 - AA - 26-Nov-2025
#-----------------------------------------------------------------------------------------

from psdi.iface.mic import StructureData
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote, MboSetRemote
from org.jdom2.output import XMLOutputter
from psdi.mbo import SqlFormat
from java.text import SimpleDateFormat

logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("============= SYNC.MATRECTRANS.USEREXIT.OUT.AFTER: START =============")

erData.breakData()
curMbo = irData.getCurrentMbo()

#-----------------------------------------------------------------------------------------
# Format bin number into required external format
#-----------------------------------------------------------------------------------------
def formatBinNumber(bin_num):
    if not bin_num or bin_num=="":
        return None
    parts = bin_num.split("-")
    if len(parts) != 4:
        logger.debug("Invalid bin number format: " + str(bin_num))
        return None

    seg1, seg2, seg3, seg4 = parts
    merged_seg = seg1 + seg2
    #formatted_seg4 = seg4.zfill(3)
    #return merged_seg + "-" + seg3 + "-" + formatted_seg4
    return merged_seg + "-" + seg3 + "-" + seg4

#-----------------------------------------------------------------------------------------
# Set base values from MATRECTRANS
#-----------------------------------------------------------------------------------------
def setBaseData():
    erData.setCurrentData("pSourceCode", "MAXIMO")
    logger.debug("Set pSourceCode = MAXIMO")

    receivedUnit = curMbo.getString("RECEIVEDUNIT")
    #erData.setCurrentData("pUnitOfMeasure", receivedUnit)
    erData.setCurrentData("pUnitOfMeasure", getGRPUoM(receivedUnit))
    logger.debug("Set pUnitOfMeasure = " + str(receivedUnit))

    qty = curMbo.getDouble("QUANTITY")
    if qty is not None:
        erData.setCurrentData("pTransactionQty", str(abs(qty)))
        logger.debug("Set pTransactionQty = " + str(qty))
        
    cost = curMbo.getDouble("UNITCOST")
    if cost is not None:
        erData.setCurrentData("pUnitPrice", str(cost))
        logger.debug("Set pUnitPrice = " + str(cost))
        
    ActualDate = curMbo.getDate("ACTUALDATE")
    if ActualDate is not None:
        dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
        formattedActualDate = dateFormat.format(ActualDate)
        erData.setCurrentData("pTransactionDate", str(formattedActualDate))
        logger.debug("Set pTransactionDate = " + str(formattedActualDate))
        
#-----------------------------------------------------------------------------------------
# Set item segments
#-----------------------------------------------------------------------------------------
def setItemSegments():
    itemNum = irData.getCurrentDataAsString("ITEMNUM")
    if itemNum:
        parts = itemNum.split("-", 1)
        if len(parts) == 2:
            erData.setCurrentData("pItemSegment1", parts[0])
            erData.setCurrentData("pItemSegment2", parts[1])
            logger.debug("Item Segments: " + str(parts))
    else:
        for i in range(1, 3):
            erData.setCurrentDataNull("pItemSegment" + str(i))

#-----------------------------------------------------------------------------------------
# Set locator and subinventory based on bin and issuetype
#-----------------------------------------------------------------------------------------
def setBinLocator():
    bin = ''
    bin_format = ''
    issuetype = irData.getCurrentDataAsString("ISSUETYPE")

    if issuetype == "SHIPTRANSFER":
        bin = irData.getCurrentDataAsString("FROMBIN")
    elif issuetype == "SHIPRECEIPT":
        bin = irData.getCurrentDataAsString("TOBIN")
    elif issuetype == "TRANSFER":
        bin = irData.getCurrentDataAsString("FROMBIN")
    elif issuetype == "SHIPRETURN":
        bin = irData.getCurrentDataAsString("FROMBIN")
    if bin:
        bin_format = formatBinNumber(bin)
        if bin_format:
            erData.setCurrentData("pLocator", bin_format)
            logger.debug("Set pLocator = " + str(bin_format))

            subinventory ="Shed "+ bin[0:1]
            erData.setCurrentData("pSubInventory", subinventory)
            logger.debug("Set pSubInventory = " + str(subinventory))

#-----------------------------------------------------------------------------------------
# Set store location and lot number
#-----------------------------------------------------------------------------------------
def setStoreAndLot():
    issuetype = irData.getCurrentDataAsString("ISSUETYPE")

    if issuetype == "SHIPTRANSFER":
        #erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("FROMSTORELOC"))
        erData.setCurrentData("pOrganizationId", str(curMbo.getInt("FROMLOCATION.DM_GRPORGID")))
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("FROMLOT"))
    elif issuetype == "SHIPRECEIPT":
        #erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("TOSTORELOC"))
        erData.setCurrentData("pOrganizationId", str(curMbo.getInt("INVENTORY.LOCATIONS.DM_GRPORGID")))
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("TOLOT"))
    elif issuetype == "TRANSFER":
        #erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("FROMSTORELOC"))
        erData.setCurrentData("pOrganizationId", str(curMbo.getInt("FROMLOCATION.DM_GRPORGID")))
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("FROMLOT"))
    elif issuetype == "SHIPRETURN":
        #erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("FROMSTORELOC"))
        erData.setCurrentData("pOrganizationId", str(curMbo.getInt("FROMLOCATION.DM_GRPORGID")))
        erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("FROMLOT"))
#-----------------------------------------------------------------------------------------
# Split and set GL Debit Account segments
#-----------------------------------------------------------------------------------------
def setGLSegments():
    '''
    if curMbo.getString("ISSUETYPE") in ("SHIPRECEIPT"):
        gldebit = curMbo.getString("GLDEBITACCT")
    else:
    '''
    gldebit=curMbo.getString("GLDEBITACCT")
    print("*** gldebit is ***"+gldebit)
    if gldebit is not None and gldebit!='' :
        seg1,seg2,seg3,seg4,seg5,seg6,seg7,seg8=gldebit.split('-',7)
        erData.setCurrentData("psegment1",seg1 )
        erData.setCurrentData("psegment2",seg2 )
        erData.setCurrentData("psegment3",seg3 )
        erData.setCurrentData("psegment4",seg4 )
        erData.setCurrentData("psegment5",seg5)
        erData.setCurrentData("psegment6",seg6 )
        erData.setCurrentData("psegment7",seg7 )
        erData.setCurrentData("psegment8",seg8 )
    else :
        erData.setCurrentDataNull("psegment1")
        erData.setCurrentDataNull("psegment2")
        erData.setCurrentDataNull("psegment3")
        erData.setCurrentDataNull("psegment4")
        erData.setCurrentDataNull("psegment5")
        erData.setCurrentDataNull("psegment6")
        erData.setCurrentDataNull("psegment7")
        erData.setCurrentDataNull("psegment8")

#-----------------------------------------------------------------------------------------
# Set transaction reference
#-----------------------------------------------------------------------------------------
def setTransactionRef():
    pTransRef = irData.getCurrentDataAsString("MATRECTRANSID")
    if pTransRef:
        erData.setCurrentData("pTransRef", "MATRECTRANS-" + pTransRef)
        logger.debug("Set pTransRef = " + pTransRef)
    else:
        erData.setCurrentDataNull("pTransRef")
    

#-----------------------------------------------------------------------------------------
# Set basic transaction data
#-----------------------------------------------------------------------------------------
def getGRPUoM(UOM):
    GRPUoM = UOM
    UoMSet = MXServer.getMXServer().getMboSet("MEASUREUNIT", MXServer.getMXServer().getSystemUserInfo())
    where = SqlFormat(UoMSet.getUserInfo(), "MEASUREUNITID = :1")
    where.setObject(1, "MEASUREUNIT", "MEASUREUNITID", UOM)
    
    UoMSet.setWhere(where.format())
    UoMSet.reset()
    
    UoMMbo = UoMSet.moveFirst()
    if UoMMbo and not UoMMbo.isNull('DM_GRPUNITID'):
        GRPUoM = UoMMbo.getString('DM_GRPUNITID')
    UoMSet.cleanup()
    UoMSet.close()
    
    return  GRPUoM

        
#-----------------------------------------------------------------------------------------
# Set transaction Type
#-----------------------------------------------------------------------------------------
def setTransactionType():

    issuetype = irData.getCurrentDataAsString("ISSUETYPE")
    if issuetype == "SHIPTRANSFER":
        erData.setCurrentData("pTransactionType", "Miscellaneous issue")
    elif issuetype == "SHIPRECEIPT":
        erData.setCurrentData("pTransactionType", "Miscellaneous receipt")
    elif issuetype == "TRANSFER":
        erData.setCurrentData("pTransactionType", "Miscellaneous issue")
    elif issuetype == "SHIPRETURN":
        erData.setCurrentData("pTransactionType", "Miscellaneous issue")
    
    return issuetype
        
#-----------------------------------------------------------------------------------------
# Set duplicate message Type
#-----------------------------------------------------------------------------------------
        
def createDuplicateMessage ():
    logger.debug("***** Duplicate message started ***")
    originalElement = erData.getCurrentData() 
    clonedElement = originalElement.clone()
    parentElement = originalElement.getParent()
    issuetype = None
    logger.debug("***** Duplicate message started1 ***")
    for child in clonedElement.getChildren():
        if child.getName() == "ISSUETYPE":
            issuetype = child.getText()
    logger.debug("***** Duplicate message started2 ***"+str(issuetype))
    if issuetype == "TRANSFER":        
        tobin = None
        tostoreloc = None
        tolot = None
        binformat=None
        subinventory=None
        logger.debug("***** Duplicate message started3 ***")
        for child in clonedElement.getChildren():
            name = child.getName()
            if name == "TOBIN":
                tobin = child.getText()
            elif name == "TOSTORELOC":
                tostoreloc = child.getText()
            elif name == "TOLOT":
                tolot = child.getText()
        if tobin:
            binformat = formatBinNumber(tobin)
            subinventory ="Shed "+ tobin[0:1]
        logger.debug("***** Duplicate message started4 ***")    
        for child in clonedElement.getChildren():
            name = child.getName()
            if name == "pLocator" and binformat:
                child.setText(binformat)
            elif name == "pSubInventory" and subinventory:
                child.setText(subinventory)    
            elif name == "pOrganizationId" and tostoreloc:
                child.setText(tostoreloc)
            elif name == "pLotNumber" and tolot:
                child.setText(tolot)
            elif name == "pTransactionType" :
                child.setText("Miscellaneous receipt")
        logger.debug("***** Duplicate message started5 ***")
    elif issuetype == "SHIPRECEIPT":
        tobin = None
        tostoreloc = None
        tolot = None
        binformat=None
        subinventory=None
        for child in clonedElement.getChildren():
            name = child.getName()
            if name == "TOBIN":
                tobin = child.getText()
            elif name == "TOSTORELOC":
                tostoreloc = child.getText()
            elif name == "TOLOT":
                tolot = child.getText()
        if tobin:
            binformat = formatBinNumber(tobin)
            subinventory ="Shed "+ tobin[0:1]
            
        for child in clonedElement.getChildren():
            name = child.getName()
            if name == "pLocator" and binformat:
                child.setText(binformat)
            elif name == "pSubInventory" and subinventory:
                child.setText(subinventory)    
            elif name == "pOrganizationId" and tostoreloc:
                child.setText(tostoreloc)
            elif name == "pLotNumber" and tolot:
                child.setText(tolot)
            elif name == "pTransactionType" :
                child.setText("Miscellaneous receipt")

    parentElement.addContent(clonedElement)
    logger.debug("***** this is duplicate message end")

    

#-----------------------------------------------------------------------------------------
# Execute all logic
#-----------------------------------------------------------------------------------------
setBaseData()
setItemSegments()
setBinLocator()
setStoreAndLot()
setGLSegments()
setTransactionRef()
issuetype=setTransactionType()
if issuetype in ["TRANSFER", "SHIPRETURN"]:
    createDuplicateMessage()

logger.debug(XMLOutputter().outputString(erData.getData()))
logger.debug("============= SYNC.MATRECTRANS.USEREXIT.OUT.AFTER: END =============")